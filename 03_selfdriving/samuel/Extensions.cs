using System;
using System.Drawing;

namespace Challenge
{
    public static class Extensions
    {
        public static int Distance(this Point a, Point b) => Math.Abs(a.X - b.X) + Math.Abs(a.Y - b.Y);
    }
}