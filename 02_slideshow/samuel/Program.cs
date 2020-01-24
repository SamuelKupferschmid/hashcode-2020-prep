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
            //new SlideShow("in\\c_memorable_moments.txt").Solve();

            var score = 0;
            //return;
            foreach (var file in Directory.GetFiles("in"))
                score += new SlideShow(file).Solve();

            Console.WriteLine($"Total: {score}");
            Console.ReadKey();
        }
    }

    public class SlideShow
    {
        public string Filename { get; }

        public SlideShow(string filename)
        {
            Filename = filename;
        }

        public int Solve()
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
                    }).OrderBy(_ => random.Next()).ToList();
            }, "pictures");

            var buckets = CreateBuckets(pictures, 5000, 20);
            var score = 0;
            var link = new HashSet<int>();

            var slides = new List<string>();

            foreach (var bucket in buckets)
            {
                var (bucketScore, bucketSlides, tail) = SolveBucket(bucket, link);
                score += bucketScore;
                link = tail;
                slides.AddRange(bucketSlides);
            }

            slides = new[] {$"score -> {score}", slides.Count.ToString()}.Concat(slides).ToList();


            File.WriteAllLines(Path.GetFileNameWithoutExtension(Filename) + ".txt", slides);

            Console.WriteLine($"{Filename}: {score}");
            return score;
        }

        private (int score, IList<string> slides, HashSet<int> tail) SolveBucket(Bucket bucket, HashSet<int> head)
        {
            var slides = new List<string>();
            var visited = new HashSet<int>();

            var allSlides = bucket.GetSlides().ToList();

            void visit(int id)
            {
                if (allSlides[id] is CombinedPicture slide)
                {
                    for (int i = bucket.HorizontalSlides.Count; i < allSlides.Count; i++)
                    {
                        if (allSlides[i] is CombinedPicture target)
                        {
                            if (new[] {slide.Left, slide.Right, target.Left, target.Right}.Distinct().Count() < 4)
                            {
                                visited.Add(i);
                            }
                        }
                    }

                    slides.Add($"{slide.Left.Index} {slide.Right.Index}");
                }
                else
                {
                    slides.Add(allSlides[id].Index.ToString());
                }

                visited.Add(id);
            }


            var linkScores = allSlides.Select(p => (int) GetScore(p is CombinedPicture vSlide ? vSlide.Left.Tags : p.Tags, head)).ToList();

            var (current, score) = linkScores.ArgMax();
            visit(current);

            while (visited.Count < allSlides.Count)
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
                visit(current);
            }

            var tail = allSlides[current];

            return (score, slides, tail is CombinedPicture vSlide ? vSlide.Right.Tags : tail.Tags);
        }

        private IEnumerable<Bucket> CreateBuckets(IList<Picture> pictures, int horizontalSize, int verticalSize)
        {
            var hPics = pictures.Where(p => !p.IsVertical).ToList();
            var vPics = pictures.Where(p => p.IsVertical).ToList();

            int bucketCount = (int) Math.Max(Math.Ceiling((double) hPics.Count / horizontalSize),
                Math.Ceiling((double) vPics.Count / verticalSize));

            for (int i = 0; i < bucketCount; i++)
            {
                var bucket = Cache(() =>
                {
                    var hIndex = i * horizontalSize;
                    var vIndex = i * verticalSize;

                    var hSlides = hPics.Skip(hIndex).Take(horizontalSize).ToList();
                    var vPictures = vPics.Skip(vIndex).Take(verticalSize).ToList();

                    var vSlides = new List<CombinedPicture>();

                    for (int i = 0; i < vPictures.Count; i++)
                    {
                        for (int j = i + 1; j < vPictures.Count; j++)
                        {
                            var pic1 = vPictures[i];
                            var pic2 = vPictures[j];
                            vSlides.Add(new CombinedPicture
                            {
                                Index = -1,
                                Left = pic1,
                                Right = pic2,
                            });
                            vSlides.Add(new CombinedPicture
                            {
                                Index = -1,
                                Left = pic2,
                                Right = pic1,
                            });
                        }
                    }

                    return new Bucket
                    {
                        HorizontalSlides = hSlides,
                        VerticalSlides = vSlides,
                        AdjacencyMatrix = ExtractScores(hSlides.Concat(vSlides).ToList())
                    };
                }, $"bucket_{i}_{horizontalSize}_{verticalSize}");

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
                    var leftTag = pictures[i] is CombinedPicture p ? p.Left.Tags : pictures[i].Tags;
                    var rightTag = pictures[j] is CombinedPicture p2 ? p2.Right.Tags : pictures[j].Tags;
                    s[i][j] = GetScore(leftTag, rightTag);
                    s[j][i] = GetScore(rightTag, leftTag);
                }
            });

            return s;
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
                }
                catch
                {
                }
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
            public List<Picture> HorizontalSlides { get; set; }
            public List<CombinedPicture> VerticalSlides { get; set; }

            public IEnumerable<Picture> GetSlides() => HorizontalSlides.Concat(VerticalSlides);

            public byte[][] AdjacencyMatrix;
        }

        [Serializable]
        public class Picture
        {
            public bool IsVertical { get; set; }

            public int Index { get; set; }

            public HashSet<int> Tags { get; set; }
        }

        [Serializable]
        public class CombinedPicture : Picture
        {
            public Picture Left { get; set; }
            public Picture Right { get; set; }
        }
    }
}