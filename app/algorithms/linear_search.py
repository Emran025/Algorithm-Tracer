from typing import List, Generator, Any, Dict, Optional
from app.utils.types import Event, Array

# --- Visualization Constants ---
DEFAULT_COLOR = "skyblue"
VISITED_COLOR = "#ff9933"  # Orange for the element being visited/compared
FOUND_COLOR = "#66cc66"    # Green for the found element

def _create_visual_state(
    arr: Array,
    visited_index: Optional[int] = None,
    found_index: Optional[int] = None,
) -> Dict[str, Any]:
    """Creates a rich visual state for the array at each step of Linear Search."""
    bar_colors = [DEFAULT_COLOR] * len(arr)

    if visited_index is not None:
        bar_colors[visited_index] = VISITED_COLOR

    if found_index is not None:
        bar_colors[found_index] = FOUND_COLOR

    return {"array": list(arr), "bar_colors": bar_colors}

def linear_search_generator(arr: Array, target: Any) -> Generator[Event, None, None]:
    """Generates events for visualizing the Linear Search algorithm with rich visual metadata."""
    step_count = 0
    n = len(arr)
    found_at_index = -1

    yield Event(
        step=step_count, type="start", details=f"Starting search for {target}",
        data=_create_visual_state(arr)
    )
    step_count += 1

    for i in range(n):
        yield Event(
            step=step_count, type="visit", details=f"Checking index {i} (value: {arr[i]})",
            data=_create_visual_state(arr, visited_index=i)
        )
        step_count += 1

        if arr[i] == target:
            found_at_index = i
            yield Event(
                step=step_count, type="found", details=f"Target {target} found at index {i}",
                data=_create_visual_state(arr, found_index=i)
            )
            step_count += 1
            break

    if found_at_index == -1:
        yield Event(
            step=step_count, type="not_found", details=f"Target {target} not found",
            data=_create_visual_state(arr) # Final state, no highlights
        )
        step_count += 1

    final_data = _create_visual_state(arr, found_index=found_at_index if found_at_index != -1 else None)
    final_data["found"] = found_at_index != -1
    if found_at_index != -1:
        final_data["found_index"] = found_at_index

    yield Event(
        step=step_count, type="done", details="Search completed",
        data=final_data
    )

if __name__ == '__main__':
    test_array = [38, 27, 43, 3, 9, 82, 10]
    target_found = 9
    target_not_found = 100

    # --- Test Case 1: Target Found ---
    print(f"Searching for {target_found} in {test_array}")
    events_found = list(linear_search_generator(test_array, target_found))

    print(f"\n--- Generated {len(events_found)} events (found case) ---")
    for i, event in enumerate(events_found):
        print(f"Step {i}: {event.type} - {event.details}")
        assert "bar_colors" in event.data and "array" in event.data

    final_event_found = events_found[-1]
    found_event = events_found[-2]

    assert found_event.type == "found"
    assert final_event_found.type == "done"
    assert final_event_found.data["bar_colors"][test_array.index(target_found)] == FOUND_COLOR
    print("Found test passed.")

    # --- Test Case 2: Target Not Found ---
    print(f"\nSearching for {target_not_found} in {test_array}")
    events_not_found = list(linear_search_generator(test_array, target_not_found))

    print(f"\n--- Generated {len(events_not_found)} events (not found case) ---")
    for i, event in enumerate(events_not_found):
        print(f"Step {i}: {event.type} - {event.details}")
        assert "bar_colors" in event.data and "array" in event.data

    final_event_not_found = events_not_found[-1]
    not_found_event = events_not_found[-2]

    assert not_found_event.type == "not_found"
    assert final_event_not_found.type == "done"
    assert all(c == DEFAULT_COLOR for c in final_event_not_found.data["bar_colors"])
    print("Not found test passed.")

