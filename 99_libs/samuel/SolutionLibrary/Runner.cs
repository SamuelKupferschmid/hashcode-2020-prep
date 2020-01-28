using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;

namespace SolutionLibrary
{
    public class Runner<T>
    where T : Solution, new()
    {
        private readonly string _rootPath;

        public Runner(string rootPath)
        {
            _rootPath = rootPath;
        }


        public void RunInteractive()
        {
            while (true)
            {
                var inputFiles = Directory.GetFiles(Path.Combine(_rootPath, "input"));
                var totalMaxScore = 0;

                Console.WriteLine("Select Dataset:");
                Console.WriteLine("0: Run all");
                for (var i = 0; i < inputFiles.Length; i++)
                {
                    Console.WriteLine($"{i+1}: Run {Path.GetFileName(inputFiles[i])}");
                }

                var key = int.Parse(Console.ReadKey().KeyChar.ToString());
                Console.WriteLine();
                if (key == 0)
                {
                    foreach (var file in inputFiles)
                    {
                        totalMaxScore += RunDataset(file);
                    }
                }
                else
                {
                    totalMaxScore += RunDataset(inputFiles[key-1]);
                }

                Console.WriteLine($"Total Max Score: {totalMaxScore:N0}");
                Console.WriteLine();
            }
        }

        public int RunDataset(string inputFilePath)
        {
            var solution = new T {Filename = inputFilePath};
            var filename = Path.GetFileName(inputFilePath);

            var input = File.ReadAllLines(inputFilePath);
            Console.WriteLine($"Start solving {filename} [{input.Length} lines]");

            var outputFolder = Path.Combine(_rootPath, "output");

            var bestOutput = Directory.GetFiles(outputFolder)
                .Where(f => Path.GetFileName(f).StartsWith(Path.GetFileNameWithoutExtension(filename)))
                .Select(s => s.Split('_'))
                .Select(split => int.Parse(split[split.Length - 2]))
                .Concat(new []{0})
                .Max();

            var maxScore = bestOutput;
            var sw = Stopwatch.StartNew();
            var (score, output) = solution.Solve(input);

            var diff = score - maxScore;

            if (diff > 0)
            {
                File.WriteAllLines(Path.Combine(outputFolder, $"{Path.GetFileNameWithoutExtension(filename)}_{score}_samuel"), output);
            }


            Console.ForegroundColor = diff > 0 ? ConsoleColor.Green : ConsoleColor.Red;
            Console.WriteLine($"score: {score:N0} [{(diff > 0 ? "+" : "-")}{diff:N0}] in {sw.ElapsedMilliseconds / 1000} seconds");
            Console.WriteLine(new string('=', 50));
            Console.ResetColor();
            maxScore = Math.Max(score, maxScore);
            return maxScore;
        }
    }
}
