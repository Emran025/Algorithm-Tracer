# AlgoVisEdu API Documentation

This document provides a detailed reference for the core APIs and data structures used in the AlgoVisEdu project, primarily focusing on the Event Schema and the Visualization Engine API.

## 1. Event Schema

The entire visualization system is driven by a sequence of `Event` objects. Each algorithm is implemented as a generator that yields these events at every meaningful operation. The `Event` dataclass is defined in `app/utils/types.py`.

### Event Dataclass

```python
from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class Event:
    step: int
    type: str
    details: str
    data: Dict[str, Any] = field(default_factory=dict)
```

### Fields

-   **`step`** (int): A unique, monotonically increasing integer for each event. This is crucial for ordering and seeking.
-   **`type`** (str): A string identifier for the type of operation. This determines how the renderer might highlight elements.
-   **`details`** (str): A human-readable description of the event, displayed in the UI to explain the current step.
-   **`data`** (Dict[str, Any]): A dictionary containing any data relevant to the event. This is where you put indices, values, nodes, weights, and snapshots.

### Common Event Types and `data` Payloads

Below are common event types used across the implemented algorithms. When adding a new algorithm, you can reuse these or define new ones as needed.

| Event Type        | Description                                       | `data` Payload Example                                                                 |
| ----------------- | ------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `snapshot`        | Provides a full snapshot of the data structure.   | `{"array_snapshot": [5, 2, 8], "graph_snapshot": {"A": [("B", 1)]}}`               |
| `compare`         | When two elements are compared.                   | `{"i": 0, "j": 1, "value_i": 5, "value_j": 2}`                                    |
| `swap`            | When two elements in an array are swapped.        | `{"i": 0, "j": 1}`                                                                  |
| `overwrite`       | When an element in an array is overwritten.       | `{"index": 2, "value": 10, "old_value": 8}`                                        |
| `set_pivot`       | When a pivot is chosen in algorithms like Quick Sort. | `{"index": 4, "value": 7}`                                                          |
| `visit`           | When a node in a graph is visited.                | `{"u": "A", "distance": 0}`                                                        |
| `consider_edge`   | When a graph edge is being considered.            | `{"u": "A", "v": "B", "weight": 5}`                                             |
| `add_mst_edge`    | When an edge is added to the Minimum Spanning Tree. | `{"u": "A", "v": "B", "weight": 5}`                                             |
| `relax`           | When a distance is updated in a shortest path algo. | `{"u": "A", "v": "B", "new_distance": 3, "old_distance": 5}`                   |
| `set_distance`    | When a distance is initially set.                 | `{"u": "A", "new_distance": 0}`                                                    |
| `found`           | When a target element is found in a search.       | `{"index": 3, "value": 42}`                                                         |
| `done`            | The final event, signaling completion.            | `{"sorted_array": [1, 2, 3], "final_distances": {"A": 0, "B": 3}}`                |

### Example Event Traces (JSON)

Here are two short example traces in JSON format, as they would be saved or loaded by the application.

#### Merge Sort Example Trace

```json
[
  {
    "step": 0,
    "type": "snapshot",
    "details": "Initial array state",
    "array_snapshot": [
      3,
      1,
      4
    ]
  },
  {
    "step": 1,
    "type": "divide",
    "details": "Dividing array from index 0 to 2 into two halves",
    "left": 0,
    "right": 2,
    "mid": 1,
    "array_snapshot": [
      3,
      1,
      4
    ]
  },
  {
    "step": 2,
    "type": "divide",
    "details": "Dividing array from index 0 to 1 into two halves",
    "left": 0,
    "right": 1,
    "mid": 0,
    "array_snapshot": [
      3,
      1,
      4
    ]
  },
  {
    "step": 3,
    "type": "merge_start",
    "details": "Starting merge for sub-array from 0 to 1",
    "left": 0,
    "mid": 0,
    "right": 1,
    "array_snapshot": [
      3,
      1,
      4
    ]
  },
  {
    "step": 4,
    "type": "compare",
    "details": "Comparing elements at index 0 (3) and 1 (1)",
    "i": 0,
    "j": 1,
    "value_i": 3,
    "value_j": 1,
    "array_snapshot": [
      3,
      1,
      4
    ]
  },
  {
    "step": 5,
    "type": "overwrite",
    "details": "Overwriting temp_arr[0] with current_arr[1] (1)",
    "index": 0,
    "value": 1,
    "source_index": 1,
    "array_snapshot": [
      3,
      1,
      4
    ]
  },
  {
    "step": 6,
    "type": "copy_back",
    "details": "Copying temp_arr[0] (1) back to current_arr[0]",
    "index": 0,
    "value": 1,
    "array_snapshot": [
      1,
      1,
      4
    ]
  },
  {
    "step": 7,
    "type": "done",
    "details": "Merge Sort completed",
    "sorted_array": [
      1,
      3,
      4
    ]
  }
]
```

#### Dijkstra Example Trace

```json
[
  {
    "step": 0,
    "type": "snapshot",
    "details": "Initial graph state, starting from A",
    "graph_snapshot": {
      "A": [
        [
          "B",
          1
        ],
        [
          "C",
          4
        ]
      ],
      "B": [
        [
          "A",
          1
        ],
        [
          "C",
          2
        ]
      ],
      "C": [
        [
          "A",
          4
        ],
        [
          "B",
          2
        ]
      ]
    },
    "distances": {
      "A": 0,
      "B": "inf",
      "C": "inf"
    },
    "start_node": "A"
  },
  {
    "step": 1,
    "type": "visit",
    "details": "Visiting node A with distance 0",
    "u": "A",
    "distance": 0,
    "distances": {
      "A": 0,
      "B": "inf",
      "C": "inf"
    },
    "graph_snapshot": {
      "A": [
        [
          "B",
          1
        ],
        [
          "C",
          4
        ]
      ],
      "B": [
        [
          "A",
          1
        ],
        [
          "C",
          2
        ]
      ],
      "C": [
        [
          "A",
          4
        ],
        [
          "B",
          2
        ]
      ]
    }
  },
  {
    "step": 2,
    "type": "consider_edge",
    "details": "Considering edge A-B with weight 1",
    "u": "A",
    "v": "B",
    "weight": 1,
    "distances": {
      "A": 0,
      "B": "inf",
      "C": "inf"
    },
    "graph_snapshot": {
      "A": [
        [
          "B",
          1
        ],
        [
          "C",
          4
        ]
      ],
      "B": [
        [
          "A",
          1
        ],
        [
          "C",
          2
        ]
      ],
      "C": [
        [
          "A",
          4
        ],
        [
          "B",
          2
        ]
      ]
    }
  },
  {
    "step": 3,
    "type": "relax",
    "details": "Relaxing edge A-B. New distance to B is 1",
    "u": "A",
    "v": "B",
    "weight": 1,
    "old_distance": "inf",
    "new_distance": 1,
    "distances": {
      "A": 0,
      "B": 1,
      "C": "inf"
    },
    "graph_snapshot": {
      "A": [
        [
          "B",
          1
        ],
        [
          "C",
          4
        ]
      ],
      "B": [
        [
          "A",
          1
        ],
        [
          "C",
          2
        ]
      ],
      "C": [
        [
          "A",
          4
        ],
        [
          "B",
          2
        ]
      ]
    }
  },
  {
    "step": 4,
    "type": "done",
    "details": "Dijkstra\u0027s algorithm completed",
    "final_distances": {
      "A": 0,
      "B": 1,
      "C": 3
    },
    "final_paths": {
      "A": null,
      "B": "A",
      "C": "B"
    },
    "graph_snapshot": {
      "A": [
        [
          "B",
          1
        ],
        [
          "C",
          4
        ]
      ],
      "B": [
        [
          "A",
          1
        ],
        [
          "C",
          2
        ]
      ],
      "C": [
        [
          "A",
          4
        ],
        [
          "B",
          2
        ]
      ]
    }
  }
]
```

## 2. Visualization Engine API

The `VisualizationEngine` class (in `app/visualization/engine.py`) is responsible for managing the trace and providing an interface for the UI to control playback and get renderable snapshots.

### Class `VisualizationEngine`

-   **`__init__(self, trace: List[Event])`**: Initializes the engine with a full trace (list of `Event` objects).

-   **`step_count`** (property): Returns the total number of events in the trace.

-   **`current_step`** (property): Returns the `step` number of the current event.

-   **`current_event`** (property): Returns the full `Event` object at the current position.

-   **`next(self) -> Optional[Event]`**: Advances the internal pointer to the next event and returns it. Returns `None` if at the end.

-   **`prev(self) -> Optional[Event]`**: Moves the internal pointer to the previous event and returns it. Returns `None` if at the beginning.

-   **`seek(self, step_index: int) -> Event`**: Jumps to a specific event by its 0-based index in the trace list.

-   **`get_snapshot(self) -> Dict[str, Any]`**: This is a key method for rendering. It computes the state of the data structure (e.g., array or graph) at the current step. It does this by finding the most recent `snapshot` event and then re-applying all subsequent modifications up to the current event. This allows for efficient state reconstruction without storing a full copy of the data structure at every step.

-   **`get_trace_json(self) -> str`**: Serializes the entire trace into a JSON string.

-   **`from_json_trace(cls, json_trace: str) -> "VisualizationEngine"`**: A class method to create a new `VisualizationEngine` instance from a JSON trace string.

