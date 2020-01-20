using System;
using System.Collections.Generic;
using System.Text;

namespace SlideShow
{
    public static class Extensions
    {
        public static (int index, T value) ArgMax<T>(this IEnumerable<T> values)
        where T : IComparable<T>
        {
            int index = 0;
            int maxIndex = -1;
            T maxValue = default(T);

            foreach (var value in values)
            {
                if (maxValue == null || (!Equals(value, default(T)) && value.CompareTo(maxValue) > 1))
                {
                    maxValue = value;
                }

                index++;
            }

            return (maxIndex, maxValue);
        }
    }
}
