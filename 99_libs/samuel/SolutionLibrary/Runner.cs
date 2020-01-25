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
            var inputFiles = Directory.GetFiles(Path.Combine(_rootPath, "input"));

            while (true)
            {
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
                        RunDataset(file);
                    }
                }
                else
                {
                    RunDataset(inputFiles[key-1]);
                }
            }
        }

        public void RunDataset(string inputFilePath)
        {
            var solution = new T {Filename = inputFilePath};
            var filename = Path.GetFileName(inputFilePath);

            var input = File.ReadAllLines(inputFilePath);
            Console.WriteLine($"Start solving {filename} [{input.Length} lines]");

            var outputFolder = Path.Combine(_rootPath, "output");

            var bestOutput = Directory.GetFiles(outputFolder).FirstOrDefault(f =>
                                 Path.GetFileName(f).StartsWith(Path.GetFileNameWithoutExtension(filename))) ?? "0_x";

            var split = bestOutput.Split('_');
            var maxScore = int.Parse(split[split.Length - 2]);
            var sw = Stopwatch.StartNew();
            var (score, output) = solution.Solve(input);

            File.WriteAllLines(Path.Combine(outputFolder, $"{Path.GetFileNameWithoutExtension(filename)}_{score}_samuel"), output);

            var diff = score - maxScore;
            
            Console.ForegroundColor = diff > 0 ? ConsoleColor.Green : ConsoleColor.Red;
            Console.WriteLine($"score: {score} [{(diff > 0 ? "+" : "-")}{diff}] in {sw.ElapsedMilliseconds / 1000} seconds");
            Console.WriteLine(new string('=', 50));
            Console.ResetColor();
        }
    }
}
