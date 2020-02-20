using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Runtime.Intrinsics.X86;
using SolutionLibrary;
using SolutionLibrary.Collections;

namespace Challenge
{
    class Program
    {
        static void Main(string[] args)
        {
            var runner = new Runner<BookScanning>(Path.Combine("..","..","..", ".."));
            runner.RunInteractive();
        }

        public class BookScanning : Solution
        {
            public readonly Configuration Config;

            public BookScanning()
            {
                Config = new Configuration
                {
                    SignupScoreDay = 5
                };
            }

            public override (int score, IList<string> output) Solve(string[] input)
            {
                // read input
                var lineIndex = 0;

                var ints = input[lineIndex++].SplitInts();
                var bookCount = ints[0];
                var libCount = ints[1];
                var days = ints[2];

                //var libBooks = new short[libCount, bookCount];
                //return (0, new List<string>());

                var books = input[lineIndex++].SplitInts().Select((val, index) => new Book { Index = index, Score = val}).ToList();

                var unscannedLibBooks = new HashSet<int>[libCount];
                var libSignupDays = new int[libCount];
                var libRentLimit = new int[libCount];

                var booksLibraries = books.Select(_ => new List<Library>()).ToList();
                

                var libraries = new List<Library>();

                double BookScore(Book b)
                {
                    return b.Score * b.Rarity * b.Rarity;
                }

                for (int i = 0; i < libCount; i++)
                {
                    ints = input[lineIndex++].SplitInts();

                    var libBooks = input[lineIndex++].SplitInts().Select(index => books[index]).ToList();

                    var booksQueue = new PriorityQueue<Book>(libBooks, (b1, b2) => (int) (BookScore(b1) - BookScore(b2)));

                    var lib = new Library
                    {
                        Id = i,
                        SignupDays = ints[1],
                        RentLimit = ints[2],
                        Books = booksQueue,
                        SignupScore = -1
                    };

                    foreach (var book in libBooks)
                    {
                        lib.ScoreSum += book.Score;
                        booksLibraries[book.Index].Add(lib);
                    }


                    libraries.Add(lib);
                }

                for (int i = 0; i < bookCount; i++)
                {
                    books[i].Rarity = (double)libCount / booksLibraries[i].Count;
                }

                PriorityQueue<Library> signupQueue = new PriorityQueue<Library>(libraries, (library1, library2) =>  (library1.SignupScore.CompareTo(library2.SignupScore)));

                var signedLibs = new List<Library>();
                var scannedBooks = new HashSet<Book>();

                var lastSignupCompletedAt = 0;

                var score = 0;

                void ValidateQueue(PriorityQueue<Library> queue)
                {
                    while (true)
                    {
                        var lib = queue.Peek();

                        var score = lib.ScoreSum / (double)lib.SignupDays;

                        if (score != lib.SignupScore)
                        {
                            queue.Dequeue();
                            lib.SignupScore = score;
                            queue.Enqueue(lib);
                        }
                        else
                        {
                            break;
                        }
                    }
                }

                for (int day = 0; day < days; day++)
                {
                    // signup libraries
                    if (lastSignupCompletedAt <= day && signupQueue.Any())
                    {
                        ValidateQueue(signupQueue);
                        var next = signupQueue.Dequeue();

                        lastSignupCompletedAt = day + next.SignupDays;
                        next.SignupCompleteAt = lastSignupCompletedAt;

                        signedLibs.Add(next);

                        
                    }


                    //ship books
                    foreach (var lib in signedLibs.Where(l => l.SignupCompleteAt < day))
                    {
                        var remaining = lib.RentLimit;
                        while (remaining-- > 0 && lib.Books.Any())
                        {
                            var book = lib.Books.Dequeue();
                            
                            if (!scannedBooks.Contains(book))
                            {
                                foreach (var l in booksLibraries[book.Index])
                                {
                                    l.ScoreSum -= book.Score;
                                }

                                scannedBooks.Add(book);
                                lib.Scanned.Add(book);
                                score += book.Score;
                            }
                        }
                    }

                }

                
                var resultLines = new List<string>();

                signedLibs = signedLibs.Where(l => l.SignupCompleteAt <= days && l.Scanned.Any()).ToList();

                resultLines.Add(signedLibs.Count.ToString());

                foreach (var signedLib in signedLibs)
                {
                    resultLines.Add(string.Join(' ', signedLib.Id, signedLib.Scanned.Count));
                    resultLines.Add(string.Join(' ', signedLib.Scanned.Select(b => b.Index)));
                }

                return (score, resultLines);
            }
        }

        public class Library
        {
            public int Id { get; set; }
            public int SignupDays { get; set; }
            public double SignupScore { get; set; }

            public int ScoreSum { get; set; }

            public int SignupCompleteAt { get; set; }

            public PriorityQueue<Book> Books { get; set; }

            public List<Book> Scanned { get; set; } = new List<Book>();

            public int BooksValue { get; set; }
            public int RentLimit { get; set; }
        }

        public class Book
        {
            public int Index { get; set; }

            public int Score { get; set; }

            public double Rarity { get; set; }
        }

        public class Configuration
        {
            public int SignupScoreDay { get; set; }
        }
    }
}
