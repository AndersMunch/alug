alug
'''''

A small Python algorithms and data structures library.

* ``alug.heapset.HeapSet``: A priority queue with support for early deletion and priority change.
* ``alug.topo.semi_topological_sort``: Topological sorting that works even in the face of cycles.

heapset.HeapSet
===============

The `HeapSet` class in the alug.heapset module is a priority queue built on
`heapq`, which offers two main features beyond what `heapq` can do:

 * A `key` function can be set to extract the priority.
 * Items in queue can be deleted from the queue.
 * Items in queue can change priority (with some care).

If an item in a HeapSet object changes so that the `key` function would return a
different value for the item than it did before, then the heapset must be
notified using `recompute_key`.
   
Methods
+++++++

`__init__(self, elements, key=None)`
------------------------------------
Create a HeapSet with initial elements from the iterable `elements`.

The `key` function takes an element parameter and returns a priority.  A
priority is usually a number, but anything equality comparable is valid.

Elements must be hashable and equality comparable.

`push(self, ele)`
-----------------
Add an element to the heapset.

The element must be hashable and equality comparable. `KeyError` is raised if it's already in the heapset.

`pop(self) -> object`
---------------------
Extract the lowest-priority element from the heapset.


`__delitem__(self, ele)`
------------------------
Deletes the element from the heapset.

The heapset may still keep a reference to the element for a while, but it will never be returned from `pop`.
That is, unless the element is readded

`discard(self, ele)`
--------------------
Deletes the element from the heapset if the element is in the heapset. Otherwise, does nothing.

`peek(self) -> object`
----------------------
Fetch the element that would have been returned on the next `pop`.

`recompute_key(self, ele)`
--------------------------
Notify the heapset that this element has changed priority.

`__len__(self) -> int`
----------------------
Returns count of elements.

`pop_all(self) -> iterator`
---------------------------
An iterator of all elements in the heapset in priority order, extracted as they go.

`__iter__(self) -> iterator`
----------------------------
An iterator of all elements in the heapset in priority order. Doesn't change the heapset.

`__bool__(self) -> bool`
------------------------

`__contains__(self, ele) -> bool`
---------------------------------
Checks if the element is in the heapset.

topo module
===========

Functions
+++++++++

`topo.stable_topological_sort(items, partial_order) -> list`
------------------------------------------------------------
A mostly stable topological sort.

`items` is an iterable of the objects to be sorted. The objects must be hashable and equality comparable.

`partial_order` is a list of `(before,after)` constraint tuples, expressing that
the `after` object should come after the `before` object in the result.

If there are no cycles in partial_order, then a topological ordering of `items` is returned.
If cycles are found, then `topo.CycleError` is raised.

The sort is mostly stable, which means that the order of objects in `items` is
preserved as much as possible in the result.

`topo.semi_topological_sort(items, partial_order) -> list`
----------------------------------------------------------
A mostly stable topological sort that does not error out if there are cycles,
but instead returns something close to a topological sort of the input.

`items` is an iterable of the objects to be sorted. The objects must be hashable and equality comparable.

`partial_order` is a list of `(before,after)` constraint tuples, expressing that
the `after` object should come after the `before` object in the result.

If there are no cycles in partial_order, then a topological ordering of `items`
is returned.
If cycles are found, then a reordering that satisfies the input constraints to a
reasonable approximation is returned.

The sort is mostly stable, which means that the order of objects in `items` is
preserved as much as possible in the result.

License and credits
===================
alug is copyright Flonidan A/S (https://www.flonidan.dk/) and released under the MIT license.

Written by Anders Munch (ajm@flonidan.dk).

`semi_topological_sort` is based on Magma's answer to
https://stackoverflow.com/questions/57293426/topological-sort-with-loops
which is based on Eades, Lin, and Smyth [1993]: 'A fast and effective heuristic for the feedback arc set problem'.
