import unittest, random, sys, os
sys.path.insert(0, os.path.join(os.path.split(__file__)[0], '..'))
from alug.heapset import HeapSet


class Test_HeapSet(unittest.TestCase):
    def setUp(self):
        ele = list(range(16))
        self._h = HeapSet(
            ele,
            key=lambda n: (n%4, n%8, n),
            )

    def test_iter_and_pop_all(self):
        orig_len = len(self._h)
        res1 = list(self._h)
        res2 = list(self._h)
        self.assertEqual(
            res1,
            [0, 8, 4, 12, 1, 9, 5, 13, 2, 10, 6, 14, 3, 11, 7, 15]
            )
        self.assertEqual(res1, res2)
        self.assertEqual(len(self._h), orig_len)

        res3 = list(self._h.pop_all())
        self.assertEqual(res2, res3)
        self.assertEqual(len(self._h), 0)
        self.assertEqual(list(self._h), [])

    def test_discard(self):
        h = HeapSet([4,1,3,2])
        self.assertEqual(h.pop(), 1)
        h.discard(3)
        self.assertEqual(h.pop(), 2)
        self.assertEqual(h.pop(), 4)

    def test_discard_all(self):
        elements = ["a", "bb", "aaa", "bbbb"]
        h = HeapSet(elements, key=len)
        for e in elements:
            h.discard(e)
        self.assertRaises(IndexError, h.pop)

    def test_random(self):
        have = set()
        h = HeapSet([])
        for _ in range(100):
            x = random.randrange(-100, 100)
            if x < 0:
                x = -x
                have.discard(x)
                h.discard(x)
            else:
                self.assertEqual(x in h, x in have)
                if x not in have:
                    have.add(x)
                    h.push(x)

        rest = list(h.pop_all())
        self.assertEqual(set(rest), have)

        for i in range(len(rest)-1):
            self.assertTrue(rest[i] < rest[i+1])


    def test_priority_change(self):
        overrides = dict()
        def key(x):
            try:
                return overrides[x]
            except KeyError:
                return x
        elements = list(range(0, 14, 2))
        h = HeapSet(elements, key=key)
        self.assertEqual(h.pop(), 0)
        h.discard(8)
        overrides[8] = 3
        h.push(8)
        h.discard(2)
        overrides[2] = 11
        h.push(2)
        h.discard(6)
        self.assertEqual(list(h), [8, 4, 10, 2, 12])

if __name__=='__main__':
    unittest.main()
