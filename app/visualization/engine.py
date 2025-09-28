from typing import List, Dict, Any, Optional
from app.utils.types import Event, Array, Graph
import json

class VisualizationEngine:
    """Manages the execution trace (list of events) for algorithm visualization.

    Provides methods to navigate through the trace, get snapshots of the state,
    and control playback.
    """

    def __init__(self, trace: List[Event]):
        """Initializes the engine with a list of events.

        Args:
            trace (List[Event]): A list of Event objects representing the algorithm's execution.
        """
        if not trace:
            raise ValueError("Trace cannot be empty.")
        self._trace = trace
        self._current_step_index = 0
        self._max_step_index = len(trace) - 1

    @property
    def step_count(self) -> int:
        """Returns the total number of steps in the trace."""
        return len(self._trace)

    @property
    def current_step(self) -> int:
        """Returns the current step number (from the event's `step` attribute)."""
        if not self._trace:
            return 0
        return self._trace[self._current_step_index].step

    @property
    def current_event(self) -> Event:
        """Returns the current Event object."""
        if not self._trace:
            raise IndexError("No events in trace.")
        return self._trace[self._current_step_index]

    def next(self) -> Optional[Event]:
        """Advances to the next step in the trace.

        Returns:
            Optional[Event]: The next event, or None if at the end of the trace.
        """
        if self._current_step_index < self._max_step_index:
            self._current_step_index += 1
            return self.current_event
        return None

    def prev(self) -> Optional[Event]:
        """Goes back to the previous step in the trace.

        Returns:
            Optional[Event]: The previous event, or None if at the beginning of the trace.
        """
        if self._current_step_index > 0:
            self._current_step_index -= 1
            return self.current_event
        return None

    def seek(self, step_index: int) -> Event:
        """Seeks to a specific step index in the trace.

        Args:
            step_index (int): The 0-based index of the event to seek to.

        Returns:
            Event: The event at the specified step index.

        Raises:
            IndexError: If the step_index is out of bounds.
        """
        if not (0 <= step_index <= self._max_step_index):
            raise IndexError(f"Step index {step_index} out of bounds [0, {self._max_step_index}]")
        self._current_step_index = step_index
        return self.current_event

    def get_snapshot(self) -> Dict[str, Any]:
        """Returns the renderable state (snapshot) for the current step.

        With the new rich-event architecture, this method simply extracts the data
        from the current event and adds context for the renderer.
        """
        event = self.current_event

        # The event's data field now contains the complete visual state.
        snapshot_data = event.data.copy()

        # Provide context for the renderer (e.g., for the title).
        snapshot_data["current_event_type"] = event.type
        snapshot_data["current_event_details"] = event.details

        return snapshot_data

    def get_trace_json(self) -> str:
        """Returns the full trace as a JSON string."""
        return json.dumps([event.to_json_serializable() for event in self._trace], indent=2)

    @classmethod
    def from_json_trace(cls, json_trace: str) -> "VisualizationEngine":
        """Creates an engine instance from a JSON trace string.

        Args:
            json_trace (str): A JSON string representing a list of events.

        Returns:
            VisualizationEngine: An initialized engine instance.
        """
        data = json.loads(json_trace)
        # Reconstruct the 'data' field correctly from the JSON
        events = [
            Event(
                step=d["step"],
                type=d["type"],
                details=d["details"],
                data={k: v for k, v in d.items() if k not in ["step", "type", "details"]}
            ) for d in data
        ]
        return cls(events)


if __name__ == '__main__':
    # Example usage with a dummy trace containing rich visual data
    dummy_trace = [
        Event(
            step=0, type="start", details="Initial state",
            data={
                "graph_snapshot": {"A": [("B", 1)], "B": [("A", 1)]},
                "node_colors": {"A": "#ff9933", "B": "#66b3ff"},
                "edge_colors": {("A", "B"): "#b3b3b3"},
                "edge_widths": {("A", "B"): 1.5},
                "node_labels": {"A": "A\n(0)", "B": "B\n(inf)"}
            }
        ),
        Event(
            step=1, type="visit", details="Visiting B",
            data={
                "graph_snapshot": {"A": [("B", 1)], "B": [("A", 1)]},
                "node_colors": {"A": "#cccccc", "B": "#ff9933"},
                "edge_colors": {("A", "B"): "#333333"},
                "edge_widths": {("A", "B"): 3.0},
                "node_labels": {"A": "A\n(0)", "B": "B\n(1)"}
            }
        ),
        Event(step=2, type="done", details="Finished", data={})
    ]

    engine = VisualizationEngine(dummy_trace)

    print(f"Total steps: {engine.step_count}")

    # --- Test Initial State ---
    print("\n--- Initial State ---")
    print(f"Current step: {engine.current_step}")
    snapshot_initial = engine.get_snapshot()
    print(f"Snapshot details: {snapshot_initial.get('current_event_details')}")
    assert snapshot_initial['node_colors']['A'] == "#ff9933"
    assert "graph_snapshot" in snapshot_initial
    print("Initial snapshot test passed.")

    # --- Test Next State ---
    engine.next()
    print("\n--- Next State ---")
    print(f"Current step: {engine.current_step}")
    snapshot_next = engine.get_snapshot()
    print(f"Snapshot details: {snapshot_next.get('current_event_details')}")
    assert snapshot_next['node_colors']['B'] == "#ff9933"
    assert snapshot_next['edge_widths'][('A', 'B')] == 3.0
    print("Next snapshot test passed.")

    # --- Test Seek ---
    engine.seek(0)
    print("\n--- Seek to 0 ---")
    print(f"Current step: {engine.current_step}")
    snapshot_seek = engine.get_snapshot()
    assert snapshot_seek['node_colors']['A'] == "#ff9933"
    print("Seek test passed.")

    # --- Test JSON Serialization/Deserialization ---
    json_output = engine.get_trace_json()
    print(f"\n--- JSON Trace ---\n{json_output}")
    new_engine = VisualizationEngine.from_json_trace(json_output)
    new_engine.seek(1)
    snapshot_from_json = new_engine.get_snapshot()

    print("\n--- State from Deserialized JSON ---")
    print(f"Snapshot details: {snapshot_from_json.get('current_event_details')}")
    assert snapshot_from_json['node_colors']['B'] == "#ff9933"
    assert snapshot_from_json['edge_widths'][('A', 'B')] == 3.0
    print("JSON (de)serialization test passed.")

