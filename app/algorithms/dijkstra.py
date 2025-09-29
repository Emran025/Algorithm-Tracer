from typing import List, Generator, Any, Dict, Tuple, Optional, Set
from app.utils.types import Event, Graph
import heapq

# --- Visualization Constants ---
VISITED_NODE_COLOR = "#cccccc"
CURRENT_NODE_COLOR = "#ff9933"
DEFAULT_NODE_COLOR = "#66b3ff"
CONSIDER_EDGE_COLOR = "#3399ff"
RELAX_EDGE_COLOR = "#66cc66"
PATH_EDGE_COLOR = "#333333"
DEFAULT_EDGE_COLOR = "#b3b3b3"
FINAL_PATH_NODE_COLOR = "#2ca02c"  # Emphasized green for final path nodes
FINAL_PATH_EDGE_COLOR = "#2ca02c"  # Emphasized green for final path edges
DEEMPHASIZED_COLOR = "#e6e6e6"     # Very light grey for non-path elements in final view

PATH_EDGE_WIDTH = 3.0
CONSIDER_EDGE_WIDTH = 2.5
DEFAULT_EDGE_WIDTH = 1.5

def _create_visual_state(
    graph: Graph,
    distances: Dict[Any, float],
    visited: Set[Any],
    path: Dict[Any, Optional[Any]],
    current_node: Optional[Any] = None,
    considered_edge: Optional[Tuple[Any, Any]] = None,
    relaxed_edge: Optional[Tuple[Any, Any]] = None,
    is_final_state: bool = False,
) -> Dict[str, Any]:
    """Helper to create a rich visual state for the renderer at each step."""
    node_colors = {}
    edge_colors = {}
    edge_widths = {}

    path_edges = set()
    for node, parent in path.items():
        if parent:
            path_edges.add(tuple(sorted((parent, node))))

    if is_final_state:
        # Final "done" state: de-emphasize everything except the shortest path tree
        all_nodes = set(graph.keys())
        path_nodes = {node for edge in path_edges for node in edge}
        if path: # Add the start node if it exists
            path_nodes.add(next(iter(path)))


        for node in all_nodes:
            node_colors[node] = FINAL_PATH_NODE_COLOR if node in path_nodes else DEEMPHASIZED_COLOR

        for u, neighbors in graph.items():
            for v, _ in neighbors:
                edge = tuple(sorted((u, v)))
                if edge in path_edges:
                    edge_colors[edge] = FINAL_PATH_EDGE_COLOR
                    edge_widths[edge] = PATH_EDGE_WIDTH
                else:
                    edge_colors[edge] = DEEMPHASIZED_COLOR
                    edge_widths[edge] = DEFAULT_EDGE_WIDTH
    else:
        # In-progress state rendering
        node_colors = {node: DEFAULT_NODE_COLOR for node in graph}
        for node in visited:
            node_colors[node] = VISITED_NODE_COLOR
        if current_node:
            node_colors[current_node] = CURRENT_NODE_COLOR

        for u, neighbors in graph.items():
            for v, _ in neighbors:
                edge = tuple(sorted((u, v)))
                edge_colors[edge] = DEFAULT_EDGE_COLOR
                edge_widths[edge] = DEFAULT_EDGE_WIDTH

        for u, v in path_edges:
            edge = tuple(sorted((u, v)))
            edge_colors[edge] = PATH_EDGE_COLOR
            edge_widths[edge] = PATH_EDGE_WIDTH

        if considered_edge:
            edge = tuple(sorted(considered_edge))
            edge_colors[edge] = CONSIDER_EDGE_COLOR
            edge_widths[edge] = CONSIDER_EDGE_WIDTH
        if relaxed_edge:
            edge = tuple(sorted(relaxed_edge))
            edge_colors[edge] = RELAX_EDGE_COLOR
            edge_widths[edge] = PATH_EDGE_WIDTH

    node_labels = {
        node: f"{node}\n({dist if dist != float('inf') else '∞'})"
        for node, dist in distances.items()
    }

    return {
        "graph_snapshot": graph,
        "node_colors": node_colors,
        "edge_colors": edge_colors,
        "edge_widths": edge_widths,
        "node_labels": node_labels,
    }

def dijkstra_generator(graph: Graph, start_node: Any) -> Generator[Event, None, None]:
    """Generates events for visualizing Dijkstra's algorithm with rich visual metadata."""
    step_count = 0
    if not graph or start_node not in graph:
        yield Event(step=0, type="error", details=f"Start node {start_node} not in graph.", data={})
        return

    for u in graph:
        for v, weight in graph[u]:
            if weight < 0:
                yield Event(step=0, type="error", details=f"Negative weight on edge {u}-{v}.", data={})
                return

    distances = {node: float("inf") for node in graph}
    distances[start_node] = 0
    priority_queue = [(0, start_node)]
    visited = set()
    path = {node: None for node in graph}

    yield Event(
        step=step_count,
        type="start",
        details=f"Starting Dijkstra's from node {start_node}",
        data=_create_visual_state(graph, distances, visited, path, current_node=start_node)
    )
    step_count += 1

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node in visited:
            continue

        visited.add(current_node)

        yield Event(
            step=step_count,
            type="visit",
            details=f"Visiting node {current_node} (distance: {current_distance})",
            data=_create_visual_state(graph, distances, visited, path, current_node=current_node)
        )
        step_count += 1

        for neighbor, weight in sorted(graph.get(current_node, []), key=lambda x: x[0]):
            if neighbor not in visited:
                yield Event(
                    step=step_count,
                    type="consider_edge",
                    details=f"Considering edge {current_node} -> {neighbor} (weight: {weight})",
                    data=_create_visual_state(
                        graph, distances, visited, path,
                        current_node=current_node,
                        considered_edge=(current_node, neighbor)
                    )
                )
                step_count += 1

                new_distance = current_distance + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    path[neighbor] = current_node
                    heapq.heappush(priority_queue, (new_distance, neighbor))

                    yield Event(
                        step=step_count,
                        type="relax",
                        details=f"Relaxed edge {current_node} -> {neighbor}. New distance: {new_distance}",
                        data=_create_visual_state(
                            graph, distances, visited, path,
                            current_node=current_node,
                            relaxed_edge=(current_node, neighbor)
                        )
                    )
                    step_count += 1

    final_data = _create_visual_state(graph, distances, visited, path, is_final_state=True)
    final_data["distances"] = distances
    yield Event(
        step=step_count,
        type="done",
        details="Dijkstra's algorithm completed",
        data=final_data
    )

if __name__ == '__main__':
    example_graph = {
        'A': [('B', 4), ('C', 2)], 'B': [('A', 4), ('E', 3)],
        'C': [('A', 2), ('D', 2), ('F', 4)], 'D': [('C', 2), ('E', 3)],
        'E': [('B', 3), ('D', 3), ('F', 1)], 'F': [('C', 4), ('E', 1)]
    }
    start_node = 'A'

    print(f"Running Dijkstra's from node {start_node} on example graph:")
    events = list(dijkstra_generator(example_graph, start_node))

    print("\n--- Events ---")
    for i, event in enumerate(events):
        print(f"Step {i}: {event.type} - {event.details}")

    final_event = events[-1]
    final_data = final_event.data

    # Test final state colors
    assert final_data['node_colors']['A'] == FINAL_PATH_NODE_COLOR
    assert final_data['edge_colors'][('A', 'C')] == FINAL_PATH_EDGE_COLOR
    assert final_data['node_colors']['F'] == FINAL_PATH_NODE_COLOR # Part of path
    print("Final path highlighting test passed.")

    final_distances = {
        node: float(label.split('\n(')[1][:-1]) if '∞' not in label else float('inf')
        for node, label in final_data['node_labels'].items()
    }
    print("\n--- Final Distances ---")
    print(final_distances)

    expected_distances = {'A': 0, 'B': 4, 'C': 2, 'D': 4, 'E': 7, 'F': 6}
    assert final_distances == expected_distances
    print("Assertion passed: Final distances are correct.")

    negative_weight_graph = {'A': [('B', -1)], 'B': []}
    events_negative = list(dijkstra_generator(negative_weight_graph, 'A'))
    assert any(e.type == "error" for e in events_negative)
    print("Negative weight test passed.")
