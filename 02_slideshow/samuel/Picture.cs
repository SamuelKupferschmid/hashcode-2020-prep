using System;
using System.Collections.Generic;

namespace SlideShow
{
    [Serializable]
    public class Picture
    {
        public bool IsVertical { get; set; }

        public int Index { get; set; }

        public HashSet<int> Tags { get; set; }
    }
}