class UnionFind:
    """A Union-Find (Disjoint Set Union) data structure.

    Used to keep track of a set of elements partitioned into a number of disjoint (non-overlapping) sets.
    """
    def __init__(self, elements):
        """Initializes the Union-Find structure.

        Args:
            elements: An iterable of elements to initialize the sets with.
        """
        self.parent = {e: e for e in elements}
        self.rank = {e: 0 for e in elements}

    def find(self, i):
        """Finds the representative (root) of the set containing element i.

        Performs path compression for optimization.
        """
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        """Unites the sets containing elements i and j.

        Performs union by rank for optimization.
        Returns True if a union was performed (i.e., i and j were in different sets),
        False otherwise.
        """
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i != root_j:
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                self.parent[root_j] = root_i
                self.rank[root_i] += 1
            return True
        return False


if __name__ == '__main__':
    # Example usage
    elements = [0, 1, 2, 3, 4, 5]
    uf = UnionFind(elements)

    print("Initial parents:", uf.parent)

    uf.union(0, 1)
    uf.union(1, 2)
    print("After union(0,1) and union(1,2):")
    print("Parent of 0:", uf.find(0))
    print("Parent of 1:", uf.find(1))
    print("Parent of 2:", uf.find(2))
    assert uf.find(0) == uf.find(1) == uf.find(2)

    uf.union(3, 4)
    print("After union(3,4):")
    print("Parent of 3:", uf.find(3))
    print("Parent of 4:", uf.find(4))
    assert uf.find(3) == uf.find(4)

    print("Attempting union(0,3) (should connect the two components)")
    assert uf.union(0, 3) is True
    print("Parent of 0:", uf.find(0))
    print("Parent of 3:", uf.find(3))
    assert uf.find(0) == uf.find(3)

    print("Attempting union(1,2) (should do nothing as they are already connected)")
    assert uf.union(1, 2) is False

    print("Union-Find tests passed.")

