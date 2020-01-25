using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Runtime.Serialization.Formatters.Binary;

namespace SolutionLibrary
{
    public abstract class Solution
    {
        public string Filename { get; set; }

        public abstract (int score, IList<string> output) Solve(string[] input);

        protected T ExecuteCached<T>(Func<T> func, string name)
        {
            Directory.CreateDirectory(Path.GetFileNameWithoutExtension(Filename));
            var formatter = new BinaryFormatter();
            T result = default(T);

            name = $"{Path.GetFileNameWithoutExtension(Filename)}/{name}";

            if (File.Exists(name))
            {
                
                using var s = File.OpenRead(name);
                try
                {
                    result = (T) formatter.Deserialize(s);
                    Console.WriteLine($"loading ExecuteCached: {name} [{s.Length / 1024 / 1024} MByte]");
                    return result;
                }
                catch
                {
                }
            }

            Console.WriteLine($"Executing: {name}");
            result = func();

            using var stream = File.OpenWrite(name);
            formatter.Serialize(stream, result);
            Console.WriteLine($"writing ExecuteCached: {name} [{stream.Length / 1024 / 1024} MByte]");
            return result;
        }
    }
}
