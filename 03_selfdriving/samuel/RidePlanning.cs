using System;
using System.Collections.Generic;
using System.Drawing;
using System.Dynamic;
using System.Linq;
using SolutionLibrary;
using SolutionLibrary.Collections;

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

            var initialSchedule = Enumerable.Range(0, _vehicleCount)
                .Select(i => new Schedule
                {
                    VehicleIndex = i,
                    RideIndex = -1,
                    Cost = -1,
                });
            var queue = new PriorityQueue<Schedule>(initialSchedule,(a, b) => b.Cost - a.Cost);

            var assignedRides = new HashSet<int>();

            using (var progress = CreateProgressBar(_vehicleCount, "Assign Rides"))
            {

                while (queue.Any())
                {
                    var schedule = queue.Dequeue();

                    var endTime = vehicleEndTime[schedule.VehicleIndex];
                    var endPosition = vehicleEndPos[schedule.VehicleIndex];

                    if (schedule.RideIndex >= 0 && !assignedRides.Contains(schedule.RideIndex))
                    {
                        assignedRides.Add(schedule.RideIndex);
                        var ride = rides[schedule.RideIndex];
                        var arrTime = Math.Max(endTime + (endPosition.Distance(ride.StartPos)), ride.StartTime);

                        if (arrTime == ride.StartTime) score += _bonus;

                        score += ride.Distance;

                        endPosition = ride.StartPos;
                        endTime = arrTime + ride.Distance;

                        vehicleRides[schedule.VehicleIndex].Add(ride.Index);
                        progress.Tick(assignedRides.Count,score.ToString());
                    }

                    var minimalCost = int.MaxValue;
                    var bestRideIndex = -1;

                    for (int i = schedule.RideIndex + 1; i < _ridesCount; i++)
                    {
                        var ride = rides[i];
                        var distance = ride.StartPos.Distance(endPosition);

                        var buffer = ride.EndTime - ride.Distance;

                        if (endTime + distance > ride.StartTime + buffer) continue;

                        // optimal solution already found
                        if (minimalCost < ride.StartTime - endTime) break;

                        var cost = Math.Max(distance, ride.StartTime - endTime);
                        cost += -endTime * 100;

                        var earliestArrival = ride.EndTime + distance;
                        if (earliestArrival > ride.StartTime) cost += 10;

                        if (cost < minimalCost)
                        {
                            minimalCost = cost;
                            bestRideIndex = i;
                        }
                    }

                    if (bestRideIndex >= 0)
                    {
                        queue.Enqueue(new Schedule
                        {
                            VehicleIndex = schedule.VehicleIndex,
                            Cost = minimalCost,
                            RideIndex = bestRideIndex,
                        });
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

    public class Schedule
    {
        public int VehicleIndex { get; set; }
        public int RideIndex { get; set; }
        public int Cost { get; set; }
    }
}