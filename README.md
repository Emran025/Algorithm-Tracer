# AlgoVisEdu: Interactive Algorithm Visualization

AlgoVisEdu is an educational tool built with Python and Streamlit to help users visualize and understand how common algorithms work. It provides step-by-step, interactive animations for a variety of searching, sorting, and graph algorithms.

<!-- Add a screenshot of the application here -->

<div style="display: flex; justify-content: space-between; margin-bottom: 25px">
<img src="screenshots/screenshot_00.png" alt = "screenshot_00" style="width:18%">
<img src="screenshots/screenshot_01.png" alt = "screenshot_01" style="width:18%">
<img src="screenshots/screenshot_02.png" alt = "screenshot_02" style="width:18%">
<img src="screenshots/screenshot_03.png" alt = "screenshot_03" style="width : 18%">
<img src="screenshots/screenshot_04.png" alt = "screenshot_04" style="width : 18%">
</div>

> Screenshot of an interactive algorithm visualization web app called AlgoVisEdu. The main interface displays a configuration panel on the left for selecting algorithms such as Merge Sort, Quick Sort, Linear Search, Kruskal MST, and Dijkstra SSSP, with options to input data manually or generate random data. The center area is reserved for dynamic visualizations, including bar charts for sorting and searching algorithms and a network graph for Dijkstra's algorithm, where nodes and edges are highlighted in green to show the shortest path. The right panel provides detailed algorithm analysis, including time and space complexity, explanatory notes, and event details. The environment is clean and modern, with a calm and educational tone. All visible text is transcribed, including section headers like Visualization, Event Details, Algorithm Analysis, and configuration options such as Select Algorithm, Run Algorithm, and Trace

## Features

- **Interactive Visualizations**: Watch algorithms operate on data in real-time.
- **Full Playback Control**: Play, pause, step forward, step backward, and seek to any point in the execution.
- **Adjustable Speed**: Slow down the animation to catch every detail or speed it up to see the bigger picture.
- **Detailed Explanations**: See a human-readable description of every single action the algorithm takes.
- **Complexity Analysis**: View the time and space complexity for each algorithm, along with pedagogical notes.
- **Save & Load Traces**: Save the entire step-by-step execution of an algorithm to a JSON file and load it back later for review or sharing.
- **Flexible Data Input**: Manually enter your own data or generate random arrays and graphs to experiment with.

## 📚 Implemented Algorithms

The following algorithms are currently available for visualization:

- **Searching**:
  - Linear Search
- **Sorting**:
  - Merge Sort
  - Quick Sort
- **Graph**:
  - Kruskal's Algorithm (Minimum Spanning Tree)
  - Dijkstra's Algorithm (Single-Source Shortest Path)

## Getting Started

Follow these instructions to get a local copy of the project up and running.

### Prerequisites

- Python 3.8+
- `pip` and `venv`

### Installation & Setup

1.  **Clone the repository:**

    ```sh
    git clone https://github.com/your-username/AlgoVisEdu.git
    cd AlgoVisEdu
    ```

2.  **Create and activate a virtual environment:**

    ```sh
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    conda -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```sh
    conda install streamlit
    ```

### Running the Application

Once the setup is complete, you can launch the Streamlit application with a single command:

```sh
C:/Users/Thinkpad/anaconda3/Scripts/activate
conda activate base
set PYTHONPATH=%PYTHONPATH%;C:\Applications_Projacts\pyProjacts\project_03
streamlit run app/ui/streamlit_app.py
```

This will open the application in your default web browser.

## Project Structure

The project is organized into several modules to separate concerns:

```
│   .gitignore
│   .sh1
│   COMMIT_LOG.md
│   project-contents.txt
│   pyproject.toml
│   README.md
│   requirements.txt
│
├───.github
│   └───workflows
│           main.yml
│
├───.pytest_cache
│   │   .gitignore
│   │   CACHEDIR.TAG
│   │   README.md
│   │
│   └───v
│       └───cache
│               lastfailed
│               nodeids
│
├───app
│   │   __init__.py
│   │
│   ├───algorithms
│   │   │   dijkstra.py
│   │   │   kruskal.py
│   │   │   linear_search.py
│   │   │   merge_sort.py
│   │   │   quick_sort.py
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__
│   │           dijkstra.cpython-312.pyc
│   │           kruskal.cpython-312.pyc
│   │           linear_search.cpython-312.pyc
│   │           merge_sort.cpython-312.pyc
│   │           quick_sort.cpython-312.pyc
│   │           __init__.cpython-312.pyc
│   │
│   ├───ui
│   │   │   components.py
│   │   │   streamlit_app.py
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__
│   │           components.cpython-312.pyc
│   │           __init__.cpython-312.pyc
│   │
│   ├───utils
│   │   │   io.py
│   │   │   sample_generators.py
│   │   │   types.py
│   │   │   union_find.py
│   │   │   validators.py
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__
│   │           types.cpython-312.pyc
│   │           union_find.cpython-312.pyc
│   │           __init__.cpython-312.pyc
│   │
│   ├───visualization
│   │   │   engine.py
│   │   │   renderers.py
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__
│   │           engine.cpython-312.pyc
│   │           renderers.cpython-312.pyc
│   │           __init__.cpython-312.pyc
│   │
│   └───__pycache__
│           __init__.cpython-312.pyc
│
├───docs
│       API.md
│
├───examples
│       trace_dijkstra_example.json
│       trace_merge_sort_example.json
│
├───sample_data
│       sample_array.txt
│       sample_graph.json
│
└───tests
        conftest.py
        test_dijkstra.py
        test_kruskal.py
        test_linear_search.py
        test_merge_sort.py
        test_quick_sort.py
        test_streamlit_app.py
```

## How to Contribute

Adding a new algorithm is designed to be straightforward.

1.  **Create the Algorithm File**:

    - Add a new Python file in `app/algorithms/` (e.g., `my_new_sort.py`).
    - Inside this file, create a **generator function** that takes the required data as input (e.g., an array or graph).

2.  **Implement the Generator**:

    - Your function must `yield` an `Event` object (from `app.utils.types`) for every logical step of the algorithm.
    - The `data` attribute of each `Event` must contain a complete snapshot of the visual state (e.g., the array and a list of colors for the bars). See existing algorithms for examples.

3.  **Register the Algorithm**:

    - Open `app/ui/streamlit_app.py`.
    - Import your new generator function.
    - Add it to the `ALGORITHMS` dictionary, specifying its name, generator function, and type (`"array"` or `"graph"`).

    ```python
    # In app/ui/streamlit_app.py
    from app.algorithms.my_new_sort import my_new_sort_generator

    ALGORITHMS = {
        # ... other algorithms
        "My New Sort": {"generator": my_new_sort_generator, "type": "array"},
    }
    ```

4.  **Create a Renderer (Optional)**:
    - If your algorithm requires a new type of visualization, you can add a new rendering function to `app/visualization/renderers.py` and call it from `app/ui/streamlit_app.py`.

## Tech Stack

- **Python**: Core programming language.
- **Streamlit**: For creating the interactive web application UI.
- **Matplotlib**: For generating the plot-based visualizations.
- **NetworkX**: For graph data structures and layout algorithms.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
