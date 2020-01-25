using System.IO;
using SolutionLibrary;

namespace SlideShow
{
    class Program
    {
        static void Main(string[] args)
        {
            var runner = new Runner<SlideShow>(Path.Combine("..","..","..", ".."));
            runner.RunInteractive();
        }
    }
}