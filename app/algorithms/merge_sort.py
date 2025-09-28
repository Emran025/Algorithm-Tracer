from typing import List, Generator, Any, Set, Dict, Optional, Tuple
from app.utils.types import Event, Array

# --- Visualization Constants ---
DEFAULT_COLOR = "skyblue"
LEFT_PARTITION_COLOR = "#add8e6"   # Light blue for the left sub-array
RIGHT_PARTITION_COLOR = "#ffb6c1" # Light pink for the right sub-array
COMPARE_COLOR = "#ff9933"         # Orange for elements being compared
COPY_BACK_COLOR = "#9370db"       # Medium purple for the element being copied back
SORTED_COLOR = "#66cc66"          # Green for the final sorted array

def _create_visual_state(
    arr: Array,
    sorted_range: Optional[Tuple[int, int]] = None,
    left_partition: Optional[Tuple[int, int]] = None,
    right_partition: Optional[Tuple[int, int]] = None,
    compare_indices: Optional[Tuple[int, int]] = None,
    copy_back_index: Optional[int] = None,
) -> Dict[str, Any]:
    """Creates a rich visual state for the array at each step of Merge Sort."""
    n = len(arr)
    bar_colors = [DEFAULT_COLOR] * n

    if left_partition:
        low, high = left_partition
        for i in range(low, high + 1): bar_colors[i] = LEFT_PARTITION_COLOR
    if right_partition:
        low, high = right_partition
        for i in range(low, high + 1): bar_colors[i] = RIGHT_PARTITION_COLOR

    if compare_indices:
        i, j = compare_indices
        bar_colors[i] = COMPARE_COLOR
        bar_colors[j] = COMPARE_COLOR

    if copy_back_index is not None:
        bar_colors[copy_back_index] = COPY_BACK_COLOR

    if sorted_range:
        low, high = sorted_range
        for i in range(low, high + 1): bar_colors[i] = SORTED_COLOR

    state = {"array": list(arr), "bar_colors": bar_colors}
    if compare_indices:
        state["compare_indices"] = compare_indices
    return state

def merge_sort_generator(arr: Array) -> Generator[Event, None, None]:
    """Generates events for visualizing the Merge Sort algorithm with rich visual metadata."""
    n = len(arr)
    current_arr = list(arr)
    step_count = 0

    yield Event(
        step=step_count, type="start", details="Initial array state",
        data=_create_visual_state(current_arr)
    )
    step_count += 1

    def _merge_sort(sub_arr: Array, left: int, right: int) -> Generator[Event, None, None]:
        nonlocal step_count
        if left < right:
            mid = (left + right) // 2

            yield Event(
                step=step_count, type="divide", details=f"Dividing into partitions [{left}-{mid}] and [{mid+1}-{right}]",
                data=_create_visual_state(
                    sub_arr, left_partition=(left, mid), right_partition=(mid + 1, right)
                )
            )
            step_count += 1

            yield from _merge_sort(sub_arr, left, mid)
            yield from _merge_sort(sub_arr, mid + 1, right)
            yield from _merge(sub_arr, left, mid, right)

    def _merge(sub_arr: Array, left: int, mid: int, right: int) -> Generator[Event, None, None]:
        nonlocal step_count

        yield Event(
            step=step_count, type="merge", details=f"Merging partitions [{left}-{mid}] and [{mid+1}-{right}]",
            data=_create_visual_state(
                sub_arr, left_partition=(left, mid), right_partition=(mid + 1, right)
            )
        )
        step_count += 1

        left_copy = sub_arr[left : mid + 1]
        right_copy = sub_arr[mid + 1 : right + 1]
        # Snapshot for consistent visualization during comparisons
        arr_before_merge = list(sub_arr)

        i = 0  # Pointer for left_copy
        j = 0  # Pointer for right_copy
        k = left # Pointer for main array

        while i < len(left_copy) and j < len(right_copy):
            yield Event(
                step=step_count, type="compare",
                details=f"Comparing {left_copy[i]} and {right_copy[j]}",
                data=_create_visual_state(
                    arr_before_merge,  # Use the snapshot for the comparison view
                    left_partition=(left, mid), right_partition=(mid + 1, right),
                    compare_indices=(left + i, mid + 1 + j)
                )
            )
            step_count += 1

            if left_copy[i] <= right_copy[j]:
                sub_arr[k] = left_copy[i]
                i += 1
            else:
                sub_arr[k] = right_copy[j]
                j += 1

            yield Event(
                step=step_count, type="copy_back", details=f"Copying {sub_arr[k]} to sorted position {k}",
                data=_create_visual_state(
                    sub_arr, left_partition=(left, mid), right_partition=(mid + 1, right),
                    copy_back_index=k
                )
            )
            step_count += 1
            k += 1

        while i < len(left_copy):
            sub_arr[k] = left_copy[i]
            yield Event(
                step=step_count, type="copy_back", details=f"Copying remaining {sub_arr[k]} to position {k}",
                data=_create_visual_state(
                    sub_arr, left_partition=(left, mid), right_partition=(mid + 1, right),
                    copy_back_index=k
                )
            )
            step_count += 1
            i += 1
            k += 1

        while j < len(right_copy):
            sub_arr[k] = right_copy[j]
            yield Event(
                step=step_count, type="copy_back", details=f"Copying remaining {sub_arr[k]} to position {k}",
                data=_create_visual_state(
                    sub_arr, left_partition=(left, mid), right_partition=(mid + 1, right),
                    copy_back_index=k
                )
            )
            step_count += 1
            j += 1
            k += 1

        yield Event(
            step=step_count, type="sorted", details=f"Partition [{left}-{right}] is now sorted",
            data=_create_visual_state(sub_arr, sorted_range=(left, right))
        )
        step_count += 1

    yield from _merge_sort(current_arr, 0, n - 1)

    yield Event(
        step=step_count, type="done", details="Merge Sort completed",
        data=_create_visual_state(current_arr, sorted_range=(0, n - 1))
    )

if __name__ == '__main__':
    test_array = [38, 27, 43, 3, 9, 82, 10]
    print(f"Original array: {test_array}")
    events = list(merge_sort_generator(test_array))

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

    assert all(c == SORTED_COLOR for c in final_data["bar_colors"])
    print("Assertion passed: Final state has all bars colored as sorted.")
