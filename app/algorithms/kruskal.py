from typing import List, Generator, Any, Dict, Tuple, Optional, Set
from app.utils.types import Event, Graph
from app.utils.union_find import UnionFind
import matplotlib.cm as cm
import numpy as np

# --- Visualization Constants ---
CONSIDER_EDGE_COLOR = "#3399ff"  # Bright blue
MST_EDGE_COLOR = "#333333"       # Dark grey/black
REJECT_EDGE_COLOR = "#ff6666"    # Light red
DEFAULT_EDGE_COLOR = "#b3b3b3"  # Light grey

MST_EDGE_WIDTH = 3.0
CONSIDER_EDGE_WIDTH = 2.5
DEFAULT_EDGE_WIDTH = 1.5

def _get_set_colors(uf: UnionFind) -> Dict[Any, str]:
    """Assigns a unique color to each disjoint set."""
    set_representatives = {uf.find(node) for node in uf.parent}
    num_sets = len(set_representatives)

    # Use a perceptually uniform colormap
    colormap = cm.get_cmap('viridis', num_sets)
    set_colors = {rep: colormap(i) for i, rep in enumerate(set_representatives)}

    node_colors = {}
    for node in uf.parent:
        root = uf.find(node)
        # Convert RGBA to hex
        rgba_color = set_colors[root]
        hex_color = '#%02x%02x%02x' % (int(rgba_color[0]*255), int(rgba_color[1]*255), int(rgba_color[2]*255))
        node_colors[node] = hex_color

    return node_colors

def _create_visual_state(
    graph: Graph,
    uf: UnionFind,
    mst_edges: List[Tuple[Any, Any]],
    considered_edge: Optional[Tuple[Any, Any, int]] = None,
    rejected_edge: Optional[Tuple[Any, Any, int]] = None,
) -> Dict[str, Any]:
    """Helper to create a rich visual state for the renderer at each step."""
    node_colors = _get_set_colors(uf)
    edge_colors = {}
    edge_widths = {}

    # Default edge styles
    for u, neighbors in graph.items():
        for v, _ in neighbors:
            edge = tuple(sorted((u, v)))
            edge_colors[edge] = DEFAULT_EDGE_COLOR
            edge_widths[edge] = DEFAULT_EDGE_WIDTH

    # Style for MST edges
    for u, v in mst_edges:
        edge = tuple(sorted((u, v)))
        edge_colors[edge] = MST_EDGE_COLOR
        edge_widths[edge] = MST_EDGE_WIDTH

    # Highlight considered edge
    if considered_edge:
        u, v, _ = considered_edge
        edge = tuple(sorted((u, v)))
        edge_colors[edge] = CONSIDER_EDGE_COLOR
        edge_widths[edge] = CONSIDER_EDGE_WIDTH

    # Highlight rejected edge
    if rejected_edge:
        u, v, _ = rejected_edge
        edge = tuple(sorted((u, v)))
        edge_colors[edge] = REJECT_EDGE_COLOR
        edge_widths[edge] = CONSIDER_EDGE_WIDTH # Keep width consistent with consideration

    # Node labels are just the node names for Kruskal's
    node_labels = {node: str(node) for node in graph}

    return {
        "graph_snapshot": graph,
        "node_colors": node_colors,
        "edge_colors": edge_colors,
        "edge_widths": edge_widths,
        "node_labels": node_labels,
    }


def kruskal_generator(graph: Graph) -> Generator[Event, None, None]:
    """Generates events for visualizing Kruskal's algorithm with rich visual metadata."""
    step_count = 0
    nodes = list(graph.keys())
    if not nodes:
        yield Event(step=0, type="done", details="Graph is empty.", data={})
        return

    edges = []
    for u in graph:
        for v, weight in graph[u]:
            if tuple(sorted((u, v))) not in [(e[0], e[1]) for e in edges]:
                 edges.append((u, v, weight))

    edges.sort(key=lambda x: x[2])

    mst_edges = []
    uf = UnionFind(nodes)

    # Initial state
    yield Event(
        step=step_count,
        type="start",
        details="Starting Kruskal's. Edges sorted by weight.",
        data=_create_visual_state(graph, uf, mst_edges)
    )
    step_count += 1

    for u, v, weight in edges:
        # Event: Considering an edge
        yield Event(
            step=step_count,
            type="consider_edge",
            details=f"Considering edge ({u}-{v}) with weight {weight}",
            data=_create_visual_state(graph, uf, mst_edges, considered_edge=(u, v, weight))
        )
        step_count += 1

        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            mst_edges.append(tuple(sorted((u, v))))
            # Event: Add edge to MST
            yield Event(
                step=step_count,
                type="add_mst_edge",
                details=f"Adding edge ({u}-{v}) to MST. Sets merged.",
                data=_create_visual_state(graph, uf, mst_edges)
            )
            step_count += 1
        else:
            # Event: Reject edge (forms a cycle)
            yield Event(
                step=step_count,
                type="reject_edge",
                details=f"Rejecting edge ({u}-{v}). It would form a cycle.",
                data=_create_visual_state(graph, uf, mst_edges, rejected_edge=(u, v, weight))
            )
            step_count += 1

    # Final state
    yield Event(
        step=step_count,
        type="done",
        details="Kruskal's algorithm completed.",
        data=_create_visual_state(graph, uf, mst_edges)
    )

if __name__ == '__main__':
    example_graph = {
        "A": [("B", 7), ("D", 5)], "B": [("A", 7), ("C", 8), ("D", 9), ("E", 7)],
        "C": [("B", 8), ("E", 5)], "D": [("A", 5), ("B", 9), ("E", 15), ("F", 6)],
        "E": [("B", 7), ("C", 5), ("D", 15), ("F", 8), ("G", 9)],
        "F": [("D", 6), ("E", 8), ("G", 11)], "G": [("E", 9), ("F", 11)]
    }

    print("Running Kruskal's on example graph:")
    events = list(kruskal_generator(example_graph))

    print(f"\n--- Generated {len(events)} events ---")
    for i, event in enumerate(events):
        print(f"Step {i}: {event.type} - {event.details}")

    final_event = events[-1]
    final_data = final_event.data

    # Extract MST edges from the final event's visual state
    final_mst_edges = []
    for edge, color in final_data['edge_colors'].items():
        if color == MST_EDGE_COLOR:
            final_mst_edges.append(edge)

    print("\n--- Final MST Edges ---")
    print(sorted(final_mst_edges))

    expected_mst_edges = [
        ('A', 'B'), ('A', 'D'), ('C', 'E'), ('D', 'F'), ('E', 'B'), ('E', 'G')
    ]

    # Normalize for comparison
    actual_set = {frozenset(e) for e in final_mst_edges}
    expected_set = {frozenset(e) for e in expected_mst_edges}

    assert actual_set == expected_set
    print("Assertion passed: Final MST edges are correct.")

    # Test with a disconnected graph
    disconnected_graph = {"A": [("B", 1)], "B": [("A", 1)], "C": [("D", 2)], "D": [("C", 2)]}
    print("\nRunning Kruskal's on disconnected graph:")
    events_disconnected = list(kruskal_generator(disconnected_graph))
    final_event_disconnected = events_disconnected[-1]

    final_mst_disconnected = []
    for edge, color in final_event_disconnected.data['edge_colors'].items():
        if color == MST_EDGE_COLOR:
            final_mst_disconnected.append(edge)

    print(sorted(final_mst_disconnected))
    expected_disconnected_set = {frozenset(("A", "B")), frozenset(("C", "D"))}
    actual_disconnected_set = {frozenset(e) for e in final_mst_disconnected}

    assert actual_disconnected_set == expected_disconnected_set
    print("Disconnected graph test passed.")