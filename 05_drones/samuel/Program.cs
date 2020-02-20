using System;
using System.Collections.Generic;
using System.Drawing;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Reflection.Metadata.Ecma335;
using SolutionLibrary;
using SolutionLibrary.Collections;

namespace Challenge
{
    class Program
    {
        static void Main(string[] args)
        {
            var runner = new Runner<Drones>(Path.Combine("..","..","..", ".."));
            runner.RunInteractive();
        }

        public class Drones : Solution
        {
            public override (int score, IList<string> output) Solve(string[] input)
            {
                var ints = input[0].SplitInts();
                var rowCount = ints[0];
                var colCount = ints[1];
                var droneCount = ints[2];
                var stepsCount = ints[3];
                var maxLoad = ints[4];

                var line = 1;

                // products
                var prodCount = int.Parse(input[line++]);
                var prodWeights = input[line++].SplitInts();

                // warehouses
                var whCount = int.Parse(input[line++]);
                var whPositions = new Point[whCount];
                var whProdStock = new short[whCount, prodCount];

                for (int i = 0; i < whCount; i++)
                {
                    var pos = input[line++].SplitInts();
                    whPositions[i] = new Point(pos[0], pos[1]);
                    var stock = input[line++].SplitInts();
                    for (int j = 0; j < prodCount; j++)
                    {
                        whProdStock[i, j] = (short)stock[j];
                    }
                }

                // orders
                var orderCount = int.Parse(input[line++]);
                var orderPositions = new Point[orderCount];

                var orderItemsCount = new short[orderCount, prodCount];
                for (int i = 0; i < orderCount; i++)
                {
                    var pos = input[line++].SplitInts();
                    orderPositions[i] = new Point(pos[0], pos[1]);
                    var itemsCount = int.Parse(input[line++]);
                    foreach (var item in input[line++].SplitInts())
                    {
                        orderItemsCount[i, item]++;
                    }
                }

                var size = prodCount + whCount;
                var distances = new short[size, size];

                for (int row = 0; row < size; row++)
                {
                    for (int col = row + 1; col < size; col++)
                    {
                        var pos1 = row < whCount ? whPositions[row] : orderPositions[row - whCount];
                        var pos2 = col < whCount ? whPositions[col] : orderPositions[col - whCount];
                        var dist = (short)Math.Ceiling(Math.Sqrt(Math.Pow(pos1.X - pos2.X, 2) + Math.Pow(pos1.Y - pos2.Y, 2)));
                        distances[row, col] = dist;
                        distances[col, row] = dist;
                    }
                }

                var queue = new PriorityQueue<Order>( Enumerable.Range(0, orderCount).Select(i => new Order {Index = i, Cost = int.MaxValue}), 
                    (order1, order2) => order1.Cost - order2.Cost);

                while (queue.Any())
                {
                    var order = queue.Dequeue();

                    //if valid handle id

                    // else recalculate

                }
                return (0, new List<string>());
            }
        }

        public class Order
        {
            public int Index { get; set; }

            public int Cost { get; set; }


        }
    }
}
