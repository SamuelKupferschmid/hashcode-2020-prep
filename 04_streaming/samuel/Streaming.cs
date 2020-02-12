using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices.ComTypes;
using SolutionLibrary;

namespace Challenge
{
    public class Streaming : Solution
    {
        public override (int score, IList<string> output) Solve(string[] input)
        {
            var firstLine = input[0].Split(' ').Select(int.Parse).ToList();
            var videosCount = firstLine[0];
            var endpointCount = firstLine[1];
            var requestCount = firstLine[2];
            var cacheServerCount = firstLine[3];
            var cacheServerCapacity = firstLine[4];

            var videoSizes = input[0].SplitInts();
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

            //videos
            for (int i = 0; i < requestCount; i++)
            {
                var splits = input[rowIndex++].SplitInts();
                endPointVideoRequests[splits[1], splits[0]] = (short)splits[2];
            }

            var cacheVideos = Enumerable.Repeat(0, cacheServerCount).Select(_ => new HashSet<int>()).ToList();


            var cacheVideoScore = new short[cacheServerCount, videosCount];
            var result = new List<string>();
            var score = 0;

            for (int c = 0; c < cacheServerCount; c++)
            {
                for (int v = 0; v < videosCount; v++)
                {
                    
                }
            }

            result.Add(cacheVideos.Count.ToString());
            for (int i = 0; i < cacheVideos.Count; i++)
            {
                result.Add($"{i} {string.Join(' ', cacheVideos[i])}");
            }

            return (score, result);
        }
    }

    
}