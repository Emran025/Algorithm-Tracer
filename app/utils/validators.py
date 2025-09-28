from typing import List, Any, Dict, Tuple

def validate_array_input(arr_str: str) -> List[int]:
    """Validates and converts a comma-separated string of integers to a list of ints.

    Args:
        arr_str (str): A comma-separated string of integers.

    Returns:
        List[int]: A list of integers.

    Raises:
        ValueError: If the input string is not a valid comma-separated list of integers.
    """
    if not arr_str.strip():
        return []
    try:
        return [int(x.strip()) for x in arr_str.split(",") if x.strip()]
    except ValueError:
        raise ValueError("Invalid array input. Please enter comma-separated integers.")

def validate_graph_input(graph_data: Dict[Any, List[Tuple[Any, int]]]) -> None:
    """Validates a graph represented as an adjacency list.

    Args:
        graph_data (Dict[Any, List[Tuple[Any, int]]]): The graph data.

    Raises:
        ValueError: If the graph data is invalid (e.g., negative weights, self-loops).
    """
    if not graph_data:
        return

    nodes = set(graph_data.keys())
    for u, neighbors in graph_data.items():
        if u not in nodes:
            raise ValueError(f"Node {u} in adjacency list key is not consistent.")
        for v, weight in neighbors:
            if v not in nodes:
                raise ValueError(f"Neighbor node {v} of {u} is not defined in the graph.")
            if not isinstance(weight, (int, float)) or weight < 0:
                raise ValueError(f"Edge {u}-{v} has invalid or negative weight: {weight}. Weights must be non-negative numbers.")
            if u == v:
                raise ValueError(f"Self-loop detected for node {u}. Self-loops are not supported.")


if __name__ == '__main__':
    # Test array validation
    print("Testing array validation...")
    try:
        arr = validate_array_input("1,2,3,4,5")
        print(f"Valid array: {arr}")
        assert arr == [1, 2, 3, 4, 5]

        arr = validate_array_input("  1 , 2, 3  ")
        print(f"Valid array with spaces: {arr}")
        assert arr == [1, 2, 3]

        arr = validate_array_input("")
        print(f"Empty array: {arr}")
        assert arr == []

        arr = validate_array_input("1,a,3")
    except ValueError as e:
        print(f"Expected error: {e}")
        assert str(e) == "Invalid array input. Please enter comma-separated integers."

    # Test graph validation
    print("\nTesting graph validation...")
    valid_graph = {
        "A": [("B", 1), ("C", 2)],
        "B": [("A", 1)],
        "C": [("A", 2)]
    }
    try:
        validate_graph_input(valid_graph)
        print("Valid graph.")

        invalid_graph_node = {
            "A": [("B", 1)],
            "B": [("D", 1)] # D is not defined
        }
        validate_graph_input(invalid_graph_node)
    except ValueError as e:
        print(f"Expected error: {e}")
        assert "Neighbor node D of B is not defined in the graph." in str(e)

    invalid_graph_weight = {
        "A": [("B", -1)],
        "B": [("A", 1)]
    }
    try:
        validate_graph_input(invalid_graph_weight)
    except ValueError as e:
        print(f"Expected error: {e}")
        assert "has invalid or negative weight" in str(e)

    invalid_graph_self_loop = {
        "A": [("A", 1)],
        "B": []
    }
    try:
        validate_graph_input(invalid_graph_self_loop)
    except ValueError as e:
        print(f"Expected error: {e}")
        assert "Self-loop detected for node A" in str(e)

    print("All validator tests completed.")

