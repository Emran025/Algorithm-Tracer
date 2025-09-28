from typing import List, Generator, Any
from app.utils.types import Event, Array

def quick_sort_generator(arr: Array) -> Generator[Event, None, None]:
    """Generates events for visualizing the Quick Sort algorithm.

    Args:
        arr (Array): The list of numbers to be sorted.

    Yields:
        Event: An event object representing a step in the algorithm.
    """
    n = len(arr)
    current_arr = list(arr) # Work on a copy
    step_count = 0

    yield Event(
        step=step_count,
        type="snapshot",
        details="Initial array state",
        data={"array_snapshot": list(current_arr)}
    )
    step_count += 1

    def _partition(low: int, high: int) -> int:
        nonlocal step_count
        pivot = current_arr[high] # Choose the last element as the pivot
        pivot_index = high

        yield Event(
            step=step_count,
            type="set_pivot",
            details=f"Setting pivot to {pivot} at index {pivot_index}",
            data={"index": pivot_index, "value": pivot, "array_snapshot": list(current_arr)}
        )
        step_count += 1

        i = low - 1
        for j in range(low, high):
            yield Event(
                step=step_count,
                type="compare",
                details=f"Comparing arr[{j}] ({current_arr[j]}) with pivot {pivot}",
                data={"i": j, "j": pivot_index, "value_i": current_arr[j], "value_j": pivot, "array_snapshot": list(current_arr)}
            )
            step_count += 1

            if current_arr[j] <= pivot:
                i += 1
                current_arr[i], current_arr[j] = current_arr[j], current_arr[i]
                yield Event(
                    step=step_count,
                    type="swap",
                    details=f"Swapping arr[{i}] ({current_arr[j]}) and arr[{j}] ({current_arr[i]})",
                    data={"i": i, "j": j, "array_snapshot": list(current_arr)}
                )
                step_count += 1

        current_arr[i + 1], current_arr[high] = current_arr[high], current_arr[i + 1]
        yield Event(
            step=step_count,
            type="swap",
            details=f"Swapping pivot {pivot} with arr[{i + 1}] ({current_arr[high]})",
            data={"i": i + 1, "j": high, "array_snapshot": list(current_arr)}
        )
        step_count += 1

        return i + 1

    def _quick_sort(low: int, high: int) -> None:
        nonlocal step_count
        if low < high:
            yield Event(
                step=step_count,
                type="divide",
                details=f"QuickSort on sub-array from index {low} to {high}",
                data={"low": low, "high": high, "array_snapshot": list(current_arr)}
            )
            step_count += 1

            pi = yield from _partition_generator(low, high) # Use yield from for sub-generator

            yield from _quick_sort(low, pi - 1)
            yield from _quick_sort(pi + 1, high)

    # Wrapper for partition to make it a generator
    def _partition_generator(low: int, high: int) -> Generator[Event, None, int]:
        nonlocal step_count
        pivot_val = current_arr[high]
        pivot_idx = high

        yield Event(
            step=step_count,
            type="set_pivot",
            details=f"Setting pivot to {pivot_val} at index {pivot_idx}",
            data={"index": pivot_idx, "value": pivot_val, "array_snapshot": list(current_arr)}
        )
        step_count += 1

        i = low - 1
        for j in range(low, high):
            yield Event(
                step=step_count,
                type="compare",
                details=f"Comparing arr[{j}] ({current_arr[j]}) with pivot {pivot_val}",
                data={"i": j, "j": pivot_idx, "value_i": current_arr[j], "value_j": pivot_val, "array_snapshot": list(current_arr)}
            )
            step_count += 1

            if current_arr[j] <= pivot_val:
                i += 1
                if i != j:
                    current_arr[i], current_arr[j] = current_arr[j], current_arr[i]
                    yield Event(
                        step=step_count,
                        type="swap",
                        details=f"Swapping arr[{i}] ({current_arr[i]}) and arr[{j}] ({current_arr[j]})",
                        data={"i": i, "j": j, "array_snapshot": list(current_arr)}
                    )
                    step_count += 1

        current_arr[i + 1], current_arr[high] = current_arr[high], current_arr[i + 1]
        yield Event(
            step=step_count,
            type="swap",
            details=f"Placing pivot {pivot_val} at its correct position arr[{i + 1}]",
            data={"i": i + 1, "j": high, "array_snapshot": list(current_arr)}
        )
        step_count += 1
        return i + 1


    yield from _quick_sort(0, n - 1)

    yield Event(
        step=step_count,
        type="done",
        details="Quick Sort completed",
        data={"sorted_array": list(current_arr)}
    )


if __name__ == '__main__':
    test_array = [3,1,4,1,5,9,2,6]
    print(f"Original array: {test_array}")
    events = list(quick_sort_generator(test_array))

    print("\n--- Events ---")
    for event in events:
        print(event.to_json_serializable())

    print("\n--- Final Array ---")
    final_array_event = next(e for e in reversed(events) if e.type == "done")
    print(final_array_event.data["sorted_array"])
    assert final_array_event.data["sorted_array"] == sorted([3,1,4,1,5,9,2,6])
    print("Assertion passed: Array is sorted correctly.")

    test_array_2 = [3, 1, 4, 1, 5, 9, 2, 6]
    print(f"\nOriginal array 2: {test_array_2}")
    events_2 = list(quick_sort_generator(test_array_2))
    final_array_event_2 = next(e for e in reversed(events_2) if e.type == "done")
    assert final_array_event_2.data["sorted_array"] == sorted([3, 1, 4, 1, 5, 9, 2, 6])
    print("Assertion 2 passed: Array is sorted correctly.")
