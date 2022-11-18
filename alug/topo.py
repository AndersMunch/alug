import random, operator
from .heapset import HeapSet


class CycleError(ValueError):
    pass

class _TopoNode:
    __slots__ = ['ix', 'ins', 'outs', 'label']
    def __init__(self, ix, label):
        self.ix = ix
        self.label = label
        self.ins = set()
        self.outs = set()
    def __lt__(self, other):
        return self.ix < other.ix
    def __eq__(self, other):
        return self.ix == other.ix
    def __hash__(self):
        return self.ix
    def __repr__(self):
        if self.ins is None:
            return '<Node %s (dead)>' % (self.label,)
        else:
            return '<Node %s: in=%r,out=%r>' % (self.label,len(self.ins),len(self.outs))


def semi_topological_sort(items, partial_order):
    """!
    @brief Cycle-tolerant stable-ish topological sort.
    @param[in] items		An iterable of hashable elements to sort.
    @param[in] partial_order	List of (before,after) dependencies prescribing that the 'before' node should
                                precede the 'after' node in the result.
    @return list of items in the specified order.

    If there are no cycles in partial_order, then a topological ordering is returned.
    If there are cycles, then a good approximation to a topological ordering is returned.

    Based on https://stackoverflow.com/questions/57293426/topological-sort-with-loops
    which is based on: Eades, Lin, and Smyth [1993]: 'A fast and effective heuristic for the feedback arc set problem'.
    """
    lstack = []
    rstack = []

    label_to_node = { label:_TopoNode(no, label) for no,label in enumerate(items) }

    for src,dst in partial_order:
        s_node = label_to_node[src]
        d_node = label_to_node[dst]
        if s_node is not d_node:
            s_node.outs.add(d_node)
            d_node.ins.add(s_node)

    nodes = set(label_to_node.values())
    sources = set(node for node in nodes if len(node.ins)==0)
    sinks = set(node for node in nodes if len(node.outs)==0)

    source_heap = HeapSet(sources)
    sink_heap = HeapSet(sinks, key=lambda node: -node.ix)

    # If there is a cycle, this is how we pick an arbitrary node to go first:
    # Prefer nodes with more inputs and outputs, since removing such a node has a better chance of
    # breaking cycles.
    # Failing that, abide by the original order (.ix).
    source_candidate_heap = HeapSet(nodes, key=lambda n: (-(len(n.ins)+len(n.outs)), n.ix))

    def disconnect(node):
        for in_node in node.ins:
            in_node.outs.discard(node)
            source_candidate_heap.recompute_key(node)
            if len(in_node.outs)==0:
                sink_heap.push(in_node)
        for out_node in node.outs:
            out_node.ins.discard(node)
            source_candidate_heap.recompute_key(node)
            if len(out_node.ins)==0:
                source_heap.push(out_node)
        source_heap.discard(node)
        sink_heap.discard(node)
        source_candidate_heap.discard(node)
        
        node.ins = None
        node.outs = None
        nodes.discard(node)

    while True:
        if source_heap:
            inode = source_heap.pop()
            disconnect(inode)
            lstack.append(inode)
            source_candidate_heap.discard(inode)

        elif sink_heap:
            anode = sink_heap.pop()
            disconnect(anode)
            rstack.append(anode)
            source_candidate_heap.discard(anode)

        elif source_candidate_heap:
            inode = source_candidate_heap.pop()
            disconnect(inode)
            lstack.append(inode)
            source_candidate_heap.discard(inode)

        else:
            break

    return [node.label for node in lstack + rstack[::-1]]

def stable_topological_sort(items, partial_order):
    """!
    @brief Stable-ish topological sort.
    @param[in] items		An iterable of hashable elements to sort.
    @param[in] partial_order	List of (before,after) dependencies prescribing that the 'before' node should
                                precede the 'after' node in the result.
    @return list of items in the specified order.

    Based on https://stackoverflow.com/questions/57293426/topological-sort-with-loops
    which is based on: Eades, Lin, and Smyth [1993]: 'A fast and effective heuristic for the feedback arc set problem'.
    """
    lstack = []
    rstack = []

    label_to_node = { label:_TopoNode(no, label) for no,label in enumerate(items) }

    for src,dst in partial_order:
        s_node = label_to_node[src]
        d_node = label_to_node[dst]
        if s_node is not d_node:
            s_node.outs.add(d_node)
            d_node.ins.add(s_node)

    nodes = set(label_to_node.values())
    sources = set(node for node in nodes if len(node.ins)==0)
    sinks = set(node for node in nodes if len(node.outs)==0)

    source_heap = HeapSet(sources)
    sink_heap = HeapSet(sinks, key=lambda node: -node.ix)

    def disconnect(node):
        for in_node in node.ins:
            in_node.outs.discard(node)
            if len(in_node.outs)==0:
                sink_heap.push(in_node)
        for out_node in node.outs:
            out_node.ins.discard(node)
            if len(out_node.ins)==0:
                source_heap.push(out_node)
        source_heap.discard(node)
        sink_heap.discard(node)

        node.ins = None
        node.outs = None
        nodes.discard(node)

    while nodes:
        if source_heap:
            inode = source_heap.pop()
            disconnect(inode)
            lstack.append(inode)

        elif sink_heap:
            anode = sink_heap.pop()
            disconnect(anode)
            rstack.append(anode)

        else:
            raise CycleError

    return [node.label for node in lstack + rstack[::-1]]
