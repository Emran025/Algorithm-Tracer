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
        """Returns a minimal renderable state (snapshot) for the current step.

        Finds the most recent full snapshot (array_snapshot or graph_snapshot) at or
        before the current step, then re-applies only the modifications that occur
        after that snapshot up to the current step.
        """
        snapshot_data: Dict[str, Any] = {}
        current_array: Optional[Array] = None
        current_graph: Optional[Graph] = None

        # Find the most recent full snapshot (and remember its index)
        snapshot_index: Optional[int] = None
        for i in range(self._current_step_index + 1):
            event = self._trace[i]
            if "array_snapshot" in event.data:
                current_array = list(event.data["array_snapshot"])
                current_graph = None
                snapshot_index = i
            elif "graph_snapshot" in event.data:
                # deep copy via json to avoid accidental references
                current_graph = json.loads(json.dumps(event.data["graph_snapshot"]))
                current_array = None
                snapshot_index = i

        # If we found a snapshot, replay only events after it. Otherwise start at 0.
        start_index = 0 if snapshot_index is None else (snapshot_index + 1)

        # Apply modifications from start_index up to the current step index
        for i in range(start_index, self._current_step_index + 1):
            event = self._trace[i]

            if current_array is not None:
                # Overwrite (used by merge/copy-back style algorithms)
                if event.type == "overwrite" and "index" in event.data and "value" in event.data:
                    idx = event.data["index"]
                    val = event.data["value"]
                    if 0 <= idx < len(current_array):
                        current_array[idx] = val

                # Swap (used by many in-place sorts)
                elif event.type == "swap" and "i" in event.data and "j" in event.data:
                    idx_i = event.data["i"]
                    idx_j = event.data["j"]
                    if 0 <= idx_i < len(current_array) and 0 <= idx_j < len(current_array):
                        current_array[idx_i], current_array[idx_j] = current_array[idx_j], current_array[idx_i]

                # (Optional) handle other array-modifying event types if your algorithms add them

            if current_graph is not None:
                if event.type == "set_distance" and "u" in event.data and "new_distance" in event.data:
                    node = event.data["u"]
                    if "distances" not in snapshot_data:
                        snapshot_data["distances"] = {}
                    snapshot_data["distances"][node] = event.data["new_distance"]
                elif event.type == "add_mst_edge" and "u" in event.data and "v" in event.data:
                    if "mst_edges" not in snapshot_data:
                        snapshot_data["mst_edges"] = []
                    snapshot_data["mst_edges"].append((event.data["u"], event.data["v"]))
                # (Optional) add other graph updates here

        if current_array is not None:
            snapshot_data["array"] = current_array
        if current_graph is not None:
            snapshot_data["graph"] = current_graph

        # Provide context for renderers
        snapshot_data["current_event_type"] = self.current_event.type
        snapshot_data["current_event_details"] = self.current_event.details
        snapshot_data["current_event_data"] = self.current_event.data

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
        events = [Event(step=d["step"], type=d["type"], details=d["details"], data={k: v for k, v in d.items() if k not in ["step", "type", "details"]}) for d in data]
        return cls(events)


if __name__ == '__main__':
    # Example usage with a dummy trace
    dummy_trace = [
        Event(step=0, type="snapshot", details="Initial array", data={"array_snapshot": [5, 2, 8, 1]}),
        Event(step=1, type="compare", details="Compare 5 and 2", data={"i": 0, "j": 1}),
        Event(step=2, type="swap", details="Swap 5 and 2", data={"i": 0, "j": 1}),
        Event(step=3, type="snapshot", details="Array after swap", data={"array_snapshot": [2, 5, 8, 1]}),
        Event(step=4, type="compare", details="Compare 8 and 1", data={"i": 2, "j": 3}),
        Event(step=5, type="swap", details="Swap 8 and 1", data={"i": 2, "j": 3}),
        Event(step=6, type="done", details="Algorithm finished", data={"sorted_array": [1, 2, 5, 8]}),
    ]

    engine = VisualizationEngine(dummy_trace)

    print(f"Total steps: {engine.step_count}")
    print(f"Current step (initial): {engine.current_step}")
    print(f"Current event (initial): {engine.current_event.to_json_serializable()}")
    print(f"Snapshot (initial): {engine.get_snapshot()}")

    engine.next()
    print(f"\nCurrent step (next): {engine.current_step}")
    print(f"Current event (next): {engine.current_event.to_json_serializable()}")
    print(f"Snapshot (next): {engine.get_snapshot()}")

    engine.seek(5)
    print(f"\nCurrent step (seek to 5): {engine.current_step}")
    print(f"Current event (seek to 5): {engine.current_event.to_json_serializable()}")
    print(f"Snapshot (seek to 5): {engine.get_snapshot()}")

    engine.prev()
    print(f"\nCurrent step (prev): {engine.current_step}")
    print(f"Current event (prev): {engine.current_event.to_json_serializable()}")
    print(f"Snapshot (prev): {engine.get_snapshot()}")

    # Test JSON serialization/deserialization
    json_output = engine.get_trace_json()
    print(f"\nJSON Trace:\n{json_output}")

    new_engine = VisualizationEngine.from_json_trace(json_output)
    print(f"\nNew engine current step: {new_engine.current_step}")
    print(f"New engine current event: {new_engine.current_event.to_json_serializable()}")
    assert new_engine.step_count == engine.step_count
    print("JSON (de)serialization test passed.")

    # Test graph snapshot logic
    graph_trace = [
        Event(step=0, type="snapshot", details="Initial graph", data={"graph_snapshot": {"A": [("B", 1)], "B": [("A", 1)]}}),
        Event(step=1, type="set_distance", details="Set distance A to 0", data={"u": "A", "new_distance": 0}),
        Event(step=2, type="add_mst_edge", details="Add edge A-B", data={"u": "A", "v": "B", "weight": 1}),
        Event(step=3, type="done", details="Graph algo finished", data={}),
    ]
    graph_engine = VisualizationEngine(graph_trace)
    graph_engine.seek(2)
    graph_snapshot = graph_engine.get_snapshot()
    print(f"\nGraph snapshot at step 2: {graph_snapshot}")
    assert "graph" in graph_snapshot
    assert "distances" in graph_snapshot
    assert graph_snapshot["distances"]["A"] == 0
    assert "mst_edges" in graph_snapshot
    assert ("A", "B") in graph_snapshot["mst_edges"]
    print("Graph snapshot test passed.")

