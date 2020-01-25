using System;

namespace SlideShow
{
    [Serializable]
    public class CombinedPicture : Picture
    {
        public Picture Left { get; set; }
        public Picture Right { get; set; }
    }
}