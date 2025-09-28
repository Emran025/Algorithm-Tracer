import json
from typing import List, Dict, Any
from app.utils.types import Event

def load_trace_from_file(filepath: str) -> List[Event]:
    """Loads a list of Event objects from a JSON file.

    Args:
        filepath (str): The path to the JSON file.

    Returns:
        List[Event]: A list of Event objects.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file content is not valid JSON.
        ValueError: If the JSON structure does not conform to expected event format.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        events_data = json.load(f)

    if not isinstance(events_data, list):
        raise ValueError("JSON content must be a list of event objects.")

    events = []
    for d in events_data:
        if not all(k in d for k in ["step", "type", "details"]):
            raise ValueError(f"Event object missing required keys: {d}")
        events.append(Event(step=d["step"], type=d["type"], details=d["details"], data={k: v for k, v in d.items() if k not in ["step", "type", "details"]}))
    return events

def save_trace_to_file(filepath: str, trace: List[Event]):
    """Saves a list of Event objects to a JSON file.

    Args:
        filepath (str): The path to the JSON file.
        trace (List[Event]): A list of Event objects to save.
    """
    serializable_trace = [event.to_json_serializable() for event in trace]
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(serializable_trace, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    # Dummy events for testing
    dummy_events = [
        Event(step=0, type="start", details="Algorithm started", data={"initial_value": 10}),
        Event(step=1, type="process", details="Processing step 1", data={"current_value": 5}),
        Event(step=2, type="done", details="Algorithm finished", data={"final_result": 0})
    ]

    test_file = "test_trace.json"

    print(f"Saving dummy events to {test_file}...")
    save_trace_to_file(test_file, dummy_events)
    print("Save complete.")

    print(f"Loading events from {test_file}...")
    loaded_events = load_trace_from_file(test_file)
    print("Load complete.")

    assert len(loaded_events) == len(dummy_events)
    for i in range(len(loaded_events)):
        assert loaded_events[i].step == dummy_events[i].step
        assert loaded_events[i].type == dummy_events[i].type
        assert loaded_events[i].details == dummy_events[i].details
        assert loaded_events[i].data == dummy_events[i].data
    print("Load/Save test passed: Loaded events match original events.")

    import os
    os.remove(test_file)
    print(f"Cleaned up {test_file}.")

    # Test error handling for invalid JSON
    invalid_json_file = "invalid.json"
    with open(invalid_json_file, "w") as f:
        f.write("{\"not_a_list\": 1}")
    try:
        load_trace_from_file(invalid_json_file)
    except ValueError as e:
        print(f"Expected error for invalid JSON structure: {e}")
        assert "JSON content must be a list of event objects." in str(e)
    os.remove(invalid_json_file)

    # Test error handling for missing keys
    missing_key_json_file = "missing_key.json"
    with open(missing_key_json_file, "w") as f:
        f.write("[{\"step\": 0, \"type\": \"start\"}]") # Missing 'details'
    try:
        load_trace_from_file(missing_key_json_file)
    except ValueError as e:
        print(f"Expected error for missing keys: {e}")
        assert "Event object missing required keys" in str(e)
    os.remove(missing_key_json_file)

