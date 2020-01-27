﻿using System;
using System.IO;
using SolutionLibrary;

namespace Challenge
{
    class Program
    {
        static void Main(string[] args)
        {
            var runner = new Runner<T>(Path.Combine("..","..","..", ".."));
            runner.RunInteractive();
        }
    }
}