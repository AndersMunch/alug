import unittest, random, pprint, sys, os.path
sys.path.insert(0, os.path.join(os.path.split(__file__)[0], '..'))
from alug.topo import semi_topological_sort, stable_topological_sort, CycleError

try:
    import graphlib
except ImportError:
    # Skip tests that require graphlib on older Python's that don't have it.
    # alug.topo should work fine on older Python's just the same.
    graphlib = None

class Test_semi_topological_sort(unittest.TestCase):
    def testempty(self):
        self.assertEqual(
            semi_topological_sort([], []),
            [],
            )

    def testone(self):
        self.assertEqual(
            semi_topological_sort(['fronkonstein'], []),
            ['fronkonstein'],
            )

    def test_two_nocondition(self):
        self.assertEqual(
            semi_topological_sort(['hello', 'world'], []),
            ['hello', 'world'],
            )

    def test_two_condition_as_is(self):
        self.assertEqual(
            semi_topological_sort(['hello', 'world'], [('hello','world')]),
            ['hello', 'world'],
            )

    def test_two_condition_reverse(self):
        self.assertEqual(
            semi_topological_sort(['hello', 'world'], [('world', 'hello')]),
            ['world', 'hello'],
            )

    def test_two_cycle(self):
        self.assertEqual(
            semi_topological_sort(['hello', 'world'],
                                  [('hello','world'), ('world', 'hello')]),
            ['hello', 'world'],
            )

    def test_total_order(self):
        N = 100
        ordered = list(range(N))
        unordered = ordered.copy()
        random.shuffle(unordered)
        conditions = [(n,n+1) for n in range(N-1)]
        random.shuffle(conditions)
        self.assertEqual(
            semi_topological_sort(unordered, conditions),
            ordered,
            )

    def testexample1(self):
        self.assertEqual(
            semi_topological_sort([1,2,3], [(1,2),(1,3),(3,2)]),
            [1,3,2])

    def testexample2(self):
        self.assertEqual(
            semi_topological_sort([1,2], [(2,1),(2,1)]),
            [2,1])

    def testregression1(self):
        self.assertEqual(
            semi_topological_sort([1,2,3], []),
            [1,2,3])

    def testregression2(self):
        self.assertEqual(
            semi_topological_sort([1,2,3,4], [(1,2),(3,4)]),
            [1,2,3,4])

    def testregression3(self):
        self.assertEqual(
            semi_topological_sort([4,3,2,1], [(1,2),(3,4)]),
            [3,4,1,2])

    def testregression4(self):
        self.assertEqual(
            semi_topological_sort([1,4,3,2], [(4,1),(3,2)]),
            [4,1,3,2])

    def testregression5(self):
        self.assertEqual(
            semi_topological_sort([4,2,3,1], [(3,2)]),
            [4,3,2,1])

    def testchain(self):
        self.assertEqual(
            semi_topological_sort([1,2,3,4], [(1,2),(2,3),(3,4)]),
            [1,2,3,4])
        self.assertEqual(
            semi_topological_sort([4,2,3,1], [(1,2),(2,3),(3,4)]),
            [1,2,3,4])
        self.assertEqual(
            semi_topological_sort([1,2,3,4], [(3,4),(2,1),(1,3)]),
            [2,1,3,4])

    def test_failed_at_one_point(self):
        self.assertEqual(
            semi_topological_sort([4,3,2,1], [(3,4),(2,1),(1,3)]),
            [2,1,3,4])

    def test_odd_one_out(self):
        self.assertEqual(
            semi_topological_sort(
                [5,1,4,2,3],
                [(1,2), (2,3), (3,4), (4,5), # everything fits [1,2,3,4,5]
                 (4,2), # except this one dep. going the other way
                 ]),
             # The original intended solution was [1,2,3,4,5], but the algorithm found a better one!
             [1,4,2,3,5],
            )

    def test_topology_10_3(self):
        for _ in range(10):
            self._test_topology(N_elements=10, N_conditions=3)

    def test_topology_100_100(self):
        self._test_topology(N_elements=100, N_conditions=100)

    def test_topology_50_200(self):
        self._test_topology(N_elements=50, N_conditions=200)


    def _test_topology(self, N_elements, N_conditions):
        base_set = list(range(N_elements))
        conditions = set()
        for _ in range(N_conditions):
            A = random.randrange(N_elements)
            B = random.randrange(N_elements)
            if A==B:
                continue
            if A > B:
                conditions.add((B,A))
            else:
                conditions.add((A,B))

        random.shuffle(base_set)
        base_set = list(map(str, base_set))
        conditions = [list(map(str, pair)) for pair in conditions]
        res = semi_topological_sort(base_set, conditions)
        self._check_result_validity(elements=base_set, conditions=list(conditions), res=res)


    def _check_result_validity(self, elements, conditions, res, max_order_violations=0):
        N_elements = len(elements)
        N_conditions = len(conditions)

        self.assertEqual(set(res), set(elements))
        ixx = dict()
        for ix,item in enumerate(res):
            ixx[item] = ix

        order_violations = []
        for A,B in conditions:
            if ixx[A] >= ixx[B]:
                order_violations.append((A,B))

        if len(order_violations) > max_order_violations:
            print("ERROR:")
            print("Elements:")
            pprint.pprint(elements)
            print("Conditions:")
            pprint.pprint(conditions)
            print("Result:")
            pprint.pprint(res)
            for A,B in order_violations:
                print("Failed constraint [%s]=%s >= [%s]=%s" % (ixx[A], A, ixx[B], B))
            self.assertLessEqual(len(order_violations), max_order_violations)
                

        # Check that the original order is mostly retained.
        if max_order_violations==0 and N_conditions < N_elements:
            # xx something definitely wrong here:
            # This sorts identically, no changes needed:
            # [0, 9, 1, 6, 3, 2, 5, 8, 4, 7], [(0, 9), (2, 8)]
            # Yet it counts only 4 order preservations, there should have been 9?!
            order_preservations = 0
            for elno in range(N_elements-1):
                if ixx[elements[elno]] < ixx[elements[elno+1]]:
                    order_preservations += 1

            if order_preservations >= N_elements - 1 - N_conditions:
                pass
            else:
                print("N_elements=%d, N_conditions=%d, #order_preservations=%d" % (N_elements, N_conditions, order_preservations))
                if N_elements <= 10:
                    print("base set:")
                    pprint.pprint(elements)
                    print("conditions:")
                    pprint.pprint(conditions)
                    print("result:")
                    pprint.pprint(res)
                self.assertGreaterEqual(order_preservations, N_elements - 1 - N_conditions)


    def test_stability(self):
        # Sort disconnected sets: Multiple groups, and no dependencies cross-group.
        N_elements = 30
        group_size = 10
        N_groups = 3
        N_elements = group_size * N_groups
        N_conditions = 20

        base_set = list(range(N_elements))

        conds = set()
        for _ in range(N_conditions):
            A = random.randrange(N_elements)
            groupno = A // group_size
            # Find a B in the same group as A, but different from A.
            B = groupno * group_size + random.randrange(group_size - 1)
            if B >= A:
                B += 1
            if A < B:
                # No cycles.
                A,B = B,A
            conds.add((A,B))
        conds = list(conds)

        res = semi_topological_sort(base_set,conds)

        # This is the sort of stability I want: as there are no dependencies between the groups, there should be
        # no reordering, and each group should retain its position in the result, only sorted internally.
        #
        # Ideally, this should work even though there are cycles, it doesn't though.

        for groupno,groupbase in enumerate(range(0, N_elements, group_size)):
            group = base_set[groupbase:groupbase+group_size]
            res_group = res[groupbase:groupbase+group_size]
            self.assertEqual(sorted(res_group), sorted(group))


    def test_example_with_poor_order_preservation(self):
        # Went looking for an example of the order being poorly preserved, and found this:
        
        # N_elements=10, N_conditions=2, #order_preservations=4
        # base set:
        # [4, 3, 7, 2, 6, 8, 9, 0, 1, 5]
        # conditions:
        # [(5, 9), (3, 8)]
        # result:
        # [4, 3, 7, 2, 6, 8, 0, 1, 5, 9]

        # However, that's not bad at all.  The only change is moving the 9.
        # How does that amount to 4 order changes?  Probably a bad algorithm in the test code, not the code under test.
        
        base_set = [4, 3, 7, 2, 6, 8, 9, 0, 1, 5]
        conditions = [(5, 9), (3, 8)]
        self.assertEqual(semi_topological_sort(base_set, conditions),
                         [4, 3, 7, 2, 6, 8, 0, 1, 5, 9])


if graphlib is not None:
    def stdlib_toposort(items, partial_order):
        """!
        @brief Wrapper around graphlib.TopologicalSorter for interface compatibility.
        """
        graph = { it:set() for it in items }
        for before,after in partial_order:
            graph[after].add(before)

        ts = graphlib.TopologicalSorter(graph)
        return list(ts.static_order())


    class Test_stable_topological_sort(unittest.TestCase):
        def check_is_a_topological_sort_of(self, sortedvals, unsortedvals, conditions):
            self.assertEqual(set(sortedvals), set(unsortedvals))
            positions = dict((element,ix) for ix,element in enumerate(sortedvals))
            for before,after in conditions:
                self.assertLessEqual(positions[before], positions[after], (sortedvals,conditions,before,after))

        def _ex(self, elements, conditions, ordered=None):
            # Test that CycleError occurs precisely when the stdlib toposort would have CycleError'd.
            try:
                stdlib_toposort(elements, conditions)
            except graphlib.CycleError:
                self.assertRaises(CycleError, stable_topological_sort, elements, conditions)
            else:
                sortedvals = stable_topological_sort(elements, conditions)
                self.check_is_a_topological_sort_of(sortedvals, elements, conditions)

                # If a specific ordering is expected, check that.
                if ordered is not None:
                    self.assertEqual(sortedvals, ordered)

        def testempty(self):
            self._ex([], [])

        def testone(self):
            self._ex(['fronkonstein'], [])

        def test_two_nocondition(self):
            self._ex(['hello', 'world'], [])

        def test_two_condition_as_is(self):
            self._ex(['hello', 'world'], [('hello','world')])

        def test_two_condition_reverse(self):
            self._ex(['hello', 'world'], [('world', 'hello')])

        def test_two_cycle(self):
            self._ex(['hello', 'world'],
                     [('hello','world'), ('world', 'hello')])

        def test_total_order(self):
            N = 100
            ordered = list(range(N))
            unordered = ordered.copy()
            random.shuffle(unordered)
            conditions = [(n,n+1) for n in range(N-1)]
            random.shuffle(conditions)
            self._ex(unordered, conditions, ordered)

        def testexample1(self):
            self._ex([1,2,3], [(1,2),(1,3),(3,2)])

        def testexample2(self):
            self._ex([1,2], [(2,1),(2,1)])

        def testregression1(self):
            self._ex([1,2,3], [])

        def testregression2(self):
            self._ex([1,2,3,4], [(1,2),(3,4)], [1,2,3,4])

        def testregression3(self):
            self._ex([4,3,2,1], [(1,2),(3,4)], [3,4,1,2])

        def testregression4(self):
            self._ex([1,4,3,2], [(4,1),(3,2)], [4,1,3,2])

        def testregression5(self):
            self._ex([4,2,3,1], [(3,2)], [4,3,2,1])

        def testchain(self):
            self._ex([1,2,3,4], [(1,2),(2,3),(3,4)])

        def test_failed_at_one_point(self):
            self._ex([4,3,2,1], [(3,4),(2,1),(1,3)])

        def test_odd_one_out(self):
            self._ex(
                [5,1,4,2,3],
                [(1,2), (2,3), (3,4), (4,5), # everything fits [1,2,3,4,5]
                 (4,2), # except this one dep. going the other way
                 ],
                 # The original intended solution was [1,2,3,4,5], but the algorithm found a better one!
                 [1,4,2,3,5],
                )

        def test_random(self):
            # These can be set to higher values for a more thorough test.
            repeat_times = 100
            max_size = 100
            for _ in range(repeat_times):
                N_ele = random.randrange(1, max_size)
                N_constraints = random.randrange(N_ele//2, round(N_ele*1.5))
                elements = list(range(N_ele))
                random.shuffle(elements)
                constraints = [(random.randrange(N_ele), random.randrange(N_ele)) for _ in range(N_constraints)]
                constraints = [(before,after) for before,after in constraints if before != after]
                random.shuffle(constraints)
                self._ex(elements, constraints)


if __name__=='__main__':
    unittest.main()
