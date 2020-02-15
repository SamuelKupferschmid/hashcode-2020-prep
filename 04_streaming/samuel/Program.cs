using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using SolutionLibrary;
using SolutionLibrary.Extensions;

namespace Challenge
{
    class Program
    {
        static void Main(string[] args)
        {
            var runner = new Runner<RandomAssign>(Path.Combine("..","..","..", ".."));
            runner.RunInteractive();
        }

        public class RandomAssign: Solution
        {
             public override (int score, IList<string> output) Solve(string[] input)
        {
            var firstLine = input[0].Split(' ').Select(int.Parse).ToList();
            var videosCount = firstLine[0];
            var endpointCount = firstLine[1];
            var requestCount = firstLine[2];
            var cacheServerCount = firstLine[3];
            var cacheServerCapacity = firstLine[4];

            var videoSizes = input[1].SplitInts();
            var serverCapacities = Enumerable.Repeat(cacheServerCapacity, cacheServerCount).ToList();

            var endPointCacheLatencyBenefit = new short[endpointCount, cacheServerCount];
            var endPointVideoRequests = new short[endpointCount, videosCount];

            // endpoints
            var rowIndex = 2;
            for (int i = 0; i < endpointCount; i++)
            {
                var split = input[rowIndex++].SplitInts();
                var datacenterLatency = split[0];
                var connectionsCount = split[1];

                for (int j = 0; j < connectionsCount; j++)
                {
                    split = input[rowIndex++].SplitInts();
                    var index = split[0];
                    var cacheLatency = split[1];
                    endPointCacheLatencyBenefit[i, index] = (short)(datacenterLatency - cacheLatency);
                }
            }

            var requestsTotal = 0;
            var videoRequests = new int[videosCount];

            //videos
            for (int i = 0; i < requestCount; i++)
            {
                var splits = input[rowIndex++].SplitInts();

                requestsTotal += splits[2];
                endPointVideoRequests[splits[1], splits[0]] = (short)splits[2];
                videoRequests[splits[0]] += splits[2];
            }

            var cacheVideos = Enumerable.Repeat(0, cacheServerCount).Select(_ => new HashSet<int>()).ToList();

            var totalCapaity = cacheServerCapacity * cacheServerCount;

            var rand = new Random();
            var watchdog = 1000;

            while (totalCapaity > 0)
            {
                // instead of uniform distribution i pick a random value relative to the amount of request of a video
                // and available space of a cache server
                int cacheIndex = serverCapacities.GetRandomIndexByDistribution(totalCapaity);
                int videoIndex = videoRequests.GetRandomIndexByDistribution(requestsTotal);

                if (!cacheVideos[cacheIndex].Contains(videoIndex) &&
                    videoSizes[videoIndex] <= serverCapacities[cacheIndex])
                {
                    var size = videoSizes[videoIndex];
                    totalCapaity -= size;
                    serverCapacities[cacheIndex] -= size;
                    cacheVideos[cacheIndex].Add(videoIndex);
                    watchdog = 1000;
                }
                else if(--watchdog < 0){break;}
            }

            var result = new List<string>();
            var score = 0L;

            for (int e = 0; e < endpointCount; e++)
            {
                for (int v = 0; v < videosCount; v++)
                {
                    var vidReqs = endPointVideoRequests[e, v];

                    if (vidReqs > 0)
                    {
                        // find best endpoint
                        var latencyBenefit = 0;
                        for (int c = 0; c < cacheServerCount; c++)
                        {
                            if (cacheVideos[c].Contains(v))
                            {
                                latencyBenefit = Math.Max(latencyBenefit, endPointCacheLatencyBenefit[e, c]);
                            }
                        }

                        score += vidReqs * latencyBenefit;
                    }
                }
            }

            score = (int)((double)score * 1000 / requestsTotal);

            result.Add(cacheVideos.Count.ToString());
            for (int i = 0; i < cacheVideos.Count; i++)
            {
                result.Add($"{i} {string.Join(' ', cacheVideos[i])}");
            }

            return ((int)score, result);
        }
        }
    }
}
