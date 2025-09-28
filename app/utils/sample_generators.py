import random
from typing import List, Any, Dict, Tuple

def generate_random_array(size: int, min_val: int, max_val: int) -> List[int]:
    """Generates a random array of integers.

    Args:
        size (int): The number of elements in the array.
        min_val (int): The minimum possible value for an element.
        max_val (int): The maximum possible value for an element.

    Returns:
        List[int]: A list of random integers.
    """
    return [random.randint(min_val, max_val) for _ in range(size)]

def generate_random_graph(num_nodes: int, density: float, weight_range: Tuple[int, int], directed: bool = False) -> Dict[Any, List[Tuple[Any, int]]]:
    """Generates a random graph as an adjacency list.

    Args:
        num_nodes (int): The number of nodes in the graph.
        density (float): The probability of an edge existing between any two nodes (0.0 to 1.0).
        weight_range (Tuple[int, int]): A tuple (min_weight, max_weight) for edge weights.
        directed (bool): If True, generates a directed graph; otherwise, an undirected graph.

    Returns:
        Dict[Any, List[Tuple[Any, int]]]: The generated graph as an adjacency list.
    """
    nodes = [chr(65 + i) for i in range(num_nodes)] # Use A, B, C...
    graph = {node: [] for node in nodes}

    min_w, max_w = weight_range

    for i in range(num_nodes):
        for j in range(num_nodes):
            if i == j: # No self-loops
                continue
            if random.random() < density:
                weight = random.randint(min_w, max_w)
                graph[nodes[i]].append((nodes[j], weight))
                if not directed:
                    # For undirected, ensure the reverse edge exists with the same weight
                    # and avoid adding duplicates if already added by j's iteration
                    if (nodes[i], weight) not in graph[nodes[j]]:
                        graph[nodes[j]].append((nodes[i], weight))
    return graph


if __name__ == '__main__':
    print("Generating random array:")
    random_arr = generate_random_array(10, 0, 100)
    print(random_arr)
    assert len(random_arr) == 10
    assert all(0 <= x <= 100 for x in random_arr)

    print("\nGenerating random undirected graph:")
    random_graph_undirected = generate_random_graph(5, 0.5, (1, 10), directed=False)
    print(random_graph_undirected)
    assert len(random_graph_undirected) == 5
    # Basic check for symmetry in undirected graph
    for u, neighbors in random_graph_undirected.items():
        for v, weight in neighbors:
            found_reverse = False
            for neighbor_of_v, weight_of_reverse in random_graph_undirected.get(v, []):
                if neighbor_of_v == u and weight_of_reverse == weight:
                    found_reverse = True
                    break
            assert found_reverse, f"Undirected graph not symmetric for edge {u}-{v}"

    print("\nGenerating random directed graph:")
    random_graph_directed = generate_random_graph(4, 0.7, (1, 20), directed=True)
    print(random_graph_directed)
    assert len(random_graph_directed) == 4
    # Basic check for asymmetry in directed graph (not strictly required, but good to check)
    for u, neighbors in random_graph_directed.items():
        for v, weight in neighbors:
            # Check if reverse edge exists, it shouldn't necessarily
            pass

    print("All sample generator tests passed.")

