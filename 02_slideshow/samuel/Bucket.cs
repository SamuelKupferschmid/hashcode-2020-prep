using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace SlideShow
{
    [Serializable]
    public class Bucket
    {
        public List<Picture> HorizontalSlides { get; set; }
        public List<CombinedPicture> VerticalSlides { get; set; }

        public IEnumerable<Picture> GetSlides() => HorizontalSlides.Concat(VerticalSlides);

        public byte[][] AdjacencyMatrix;
    }
}
