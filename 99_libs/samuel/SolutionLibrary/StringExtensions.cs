using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace SolutionLibrary
{
    public static class StringExtensions
    {
        public static List<int> SplitInts(this string text) => text.Split(' ').Select(int.Parse).ToList();
    }
}
