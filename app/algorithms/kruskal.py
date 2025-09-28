from typing import List, Generator, Any, Dict, Tuple
from app.utils.types import Event, Graph
from app.utils.union_find import UnionFind

def kruskal_generator(graph: Graph) -> Generator[Event, None, None]:
    """Generates events for visualizing Kruskal's algorithm for Minimum Spanning Tree (MST).

    Args:
        graph (Graph): The graph represented as an adjacency list
                       (e.g., {"A": [("B", 1)], "B": [("A", 1)]}).

    Yields:
        Event: An event object representing a step in the algorithm.
    """
    step_count = 0
    nodes = list(graph.keys())
    edges = []
    for u in graph:
        for v, weight in graph[u]:
            # Add each edge only once for undirected graphs
            if (v, u, weight) not in edges and (u, v, weight) not in edges:
                edges.append((u, v, weight))

    # Sort all edges by weight
    edges.sort(key=lambda x: x[2])

    mst_edges = []
    uf = UnionFind(nodes)

    yield Event(
        step=step_count,
        type="snapshot",
        details="Initial graph state",
        data={"graph_snapshot": graph, "nodes": nodes, "sorted_edges": edges}
    )
    step_count += 1

    for u, v, weight in edges:
        yield Event(
            step=step_count,
            type="consider_edge",
            details=f"Considering edge ({u}-{v}) with weight {weight}",
            data={"u": u, "v": v, "weight": weight, "mst_edges": list(mst_edges), "graph_snapshot": graph}
        )
        step_count += 1

        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            mst_edges.append((u, v))
            yield Event(
                step=step_count,
                type="add_mst_edge",
                details=f"Adding edge ({u}-{v}) to MST (weight {weight})",
                data={"u": u, "v": v, "weight": weight, "mst_edges": list(mst_edges), "graph_snapshot": graph}
            )
            step_count += 1

    yield Event(
        step=step_count,
        type="done",
        details="Kruskal's algorithm completed",
        data={"mst_edges": mst_edges, "final_graph": graph}
    )


if __name__ == '__main__':
    # Example graph (from Wikipedia for Kruskal's)
    example_graph = {
        "A": [("B", 7), ("D", 5)],
        "B": [("A", 7), ("C", 8), ("D", 9), ("E", 7)],
        "C": [("B", 8), ("E", 5)],
        "D": [("A", 5), ("B", 9), ("E", 15), ("F", 6)],
        "E": [("B", 7), ("C", 5), ("D", 15), ("F", 8), ("G", 9)],
        "F": [("D", 6), ("E", 8), ("G", 11)],
        "G": [("E", 9), ("F", 11)]
    }

    print("Running Kruskal's on example graph:")
    events = list(kruskal_generator(example_graph))

    print("\n--- Events ---")
    for event in events:
        print(event.to_json_serializable())

    print("\n--- Final MST Edges ---")
    final_event = next(e for e in reversed(events) if e.type == "done")
    print(final_event.data["mst_edges"])

    # Expected MST edges (order might vary, but the set of edges should be the same)
    expected_mst_edges = [
        ("A", "D"), ("C", "E"), ("D", "F"), ("B", "E"), ("A", "B"), ("E", "G")
    ]
    # Convert to set of frozensets for order-independent comparison
    actual_mst_edges_set = {frozenset(edge) for edge in final_event.data["mst_edges"]}
    expected_mst_edges_set = {frozenset(edge) for edge in expected_mst_edges}

    assert actual_mst_edges_set == expected_mst_edges_set
    print("Assertion passed: MST edges are correct.")

    # Test with a disconnected graph (should still find MST for each component)
    disconnected_graph = {
        "A": [("B", 1)],
        "B": [("A", 1)],
        "C": [("D", 2)],
        "D": [("C", 2)]
    }
    print("\nRunning Kruskal's on disconnected graph:")
    events_disconnected = list(kruskal_generator(disconnected_graph))
    final_event_disconnected = next(e for e in reversed(events_disconnected) if e.type == "done")
    print(final_event_disconnected.data["mst_edges"])
    expected_disconnected_mst = [{frozenset(("A", "B"))}, {frozenset(("C", "D"))}]
    actual_disconnected_mst = [{frozenset(edge)} for edge in final_event_disconnected.data["mst_edges"]]
    assert all(item in expected_disconnected_mst for item in actual_disconnected_mst) and \
           all(item in actual_disconnected_mst for item in expected_disconnected_mst)
    print("Disconnected graph test passed.")

