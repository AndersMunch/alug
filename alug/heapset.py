import itertools, heapq


class HeapSet:
    """!
    @brief Heap with efficient deletion and a key function option.
    """
    def __init__(self, elements, key=None):
        """!
        @param[in] elements	Sequence of hashable elements.
        @param[in] key		Derives
        """
        if key is None:
            self._decorate = lambda ele: ele
            self._undecorate = lambda dec: dec
        else:
            counter = iter(itertools.count())
            self._decorate = lambda ele: (key(ele), next(counter), ele)
            self._undecorate = lambda dec: dec[-1]
        self._has_key_function = key is not None
        self._heap_of_decs = list(map(self._decorate, elements))
        self._ele_to_dec = dict(zip(elements, self._heap_of_decs))
        heapq.heapify(self._heap_of_decs)
        assert len(self._heap_of_decs) == len(self._ele_to_dec) # ensures that 'elements' are re-iterable.

    def push(self, ele):
        if ele in self._ele_to_dec:
            raise KeyError('already on heap')
        dec = self._decorate(ele)
        self._ele_to_dec[ele] = dec
        heapq.heappush(self._heap_of_decs, dec)

    def pop(self):
        while 1:
            dec = heapq.heappop(self._heap_of_decs)
            ele = self._undecorate(dec)
            if ele in self._ele_to_dec and dec is self._ele_to_dec[ele]:
                del self._ele_to_dec[ele]
                return ele

    def discard(self, ele):
        # Deletes from _ele_to_dec but not _heap_of_decs.
        # Works only because pop/discard/peek doublechecks heappop results against _ele_to_dec also.
        # Deleted elements remain in _heap_of_decs until that happens.
        try:
            del self._ele_to_dec[ele]
        except KeyError:
            pass

    def __delitem__(self, ele):
        del self._ele_to_dec[ele]

    def peek(self):
        while 1:
            dec = heapq.heappop(self._heap_of_decs)
            ele = self._undecorate(dec)
            if ele in self._ele_to_dec and dec is self._ele_to_dec[ele]:
                heapq.heappush(self._heap_of_decs, dec)
                return res

    def recompute_key(self, ele):
        """!
        @brief Notify that the priority, as computed by the key function, has changed.
        For this to work, the key function must return a different object for different priorities.
        The key objects themselves (as returned by the key function) must not change sort order
        during the lifetime of the HeapSet.
        """
        # Basically discard+push, except a no-op if the element is not in the HeapSet.
        assert self._has_key_function
        try:
            del self._ele_to_dec[ele]
        except KeyError:
            pass
        else:
            self.push(ele)

    def __len__(self):
        return len(self._ele_to_dec)

    def pop_all(self):
        try:
            while 1:
                yield self.pop()
        except IndexError:
            pass

    def __iter__(self):
        heap = self._heap_of_decs.copy()
        decs = self._ele_to_dec.copy()
        while heap:
            dec = heapq.heappop(heap)
            ele = self._undecorate(dec)
            if ele in decs and dec is decs[ele]:
                yield ele

    def __bool__(self):
        return len(self) > 0

    def __contains__(self, ele):
        return ele in self._ele_to_dec
