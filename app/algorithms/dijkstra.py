from typing import List, Generator, Any, Dict, Tuple
from app.utils.types import Event, Graph
import heapq

def dijkstra_generator(graph: Graph, start_node: Any) -> Generator[Event, None, None]:
    """Generates events for visualizing Dijkstra's algorithm for Single Source Shortest Path (SSSP).

    Args:
        graph (Graph): The graph represented as an adjacency list
                       (e.g., {"A": [("B", 1)], "B": [("A", 1)]}).
        start_node (Any): The starting node for finding shortest paths.

    Yields:
        Event: An event object representing a step in the algorithm.
    """
    step_count = 0
    if not graph or start_node not in graph:
        yield Event(
            step=step_count,
            type="error",
            details=f"Start node {start_node} not found in graph or graph is empty.",
            data={"graph_snapshot": graph, "start_node": start_node}
        )
        step_count += 1
        yield Event(
            step=step_count,
            type="done",
            details="Dijkstra's algorithm aborted due to invalid start node or empty graph.",
            data={}
        )
        return

    distances = {node: float("inf") for node in graph}
    distances[start_node] = 0
    priority_queue = [(0, start_node)] # (distance, node)

    visited = set()
    path = {node: None for node in graph}

    # Initial snapshot
    yield Event(
        step=step_count,
        type="snapshot",
        details=f"Initial graph state, starting from {start_node}",
        data={"graph_snapshot": graph, "distances": {k: (v if v != float('inf') else 'inf') for k, v in distances.items()}, "start_node": start_node}
    )
    step_count += 1

    # Validate non-negative weights
    for u in graph:
        for v, weight in graph[u]:
            if weight < 0:
                yield Event(
                    step=step_count,
                    type="error",
                    details=f"Negative weight detected on edge {u}-{v}. Dijkstra's does not support negative weights.",
                    data={"u": u, "v": v, "weight": weight}
                )
                step_count += 1
                yield Event(
                    step=step_count,
                    type="done",
                    details="Dijkstra's algorithm aborted due to negative weights.",
                    data={}
                )
                return # Abort if negative weight found

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node in visited:
            continue

        visited.add(current_node)

        yield Event(
            step=step_count,
            type="visit",
            details=f"Visiting node {current_node} with distance {current_distance}",
            data={"u": current_node, "distance": current_distance, "distances": {k: (v if v != float('inf') else 'inf') for k, v in distances.items()}, "graph_snapshot": graph}
        )
        step_count += 1

        for neighbor, weight in graph.get(current_node, []):
            yield Event(
                step=step_count,
                type="consider_edge",
                details=f"Considering edge {current_node}-{neighbor} with weight {weight}",
                data={"u": current_node, "v": neighbor, "weight": weight, "distances": {k: (v if v != float('inf') else 'inf') for k, v in distances.items()}, "graph_snapshot": graph}
            )
            step_count += 1

            if neighbor not in visited:
                new_distance = current_distance + weight
                if new_distance < distances[neighbor]:
                    old_distance = distances[neighbor]
                    distances[neighbor] = new_distance
                    path[neighbor] = current_node
                    heapq.heappush(priority_queue, (new_distance, neighbor))

                    yield Event(
                        step=step_count,
                        type="relax",
                        details=f"Relaxing edge {current_node}-{neighbor}. New distance to {neighbor} is {new_distance}",
                        data={"u": current_node, "v": neighbor, "weight": weight, "old_distance": (old_distance if old_distance != float('inf') else 'inf'), "new_distance": new_distance, "distances": {k: (v if v != float('inf') else 'inf') for k, v in distances.items()}, "graph_snapshot": graph}
                    )
                    step_count += 1

    yield Event(
        step=step_count,
        type="done",
        details="Dijkstra's algorithm completed",
        data={"final_distances": {k: (v if v != float('inf') else 'inf') for k, v in distances.items()}, "final_paths": path, "graph_snapshot": graph}
    )


if __name__ == '__main__':
    # Example graph from a common Dijkstra's visualization
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
    for event in events:
        print(event.to_json_serializable())

    print("\n--- Final Distances ---")
    final_event = next(e for e in reversed(events) if e.type == "done")
    print(final_event.data["final_distances"])

    expected_distances = {'A': 0, 'B': 4, 'C': 2, 'D': 4, 'E': 7, 'F': 6}
    assert final_event.data["final_distances"] == expected_distances
    print("Assertion passed: Final distances are correct.")

    # Test with negative weight (should abort)
    negative_weight_graph = {
        'A': [('B', -1)],
        'B': [('C', 2)],
        'C': []
    }
    print("\nRunning Dijkstra's on graph with negative weight:")
    events_negative = list(dijkstra_generator(negative_weight_graph, 'A'))
    assert any(e.type == "error" for e in events_negative)
    assert events_negative[-1].details == "Dijkstra's algorithm aborted due to negative weights."
    print("Negative weight test passed (algorithm aborted as expected).")

