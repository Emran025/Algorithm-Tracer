import pytest
import re
from app.algorithms.merge_sort import merge_sort_generator
from app.utils.types import Event

def test_merge_sort_visualization_consistency():
    """
    Tests that the visualization for 'compare' events in merge_sort_generator
    is consistent with the event's details. It ensures the array state shown
    during a comparison reflects the array *before* elements are moved.
    """
    # This array is specifically chosen to trigger the bug.
    # The first merge will be between [27] and [38], then [3] and [43].
    # The final merge of [27, 38] and [3, 43] will cause the issue.
    # When comparing 27 and 3, the visualization will be correct.
    # After 3 is copied to index 0, the next comparison is 27 and 43.
    # The bug will show the array state with 3 at index 0, but the indices
    # will still point to index 0 and index 2, showing a comparison
    # between 3 and 43 in the visualization, while the details say 27 and 43.
    test_array = [38, 27, 43, 3]

    events = list(merge_sort_generator(test_array))

    for event in events:
        if event.type == "compare":
            # Extract numbers from the details string, e.g., "Comparing 38 and 27"
            match = re.search(r"Comparing ([-?\d]+) and ([-?\d]+)", event.details)
            assert match, f"Could not parse details string: {event.details}"

            val1_from_details = int(match.group(1))
            val2_from_details = int(match.group(2))

            # Get the indices from the event data
            compare_indices = event.data.get("compare_indices")
            assert compare_indices, "Compare event is missing 'compare_indices' data"

            idx1, idx2 = compare_indices

            # Get the array state from the event data
            array_state = event.data.get("array")
            assert array_state, "Compare event is missing 'array' data"

            # Get the values from the array state using the indices
            val1_from_array = array_state[idx1]
            val2_from_array = array_state[idx2]

            # The core of the test: check for consistency
            # This set comparison handles cases where the order might differ.
            assert {val1_from_details, val2_from_details} == {val1_from_array, val2_from_array}, \
                f"Visualization mismatch at step {event.step}: Details say comparing {val1_from_details} and {val2_from_details}, " \
                f"but array at indices ({idx1}, {idx2}) shows ({val1_from_array}, {val2_from_array}). The array state was: {array_state}"