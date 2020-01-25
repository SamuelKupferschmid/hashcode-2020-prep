using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;
using System.Runtime.Serialization.Formatters.Binary;
using System.Threading.Tasks;
using ShellProgressBar;
using SolutionLibrary;

namespace SlideShow
{
    public class SlideShow : Solution
    {
        public override (int score, IList<string> output) Solve(string[] input)
        {
            var random = new Random(1);

            var pictures = ExecuteCached(() =>
            {
                var lineSplits = input.Skip(1).Select(l => l.Split(" ")).ToList();
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

            var buckets = CreateBuckets(pictures, 35000, 10);
            var score = 0;
            var link = new HashSet<int>();

            var slides = new List<string>();

            Console.WriteLine();

            foreach (var bucket in buckets)
            {
                var (bucketScore, bucketSlides, tail) = SolveBucket(bucket, link);
                score += bucketScore;
                link = tail;
                slides.AddRange(bucketSlides);
            }

            Console.WriteLine();

            slides = new[] {$"score -> {score}", slides.Count.ToString()}.Concat(slides).ToList();


            File.WriteAllLines(Path.GetFileNameWithoutExtension(Filename) + ".txt", slides);

            Console.WriteLine($"{Filename}: {score}");
            return (score, slides);
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


            var linkScores = allSlides
                .Select(p => (int) GetScore(p is CombinedPicture vSlide ? vSlide.Left.Tags : p.Tags, head)).ToList();

            var (current, score) = linkScores.ArgMax();
            visit(current);

            using (var progress = new ProgressBar(allSlides.Count, "Find maximal path"))
            {
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
                    progress.Tick(visited.Count, $"bucket score: {score}");
                }
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
                var bucket = ExecuteCached(() =>
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
            using (var progress = new ProgressBar(pictures.Count, "Build adjacency matrix"))
            {
                var s = new byte[pictures.Count][];
                for (int i = 0; i < pictures.Count; i++)
                {
                    s[i] = new byte[pictures.Count];
                }

                int count = 0;

                Parallel.For(0, s.Length, i =>
                {
                    lock (this)
                    {
                        progress.Tick(++count);
                    }

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
    }
}