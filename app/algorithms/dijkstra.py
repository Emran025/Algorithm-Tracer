from typing import List, Generator, Any, Dict, Tuple, Optional, Set
from app.utils.types import Event, Graph
import heapq

# --- Visualization Constants ---
VISITED_NODE_COLOR = "#cccccc"  # Light grey for visited nodes
CURRENT_NODE_COLOR = "#ff9933"  # Bright orange for the current node
DEFAULT_NODE_COLOR = "#66b3ff"  # A calm blue for default state
CONSIDER_EDGE_COLOR = "#3399ff" # Bright blue for the edge being considered
RELAX_EDGE_COLOR = "#66cc66"   # Green for a relaxed edge
PATH_EDGE_COLOR = "#333333"    # Dark grey/black for final path edges
DEFAULT_EDGE_COLOR = "#b3b3b3" # Light grey for default edges

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
) -> Dict[str, Any]:
    """Helper to create a rich visual state for the renderer at each step."""
    node_colors = {node: DEFAULT_NODE_COLOR for node in graph}
    edge_colors = {}
    edge_widths = {}

    # Set colors for visited nodes
    for node in visited:
        node_colors[node] = VISITED_NODE_COLOR

    # Highlight the current node
    if current_node:
        node_colors[current_node] = CURRENT_NODE_COLOR

    # Build the path edges for styling
    path_edges = set()
    for node, parent in path.items():
        if parent:
            path_edges.add(tuple(sorted((parent, node))))

    # Set default edge styles
    for u, neighbors in graph.items():
        for v, _ in neighbors:
            edge = tuple(sorted((u, v)))
            edge_colors[edge] = DEFAULT_EDGE_COLOR
            edge_widths[edge] = DEFAULT_EDGE_WIDTH

    # Style path edges
    for u, v in path_edges:
        edge = tuple(sorted((u, v)))
        edge_colors[edge] = PATH_EDGE_COLOR
        edge_widths[edge] = PATH_EDGE_WIDTH

    # Highlight considered or relaxed edge
    if considered_edge:
        edge = tuple(sorted(considered_edge))
        edge_colors[edge] = CONSIDER_EDGE_COLOR
        edge_widths[edge] = CONSIDER_EDGE_WIDTH
    if relaxed_edge:
        edge = tuple(sorted(relaxed_edge))
        edge_colors[edge] = RELAX_EDGE_COLOR
        edge_widths[edge] = PATH_EDGE_WIDTH # Relaxed edge becomes part of the path

    # Create node labels with current distances
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

    # Validate non-negative weights
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

    # Initial state
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

        # Event: Visiting a new node
        yield Event(
            step=step_count,
            type="visit",
            details=f"Visiting node {current_node} (distance: {current_distance})",
            data=_create_visual_state(graph, distances, visited, path, current_node=current_node)
        )
        step_count += 1

        for neighbor, weight in sorted(graph.get(current_node, []), key=lambda x: x[0]):
            if neighbor not in visited:
                # Event: Considering an edge
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
                    old_distance = distances[neighbor]
                    distances[neighbor] = new_distance
                    path[neighbor] = current_node
                    heapq.heappush(priority_queue, (new_distance, neighbor))

                    # Event: Relaxing an edge
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

    # Final state
    yield Event(
        step=step_count,
        type="done",
        details="Dijkstra's algorithm completed",
        data=_create_visual_state(graph, distances, visited, path)
    )

if __name__ == '__main__':
    example_graph = {
        'A': [('B', 4), ('C', 2)],
        'B': [('A', 4), ('E', 3)],
        'C': [('A', 2), ('D', 2), ('F', 4)],
        'D': [('C', 2), ('E', 3)],
        'E': [('B', 3), ('D', 3), ('F', 1)],
        'F': [('C', 4), ('E', 1)]
    }
    start_node = 'A'

    print(f"Running Dijkstra's from node {start_node} on example graph:")
    events = list(dijkstra_generator(example_graph, start_node))

    print("\n--- Events ---")
    for i, event in enumerate(events):
        print(f"Step {i}: {event.type} - {event.details}")
        # print(event.to_json_serializable()) # Uncomment for full data

    final_event = events[-1]
    final_data = final_event.data
    final_distances = {
        node: float(label.split('\n(')[1][:-1]) if '∞' not in label else float('inf')
        for node, label in final_data['node_labels'].items()
    }
    print("\n--- Final Distances ---")
    print(final_distances)

    expected_distances = {'A': 0, 'B': 4, 'C': 2, 'D': 4, 'E': 7, 'F': 6}
    assert final_distances == expected_distances
    print("Assertion passed: Final distances are correct.")

    # Test with negative weight
    negative_weight_graph = {'A': [('B', -1)], 'B': []}
    events_negative = list(dijkstra_generator(negative_weight_graph, 'A'))
    assert any(e.type == "error" for e in events_negative)
    print("Negative weight test passed.")

