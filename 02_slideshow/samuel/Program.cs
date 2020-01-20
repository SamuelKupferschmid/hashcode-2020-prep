using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.Serialization.Formatters.Binary;
using System.Threading.Tasks;

namespace SlideShow
{
    class Program
    {
        static void Main(string[] args)
        {
            new SlideShow("in\\c_memorable_moments.txt").Solve();

            return;
            foreach (var file in Directory.GetFiles("in"))
                new SlideShow(file).Solve();
        }
    }

    public class SlideShow
    {
        public string Filename { get; }

        public SlideShow(string filename)
        {
            Filename = filename;
        }

        public void Solve()
        {
            var lineSplits = File.ReadLines(Filename).Skip(1).Select(l => l.Split(" ")).ToList();

            short index = 0;
            var tags = new Dictionary<string, int>();
            foreach (var tag in lineSplits.SelectMany(s => s.Skip(2)).Distinct())
            {
                tags.Add(tag, index++);
            }

            var pictures = lineSplits
                .Select((splits, i) => new Picture
                {
                    Index = i,
                    IsVertical = splits[0] == "V",
                    Tags = splits.Skip(2).Select(s => tags[s]).ToHashSet(),
                }).ToList();

            var verticalPictures = pictures.Where(p => p.IsVertical).ToList();
            var horizontalPictures = pictures.Where(p => !p.IsVertical).ToList();

            var verticalTags = Cache(() =>
            {
                var t = new int[verticalPictures.Count][][];

                Parallel.For(0, t.Length, i =>
                {
                    t[i] = new int[i][];
                    for (int j = 0; j < i; j++)
                    {
                        var set = new HashSet<int>(verticalPictures[i].Tags);
                        set.UnionWith(verticalPictures[j].Tags);

                        t[i][j] = set.ToArray();
                    }
                });

                return t;
            }, "tags");

            var scores = Cache(() =>
            {
                var s = new byte[horizontalPictures.Count][];

                Parallel.For(0, s.Length, i =>
                {
                    s[i] = new byte[i];
                    for (int j = 0; j < i; j++)
                    {
                        s[i][j] = GetScore(horizontalPictures[i].Tags, horizontalPictures[j].Tags);
                    }
                });

                return s;
            }, "score");

            for (int i = scores.Length - 1; i >= 0; i--)
            {
                if (scores[i].All(s => s == 0))
                {
                    var maxScore = 0;
                    var maxRow = 0;
                    var maxCol = 0;

                    for (int row = 0; row < verticalTags.Length; row++)
                    {
                        for (int col = 0; col < row; col++)
                        {
                            var score = GetScore(horizontalPictures[i].Tags, new HashSet<int>(verticalTags[row][col]));
                            if (score > maxScore)
                            {
                                maxScore = score;
                                maxRow = row;
                                maxCol = col;
                            }
                        }
                    }
                    
                }
            }
        }

        private T Cache<T>(Func<T> func, string name)
        {
            var formatter = new BinaryFormatter();
            T result = default(T);

            name = $"{Path.GetFileNameWithoutExtension(Filename)}_{name}";

            if (File.Exists(name))
            {
                using var s = File.OpenRead(name);
                try
                {
                    result = (T) formatter.Deserialize(s);
                    return result;
                } catch { }
            }

            result = func();
            using var stream = File.OpenWrite(name);
            formatter.Serialize(stream, result);
            return result;
        }

        private byte GetScore<T>(HashSet<T> tags1, HashSet<T> tags2)
        {
            var intersection = (byte) tags1.Intersect(tags2).Count();

            if (intersection == 0)
            {
                return 0;
            }

            var left = (byte) tags1.Except(tags2).Count();
            var right = (byte) tags2.Except(tags1).Count();

            return new[] {intersection, left, right}.Min();
        }

        [Serializable]
        public class Picture
        {
            public bool IsVertical { get; set; }

            public int Index { get; set; }

            public HashSet<int> Tags { get; set; }
        }
    }
}