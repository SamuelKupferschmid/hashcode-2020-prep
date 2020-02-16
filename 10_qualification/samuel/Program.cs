using System;
using System.Collections.Generic;
using System.IO;
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
            public override (int score, IList<string> output) Solve(string[] input)
            {
                throw new NotImplementedException();
            }
        }
    }
}
