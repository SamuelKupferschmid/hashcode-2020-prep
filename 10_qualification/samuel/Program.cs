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

                var books = input[lineIndex++].SplitInts().Select((val, index) => new Book {Index = index, Score = val})
                    .ToList();

                var unscannedLibBooks = new HashSet<int>[libCount];
                var libSignupDays = new int[libCount];
                var libRentLimit = new int[libCount];

                var booksLibraries = books.Select(_ => new List<Library>()).ToList();


                var libraries = new List<Library>();

                double BookScore(Book b)
                {
                    return b.Score * b.Rarity * b.Rarity;
                }

                var booksQueue = new PriorityQueue<Book>(books, (b1, b2) => (int) (BookScore(b1) - BookScore(b2)));

                for (int i = 0; i < libCount; i++)
                {
                    ints = input[lineIndex++].SplitInts();

                    var libBooks = input[lineIndex++].SplitInts().Select(index => books[index]).ToList();



                    var lib = new Library
                    {
                        Id = i,
                        SignupDays = ints[1],
                        RentLimit = ints[2],
                        Books = libBooks.ToHashSet(),
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
                    books[i].Rarity = (double) libCount / booksLibraries[i].Count;
                }

                PriorityQueue<Library> signupQueue = new PriorityQueue<Library>(libraries,
                    (library1, library2) => (library1.SignupScore.CompareTo(library2.SignupScore)));

                var signedLibs = new List<Library>();
                var scannedBooks = new HashSet<Book>();

                var lastSignupCompletedAt = 0;

                var score = 0;

                void ValidateQueue(PriorityQueue<Library> queue)
                {
                    while (true)
                    {
                        var lib = queue.Peek();

                        var score = lib.ScoreSum / (double) lib.SignupDays;

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


                using (var p = CreateProgressBar(days, "Days..."))
                {

                    for (int day = 0; day < days; day++)
                    {
                        p.Tick(day, score.ToString());
                        // signup libraries
                        if (lastSignupCompletedAt <= day && signupQueue.Any())
                        {
                            ValidateQueue(signupQueue);
                            var next = signupQueue.Dequeue();

                            lastSignupCompletedAt = day + next.SignupDays;
                            next.SignupCompleteAt = lastSignupCompletedAt;

                            signedLibs.Add(next);


                        }

                        var dailyShipment = signedLibs.Where(l => l.SignupCompleteAt <= day).Select(l => new Shipment
                        {
                            RemainingSpace = l.RentLimit,
                            Library = l
                        }).ToList();

                        var invalidBooks = new List<Book>();

                        while (dailyShipment.Any() && booksQueue.Any())
                        {
                            var book = booksQueue.Dequeue();
                            var maxIndex = -1;
                            var maxRemaining = 0;

                            for (int lib = 0; lib < dailyShipment.Count; lib++)
                            {
                                if (dailyShipment[lib].Library.Books.Contains(book))
                                {
                                    if (dailyShipment[lib].RemainingSpace > maxRemaining)
                                    {
                                        maxIndex = lib;
                                        maxRemaining = dailyShipment[lib].RemainingSpace;
                                    }
                                }
                            }

                            //in no library at the moment
                            if (maxIndex == -1)
                            {
                                invalidBooks.Add(book);
                            }
                            else
                            {
                                var shipment = dailyShipment[maxIndex];
                                shipment.RemainingSpace--;
                                shipment.Library.Scanned.Add(book);
                                score += book.Score;

                                if (shipment.RemainingSpace == 0)
                                {
                                    dailyShipment.RemoveAt(maxIndex);
                                }
                                else if (shipment.RemainingSpace < 0)
                                {

                                }
                            }
                        }

                        foreach (var invalidBook in invalidBooks)
                        {
                            booksQueue.Enqueue(invalidBook);
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
        }

        public class Shipment
        {
            public int RemainingSpace { get; set; }

            public Library Library { get; set; }
        }

        public class Library
        {
            public int Id { get; set; }
            public int SignupDays { get; set; }
            public double SignupScore { get; set; }

            public int ScoreSum { get; set; }

            public int SignupCompleteAt { get; set; }

            public HashSet<Book> Books { get; set; }

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
