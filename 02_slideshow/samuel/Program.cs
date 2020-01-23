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
            var random = new Random(1);

            var pictures = Cache(() =>
            {
                var lineSplits = File.ReadLines(Filename).Skip(1).Select(l => l.Split(" ")).ToList();
                short index = 0;
                var tags = new Dictionary<string, int>();
                foreach (var tag in lineSplits.SelectMany(s => s.Skip(2)).Distinct())
                {
                    tags.Add(tag, index++);
                }

                return lineSplits
                    .Select((splits, i) => new Picture
                    {
                        Index = i,
                        IsVertical = splits[0] == "V",
                        Tags = splits.Skip(2).Select(s => tags[s]).ToHashSet(),
                    }).ToList();
            }, "pictures");

            pictures = pictures.Where(p => !p.IsVertical).ToList();

            var buckets = CreateBuckets(pictures, 10).ToList();
            var score = 0;
            var link = new HashSet<int>();

            foreach (var bucket in buckets)
            {
                var (bucketScore, tail) = SolveBucket(bucket, link);
                score += bucketScore;
                link = tail;
            }
        }

        private (int score, HashSet<int>) SolveBucket(Bucket bucket, HashSet<int> head)
        {
            var visited = new HashSet<int>();

            var linkScores = bucket.Pictures.Select(p => (int)GetScore(p.Tags, head)).ToList();

            var (current, score) = linkScores.ArgMax();
            visited.Add(current);

            while (visited.Count < bucket.Pictures.Count)
            {
                
                var scores = bucket.AdjacencyMatrix[current];

                var maxVal = -1;
                var maxIndex = -1;

                for (int i = 0; i < scores.Length; i++)
                {
                    if (i != current && !visited.Contains(i) && scores[i] > maxVal)
                    {
                        maxVal = scores[i];
                        maxIndex = i;
                    }
                }

                score += maxVal;
                current = maxIndex;
                visited.Add(current);
            }

            return (score, bucket.Pictures[current].Tags);
        }

        private IEnumerable<Bucket> CreateBuckets(IList<Picture> pictures, int bucketSize)
        {
            for (int i = 0; i < pictures.Count; i++)
            {
                var bucket = Cache(() =>
                {
                    var bucketPictures = pictures.Skip(i).Take(bucketSize).ToList();

                    return new Bucket
                    {
                        Pictures = bucketPictures,
                        AdjacencyMatrix = ExtractScores(bucketPictures)
                    };
                }, $"bucket_{i/bucketSize}");

                yield return bucket;
            }
        }

        private byte[][] ExtractScores(List<Picture> pictures)
        {
            var s = new byte[pictures.Count][];
            for (int i = 0; i < pictures.Count; i++)
            {
                s[i] = new byte[pictures.Count];
            }

            Parallel.For(0, s.Length, i =>
            {
                for (int j = 0; j < i; j++)
                {
                    var score = GetScore(pictures[i].Tags, pictures[j].Tags);
                    s[i][j] = score;
                    s[j][i] = score;
                }
            });

            return s;
        }

        private int[][][] ExtractVerticalTags(List<Picture> verticalPictures)
        {
            return Cache(() =>
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
        }

        private T Cache<T>(Func<T> func, string name)
        {
            Directory.CreateDirectory(Path.GetFileNameWithoutExtension(Filename));
            var formatter = new BinaryFormatter();
            T result = default(T);

            name = $"{Path.GetFileNameWithoutExtension(Filename)}/{name}";

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
        public class Bucket
        {
            public List<Picture> Pictures { get; set; }
            public byte[][] AdjacencyMatrix;
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