import pytest
from app.algorithms.linear_search import linear_search_generator
from app.utils.types import Event

def test_linear_search_found():
    """Test linear search when the target is found."""
    arr = [10, 20, 30, 40, 50]
    target = 30
    events = list(linear_search_generator(list(arr), target))

    assert len(events) > 0
    final_event = events[-1]
    assert final_event.type == "done"
    assert final_event.data["found"] is True
    assert final_event.data["found_index"] == 2

    found_event = next((e for e in events if e.type == "found"), None)
    assert found_event is not None

def test_linear_search_not_found():
    """Test linear search when the target is not found."""
    arr = [10, 20, 30, 40, 50]
    target = 60
    events = list(linear_search_generator(list(arr), target))

    assert len(events) > 0
    final_event = events[-1]
    assert final_event.type == "done"
    assert final_event.data["found"] is False
    assert "found_index" not in final_event.data

    not_found_event = next((e for e in events if e.type == "not_found"), None)
    assert not_found_event is not None

def test_linear_search_empty_array():
    """Test linear search with an empty array."""
    arr = []
    target = 10
    events = list(linear_search_generator(list(arr), target))

    assert len(events) > 0
    final_event = events[-1]
    assert final_event.type == "done"
    assert final_event.data["found"] is False

def test_linear_search_first_element():
    """Test linear search when the target is the first element."""
    arr = [10, 20, 30]
    target = 10
    events = list(linear_search_generator(list(arr), target))

    final_event = events[-1]
    assert final_event.type == "done"
    assert final_event.data["found"] is True
    assert final_event.data["found_index"] == 0

def test_linear_search_last_element():
    """Test linear search when the target is the last element."""
    arr = [10, 20, 30]
    target = 30
    events = list(linear_search_generator(list(arr), target))

    final_event = events[-1]
    assert final_event.type == "done"
    assert final_event.data["found"] is True
    assert final_event.data["found_index"] == 2

def test_linear_search_duplicate_elements():
    """Test linear search with duplicate elements, should find the first occurrence."""
    arr = [10, 20, 30, 20, 40]
    target = 20
    events = list(linear_search_generator(list(arr), target))

    final_event = events[-1]
    assert final_event.type == "done"
    assert final_event.data["found"] is True
    assert final_event.data["found_index"] == 1