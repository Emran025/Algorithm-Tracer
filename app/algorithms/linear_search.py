from typing import List, Generator, Any
from app.utils.types import Event, Array

def linear_search_generator(arr: Array, target: Any) -> Generator[Event, None, None]:
    """Generates events for visualizing the Linear Search algorithm.

    Args:
        arr (Array): The list of elements to search through.
        target (Any): The element to search for.

    Yields:
        Event: An event object representing a step in the algorithm.
    """
    step_count = 0
    n = len(arr)
    found = False

    yield Event(
        step=step_count,
        type="snapshot",
        details=f"Initial array state, searching for {target}",
        data={"array_snapshot": list(arr), "target": target}
    )
    step_count += 1

    for i in range(n):
        yield Event(
            step=step_count,
            type="visit",
            details=f"Visiting index {i}, comparing {arr[i]} with target {target}",
            data={"index": i, "value": arr[i], "target": target, "array_snapshot": list(arr)}
        )
        step_count += 1

        if arr[i] == target:
            yield Event(
                step=step_count,
                type="found",
                details=f"Target {target} found at index {i}",
                data={"index": i, "value": arr[i], "target": target, "array_snapshot": list(arr)}
            )
            step_count += 1
            found = True
            break

    if not found:
        yield Event(
            step=step_count,
            type="not_found",
            details=f"Target {target} not found in the array",
            data={"target": target, "array_snapshot": list(arr)}
        )
        step_count += 1

    yield Event(
        step=step_count,
        type="done",
        details="Linear Search completed",
        data={"found": found, "target": target, "final_array": list(arr)}
    )


if __name__ == '__main__':
    test_array = [38, 27, 43, 3, 9, 82, 10]
    target_found = 9
    target_not_found = 100

    print(f"Searching for {target_found} in {test_array}")
    events_found = list(linear_search_generator(test_array, target_found))
    for event in events_found:
        print(event.to_json_serializable())
    final_event_found = events_found[-1]
    assert final_event_found.data["found"] is True
    print("Found test passed.")

    print(f"\nSearching for {target_not_found} in {test_array}")
    events_not_found = list(linear_search_generator(test_array, target_not_found))
    for event in events_not_found:
        print(event.to_json_serializable())
    final_event_not_found = events_not_found[-1]
    assert final_event_not_found.data["found"] is False
    print("Not found test passed.")

