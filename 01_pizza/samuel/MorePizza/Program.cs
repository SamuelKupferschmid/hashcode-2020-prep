using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace MorePizza
{
    class Program
    {
        static void Main(string[] args)
        {
            var files = Directory.GetFiles("in");

            foreach (var file in files)
            {
                var backtracking = new Backtrack(file);

                backtracking.Find();
            }
        }
    }

    public class Backtrack
    {
        private int bestSolution; // difference to optimal solution (0 == best)

        private readonly string _name; // filename without extension
        private readonly List<int> _pizzaSizes; 
        private readonly int _target; // maximum amount of slices

        public Backtrack(string inputFilename)
        {
            _name = Path.GetFileNameWithoutExtension(inputFilename);

            var values = File.ReadAllLines(inputFilename).Select(line => line.Split(' ')).ToList();
            _target = int.Parse(values[0][0]);
            _pizzaSizes = values[1].Select(int.Parse).ToList();

            bestSolution = _target;
        }

        public int Find()
        {
            // running backtracking starting with the bigges pizzas to find dead ends as soon as possible
            // first parameter indicates whitch pizzas we will order.
            Find(new bool[_pizzaSizes.Count], _pizzaSizes.Count - 1, _target);

            return bestSolution;
        }


        private void Find(bool[] orderedIndices, int index, int remaining)
        {
            if (bestSolution == 0)
            {
                
                return;
            }
            else if (index < 0)
            {
                if (remaining < bestSolution)
                {
                    bestSolution = remaining;
                    PrintSolution(orderedIndices);
                }
            }
            else
            {
                var size = _pizzaSizes[index];

                // if budged is left we try this branch
                if (remaining >= size)
                {
                    orderedIndices[index] = true;
                    Find(orderedIndices, index - 1, remaining - size);
                    orderedIndices[index] = false; // reset the index after we checked all combinations recursively
                }

                // check all solutions leaving this pizza out
                Find(orderedIndices, index - 1, remaining);
            }
        }

        private void PrintSolution(bool[] orderedIndices)
        {
            var slices = new List<int>();
            int sum = 0;

            for (int i = 0; i < _pizzaSizes.Count; i++)
            {
                if (orderedIndices[i])
                {
                    slices.Add(i);
                    sum += _pizzaSizes[i];
                }
            }

            Console.WriteLine(sum);

            var result = string.Join(' ', slices);

            File.WriteAllLines($"{_name}.out", new[] {slices.Count.ToString(), result});
        }
    }
}