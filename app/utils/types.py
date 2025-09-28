from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

@dataclass
class Event:
    """Represents a single step or event in an algorithm's execution for visualization.

    Attributes:
        step (int): Monotonic step number, starting from 0 or 1.
        type (str): Category of the event (e.g., "compare", "swap", "visit", "done").
        details (str): A short, human-readable explanation of the event.
        data (Dict[str, Any]): Optional dictionary for event-specific data.
                              This can include 'i', 'j', 'index', 'value', 'u', 'v', 'weight',
                              'old_value', 'new_value', 'distances', 'array_snapshot', 'graph_snapshot' etc.
    """
    step: int
    type: str
    details: str
    data: Dict[str, Any] = field(default_factory=dict)

    def to_json_serializable(self) -> Dict[str, Any]:
        """Converts the Event dataclass instance to a JSON-serializable dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the event.
        """
        return {
            "step": self.step,
            "type": self.type,
            "details": self.details,
            **self.data,
        }

    @classmethod
    def from_json_list(cls, json_string: str) -> List['Event']:
        """Deserializes a JSON string into a list of Event objects."""
        import json
        events_data = json.loads(json_string)
        return [
            cls(
                step=d.get("step", -1),
                type=d.get("type", "unknown"),
                details=d.get("details", ""),
                data={k: v for k, v in d.items() if k not in ["step", "type", "details"]}
            ) for d in events_data
        ]

# Define common types for clarity
Array = List[Union[int, float]]
Graph = Dict[Any, List[Any]] # Adjacency list representation

