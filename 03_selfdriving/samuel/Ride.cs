using System;
using System.Drawing;

namespace Challenge
{
    [Serializable]
    public class Ride
    {
        public int Index { get; set; }
        public Point StartPos { get; set; }
        public Point EndPos { get; set; }
        public int StartTime { get; set; }
        public int EndTime { get; set; }

        public int Duration => EndTime - StartTime;

        public int Distance => EndPos.Distance(StartPos);
    }
}