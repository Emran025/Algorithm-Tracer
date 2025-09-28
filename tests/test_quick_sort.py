import pytest
from app.algorithms.quick_sort import quick_sort_generator
from app.utils.types import Event, Array

def test_quick_sort_basic():
    """Test quick sort with a basic array."""
    arr = [10, 7, 8, 9, 1, 5]
    expected_sorted_arr = sorted(arr)
    events = list(quick_sort_generator(list(arr))) # Pass a copy

    assert len(events) > 0, "No events were generated."

    final_event = events[-1]
    assert final_event.type == "done"
    assert "array" in final_event.data
    assert final_event.data["array"] == expected_sorted_arr

    for event in events:
        assert isinstance(event, Event)
        assert isinstance(event.step, int)
        assert isinstance(event.type, str)
        assert isinstance(event.details, str)
        assert isinstance(event.data, dict)

def test_quick_sort_empty_array():
    """Test quick sort with an empty array."""
    arr = []
    expected_sorted_arr = []
    events = list(quick_sort_generator(list(arr)))

    assert len(events) > 0, "No events were generated for empty array."
    final_event = events[-1]
    assert final_event.type == "done"
    assert "array" in final_event.data
    assert final_event.data["array"] == expected_sorted_arr

def test_quick_sort_single_element_array():
    """Test quick sort with a single-element array."""
    arr = [5]
    expected_sorted_arr = [5]
    events = list(quick_sort_generator(list(arr)))

    assert len(events) > 0, "No events were generated for single element array."
    final_event = events[-1]
    assert final_event.type == "done"
    assert "array" in final_event.data
    assert final_event.data["array"] == expected_sorted_arr

def test_quick_sort_already_sorted_array():
    """Test quick sort with an already sorted array."""
    arr = [1, 2, 3, 4, 5]
    expected_sorted_arr = [1, 2, 3, 4, 5]
    events = list(quick_sort_generator(list(arr)))

    assert len(events) > 0, "No events were generated for sorted array."
    final_event = events[-1]
    assert final_event.type == "done"
    assert "array" in final_event.data
    assert final_event.data["array"] == expected_sorted_arr

def test_quick_sort_reverse_sorted_array():
    """Test quick sort with a reverse sorted array."""
    arr = [5, 4, 3, 2, 1]
    expected_sorted_arr = [1, 2, 3, 4, 5]
    events = list(quick_sort_generator(list(arr)))

    assert len(events) > 0, "No events were generated for reverse sorted array."
    final_event = events[-1]
    assert final_event.type == "done"
    assert "array" in final_event.data
    assert final_event.data["array"] == expected_sorted_arr

def test_quick_sort_duplicate_elements():
    """Test quick sort with an array containing duplicate elements."""
    arr = [3, 1, 4, 1, 5, 9, 2, 6]
    expected_sorted_arr = sorted(arr)
    events = list(quick_sort_generator(list(arr)))

    assert len(events) > 0, "No events were generated for array with duplicates."
    final_event = events[-1]
    assert final_event.type == "done"
    assert "array" in final_event.data
    assert final_event.data["array"] == expected_sorted_arr