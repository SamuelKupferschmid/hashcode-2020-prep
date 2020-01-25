using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using SolutionLibrary;

namespace Challenge
{
    public class RidePlanning : Solution
    {
        private int _rowCount;
        private int _stepsCount;
        private int _colCount;
        private int _vehicleCount;
        private int _ridesCount;
        private int _bonus;

        public override (int score, IList<string> output) Solve(string[] input)
        {
            var splits = input[0].Split(' ');

            _rowCount = int.Parse(splits[0]);
            _colCount = int.Parse(splits[1]);
            _vehicleCount= int.Parse(splits[2]);
            _ridesCount = int.Parse(splits[3]);
            _bonus = int.Parse(splits[4]);
            _stepsCount = int.Parse(splits[5]);

            var rides = ExecuteCached(() =>
            {
                return input
                    .Skip(1)
                    .Select(l => l.Split(" ").Select(int.Parse).ToArray())
                    .Select((s, i) => new Ride
                    {
                        Index = i,
                        StartPos = new Point(s[0], s[1]),
                        EndPos = new Point(s[2], s[3]),
                        StartTime = s[4],
                        EndTime = s[5]
                    })
                    .OrderBy(r => r.StartTime)
                    .ToList();
            }, "Rides");

            int position = 0;
            int score = 0;

            var vehicleRides = new List<int>[_vehicleCount];

            var vehicleEndPos = new Point[_vehicleCount];
            var vehicleEndTime = new int[_vehicleCount];

            for(int i = 0; i < _vehicleCount;i++) vehicleRides[i] = new List<int>();

            foreach (var ride in rides)
            {
                var buffer = ride.Duration - ride.Distance;
                for (int i = 0; i < _vehicleCount; i++)
                {
                    var vehDist = ride.StartPos.Distance(vehicleEndPos[i]);
                    var delay = vehDist - vehicleEndTime[i] - ride.StartTime;
                    if (delay >= 0 && delay <= buffer)
                    {
                        score += ride.Distance;
                        vehicleEndPos[i] = ride.EndPos;
                        vehicleEndTime[i] = ride.StartTime + delay + ride.Distance;

                        if(delay <= 0) score += _bonus;
                        break;
                    }
                }
            }

            var output = new List<string>();

            foreach (var vehicle in vehicleRides)
            {
                output.Add(vehicle.Count + " " + string.Join(' ', vehicle));
            }

            return (score, output);
        }
    }

    public static class Extensions
    {
        public static int Distance(this Point a, Point b) => Math.Abs(a.X - b.X) + Math.Abs(a.Y - b.Y);
    }
}