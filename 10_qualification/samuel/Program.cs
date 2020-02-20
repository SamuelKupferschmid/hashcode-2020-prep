using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;
using SolutionLibrary;

namespace Challenge
{
    class Program
    {
        static void Main(string[] args)
        {
            var runner = new Runner<Qualification>(Path.Combine("..","..","..", ".."));
            runner.RunInteractive();
        }

        public class Qualification : Solution
        {
            public readonly Configuration Config;

            public Qualification()
            {
                Config = new Configuration
                {

                };
            }

            public override (int score, IList<string> output) Solve(string[] input)
            {
                // read input
                var lineIndex = 0;

                var ints = input[lineIndex++].SplitInts();
                var rowCount = ints[0];
                var colCount = ints[1];
                var droneCount = ints[2];
                var stepsCount = ints[3];
                var maxLoad = ints[4];


                var score = 0;
                var resultLines = new List<string>();


                return (score, resultLines);
            }
        }

        public class Configuration
        {

        }
    }
}
