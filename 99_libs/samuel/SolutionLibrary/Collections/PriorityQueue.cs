using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;

namespace SolutionLibrary.Collections
{
    public class PriorityQueue<T>
    {
        private readonly Comparison<T> _comparison;
        private readonly List<T> _innerList;

        public PriorityQueue(Comparison<T> comparison)
        {
            _comparison = comparison;

            //index 0 is unused for simpler handling of array
            _innerList = new List<T> { default(T) };
        }

        public PriorityQueue(IEnumerable<T> source, Comparison<T> comparison)
            : this(comparison)
        {
            foreach (var item in source)
                Enqueue(item);
        }

        public void Enqueue(T item)
        {
            _innerList.Add(item);
            Swim(_innerList.Count - 1);
        }

        public T Dequeue()
        {
            var item = Peek();

            _innerList[1] = _innerList[_innerList.Count - 1];

            Sink(1);

            _innerList.RemoveAt(_innerList.Count - 1);

            return item;
        }

        public T Peek()
        {
            return _innerList[1];
        }

        public bool IsEmpty => _innerList.Count == 1;

        private void Swim(int i)
        {
            while (i > 1 && IsLess(i / 2, i))
            {
                Swap(i, i / 2);
                i /= 2;
            }
        }

        private void Sink(int i)
        {
            var size = _innerList.Count - 1;

            var j = 2 * i;
            while (j <= size)
            {
                if (j < size && IsLess(j, j + 1))
                    j++;
                if (!IsLess(i, j))
                    break;
                Swap(i, j);
            }
        }

        private bool IsLess(int i1, int i2) => _comparison(_innerList[i1], _innerList[i2]) < 0;

        [MethodImpl(MethodImplOptions.AggressiveInlining)]
        private void Swap(int i1, int i2)
        {
            var tmp = _innerList[i1];
            _innerList[i1] = _innerList[i2];
            _innerList[i2] = tmp;
        }

        public bool Any()
        {
            return !IsEmpty;
        }
    }
}