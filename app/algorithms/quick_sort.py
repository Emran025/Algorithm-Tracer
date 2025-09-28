from typing import List, Generator, Any, Set, Dict, Optional, Tuple
from app.utils.types import Event, Array

# --- Visualization Constants ---
DEFAULT_COLOR = "skyblue"
PARTITION_COLOR = "#cccccc"  # Light grey for the current partition
PIVOT_COLOR = "#9370db"      # Medium purple for the pivot
COMPARE_COLOR = "#ff9933"    # Orange for elements being compared
SWAP_COLOR = "#ff6666"       # Red for elements being swapped
SORTED_COLOR = "#66cc66"     # Green for sorted elements

def _create_visual_state(
    arr: Array,
    sorted_indices: Set[int],
    partition_range: Optional[Tuple[int, int]] = None,
    pivot_index: Optional[int] = None,
    compare_indices: Optional[Tuple[int, int]] = None,
    swap_indices: Optional[Tuple[int, int]] = None,
) -> Dict[str, Any]:
    """Creates a rich visual state for the array at each step."""
    bar_colors = [DEFAULT_COLOR] * len(arr)

    # Color the current partition first
    if partition_range:
        low, high = partition_range
        for i in range(low, high + 1):
            bar_colors[i] = PARTITION_COLOR

    # Then, color specific roles with higher precedence
    if pivot_index is not None:
        bar_colors[pivot_index] = PIVOT_COLOR
    if compare_indices:
        i, j = compare_indices
        bar_colors[i] = COMPARE_COLOR
        # Don't overwrite pivot color if it's being compared
        if bar_colors[j] != PIVOT_COLOR:
            bar_colors[j] = COMPARE_COLOR
    if swap_indices:
        i, j = swap_indices
        bar_colors[i] = SWAP_COLOR
        bar_colors[j] = SWAP_COLOR

    # Sorted elements have the highest precedence
    for i in sorted_indices:
        bar_colors[i] = SORTED_COLOR

    return {"array": list(arr), "bar_colors": bar_colors}

def quick_sort_generator(arr: Array) -> Generator[Event, None, None]:
    """Generates events for visualizing the Quick Sort algorithm with rich visual metadata."""
    n = len(arr)
    current_arr = list(arr)
    sorted_indices: Set[int] = set()
    step_count = 0

    yield Event(
        step=step_count, type="start", details="Initial array state",
        data=_create_visual_state(current_arr, sorted_indices)
    )
    step_count += 1

    def _partition_generator(low: int, high: int) -> Generator[Event, None, int]:
        nonlocal step_count
        pivot_val = current_arr[high]
        pivot_idx = high

        yield Event(
            step=step_count, type="set_pivot", details=f"Setting pivot to {pivot_val}",
            data=_create_visual_state(
                current_arr, sorted_indices, partition_range=(low, high), pivot_index=pivot_idx
            )
        )
        step_count += 1

        i = low - 1
        for j in range(low, high):
            yield Event(
                step=step_count, type="compare",
                details=f"Comparing {current_arr[j]} with pivot {pivot_val}",
                data=_create_visual_state(
                    current_arr, sorted_indices, partition_range=(low, high), pivot_index=pivot_idx,
                    compare_indices=(j, pivot_idx)
                )
            )
            step_count += 1

            if current_arr[j] <= pivot_val:
                i += 1
                if i != j:
                    yield Event(
                        step=step_count, type="swap",
                        details=f"Swapping {current_arr[i]} and {current_arr[j]}",
                        data=_create_visual_state(
                            current_arr, sorted_indices, partition_range=(low, high), pivot_index=pivot_idx,
                            swap_indices=(i, j)
                        )
                    )
                    step_count += 1
                    current_arr[i], current_arr[j] = current_arr[j], current_arr[i]

        final_pivot_pos = i + 1
        yield Event(
            step=step_count, type="swap",
            details=f"Placing pivot {pivot_val} at its correct position {final_pivot_pos}",
            data=_create_visual_state(
                current_arr, sorted_indices, partition_range=(low, high), pivot_index=pivot_idx,
                swap_indices=(final_pivot_pos, high)
            )
        )
        step_count += 1
        current_arr[final_pivot_pos], current_arr[high] = current_arr[high], current_arr[final_pivot_pos]
        return final_pivot_pos

    def _quick_sort(low: int, high: int) -> Generator[Event, None, None]:
        nonlocal step_count
        if low < high:
            yield Event(
                step=step_count, type="partition",
                details=f"Partitioning sub-array from index {low} to {high}",
                data=_create_visual_state(current_arr, sorted_indices, partition_range=(low, high))
            )
            step_count += 1

            pi = yield from _partition_generator(low, high)

            sorted_indices.add(pi)
            yield Event(
                step=step_count, type="sorted",
                details=f"Element {current_arr[pi]} at index {pi} is now sorted",
                data=_create_visual_state(current_arr, sorted_indices)
            )
            step_count += 1

            yield from _quick_sort(low, pi - 1)
            yield from _quick_sort(pi + 1, high)
        elif low == high: # A single-element partition is inherently sorted
            sorted_indices.add(low)
            yield Event(
                step=step_count, type="sorted",
                details=f"Element {current_arr[low]} at index {low} is sorted (single-element partition)",
                data=_create_visual_state(current_arr, sorted_indices)
            )
            step_count += 1

    yield from _quick_sort(0, n - 1)

    yield Event(
        step=step_count, type="done", details="Quick Sort completed",
        data=_create_visual_state(current_arr, sorted_indices)
    )

if __name__ == '__main__':
    test_array = [3, 1, 4, 1, 5, 9, 2, 6]
    print(f"Original array: {test_array}")
    events = list(quick_sort_generator(test_array))

    print(f"\n--- Generated {len(events)} events ---")
    for i, event in enumerate(events):
        print(f"Step {i}: {event.type} - {event.details}")
        assert "bar_colors" in event.data, f"Event {i} is missing 'bar_colors'"
        assert "array" in event.data, f"Event {i} is missing 'array'"
    print("All events contain rich visual data.")

    final_event = events[-1]
    final_data = final_event.data
    print("\n--- Final Array ---")
    print(final_data["array"])

    assert final_data["array"] == sorted(test_array)
    print("Assertion passed: Array is sorted correctly.")

    # Check that all bars are green in the final state
    assert all(c == SORTED_COLOR for c in final_data["bar_colors"])
    print("Assertion passed: Final state has all bars colored as sorted.")
