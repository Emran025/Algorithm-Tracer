from typing import List, Generator, Any
from app.utils.types import Event, Array

def merge_sort_generator(arr: Array) -> Generator[Event, None, None]:
    """Generates events for visualizing the Merge Sort algorithm.

    Args:
        arr (Array): The list of numbers to be sorted.

    Yields:
        Event: An event object representing a step in the algorithm.
    """
    n = len(arr)
    temp_arr = list(arr) # Create a temporary array for merging
    step_count = 0

    yield Event(
        step=step_count,
        type="snapshot",
        details="Initial array state",
        data={"array_snapshot": list(arr)}
    )
    step_count += 1

    def _merge_sort(current_arr: Array, left: int, right: int) -> None:
        nonlocal step_count
        if left < right:
            mid = (left + right) // 2

            yield Event(
                step=step_count,
                type="divide",
                details=f"Dividing array from index {left} to {right} into two halves",
                data={"left": left, "right": right, "mid": mid, "array_snapshot": list(current_arr)}
            )
            step_count += 1

            yield from _merge_sort(current_arr, left, mid)
            yield from _merge_sort(current_arr, mid + 1, right)

            yield from _merge(current_arr, left, mid, right)

    def _merge(current_arr: Array, left: int, mid: int, right: int) -> Generator[Event, None, None]:
        nonlocal step_count
        i = left
        j = mid + 1
        k = left

        yield Event(
            step=step_count,
            type="merge_start",
            details=f"Starting merge for sub-array from {left} to {right}",
            data={"left": left, "mid": mid, "right": right, "array_snapshot": list(current_arr)}
        )
        step_count += 1

        while i <= mid and j <= right:
            yield Event(
                step=step_count,
                type="compare",
                details=f"Comparing elements at index {i} ({current_arr[i]}) and {j} ({current_arr[j]})",
                data={"i": i, "j": j, "value_i": current_arr[i], "value_j": current_arr[j], "array_snapshot": list(current_arr)}
            )
            step_count += 1

            if current_arr[i] <= current_arr[j]:
                temp_arr[k] = current_arr[i]
                yield Event(
                    step=step_count,
                    type="overwrite",
                    details=f"Overwriting temp_arr[{k}] with current_arr[{i}] ({current_arr[i]})",
                    data={"index": k, "value": current_arr[i], "source_index": i, "array_snapshot": list(current_arr)}
                )
                step_count += 1
                i += 1
            else:
                temp_arr[k] = current_arr[j]
                yield Event(
                    step=step_count,
                    type="overwrite",
                    details=f"Overwriting temp_arr[{k}] with current_arr[{j}] ({current_arr[j]})",
                    data={"index": k, "value": current_arr[j], "source_index": j, "array_snapshot": list(current_arr)}
                )
                step_count += 1
                j += 1
            k += 1

        while i <= mid:
            temp_arr[k] = current_arr[i]
            yield Event(
                step=step_count,
                type="overwrite",
                details=f"Copying remaining element current_arr[{i}] ({current_arr[i]}) to temp_arr[{k}]",
                data={"index": k, "value": current_arr[i], "source_index": i, "array_snapshot": list(current_arr)}
            )
            step_count += 1
            i += 1
            k += 1

        while j <= right:
            temp_arr[k] = current_arr[j]
            yield Event(
                step=step_count,
                type="overwrite",
                details=f"Copying remaining element current_arr[{j}] ({current_arr[j]}) to temp_arr[{k}]",
                data={"index": k, "value": current_arr[j], "source_index": j, "array_snapshot": list(current_arr)}
            )
            step_count += 1
            j += 1
            k += 1

        for x in range(left, right + 1):
            current_arr[x] = temp_arr[x]
            yield Event(
                step=step_count,
                type="copy_back",
                details=f"Copying temp_arr[{x}] ({temp_arr[x]}) back to current_arr[{x}]",
                data={"index": x, "value": temp_arr[x], "array_snapshot": list(current_arr)}
            )
            step_count += 1

        yield Event(
            step=step_count,
            type="merge_end",
            details=f"Finished merging sub-array from {left} to {right}",
            data={"left": left, "right": right, "array_snapshot": list(current_arr)}
        )
        step_count += 1

    # Initial call to the recursive merge sort function
    yield from _merge_sort(arr, 0, n - 1)

    yield Event(
        step=step_count,
        type="done",
        details="Merge Sort completed",
        data={"sorted_array": list(arr)}
    )


if __name__ == '__main__':
    # Example usage and verification
    test_array = [38, 27, 43, 3, 9, 82, 10]
    print(f"Original array: {test_array}")
    events = list(merge_sort_generator(test_array))

    print("\n--- Events ---")
    for event in events:
        print(event.to_json_serializable())

    print("\n--- Final Array ---")
    final_array_event = next(e for e in reversed(events) if e.type == "done")
    print(final_array_event.data["sorted_array"])
    assert final_array_event.data["sorted_array"] == sorted([38, 27, 43, 3, 9, 82, 10])
    print("Assertion passed: Array is sorted correctly.")

