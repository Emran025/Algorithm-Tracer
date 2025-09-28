## Commit Log

This log summarizes the high-level commits and actions taken to build the AlgoVisEdu project.

-   **Initial Project Setup**: Created the basic directory structure, `requirements.txt`, and `pyproject.toml`.
-   **Core Types and Utilities**: Implemented `app/utils/types.py` for the `Event` dataclass and `app/utils/union_find.py` for Kruskal's algorithm helper.
-   **Merge Sort Implementation**: Developed the `merge_sort_generator` in `app/algorithms/merge_sort.py` and its corresponding unit tests in `tests/test_merge_sort.py`.
-   **Visualization Engine**: Implemented the `VisualizationEngine` in `app/visualization/engine.py` to manage event traces and state snapshots.
-   **Renderers**: Created `app/visualization/renderers.py` with functions to visualize arrays (bar charts) and graphs (network diagrams) using Matplotlib.
-   **Streamlit UI Components**: Developed `app/ui/components.py` for reusable UI elements like playback controls and data input forms.
-   **Main Streamlit Application**: Implemented `app/ui/streamlit_app.py` to integrate all components, engine, and renderers into an interactive web application.
-   **Algorithm Stubs**: Created placeholder files for `linear_search.py`, `quick_sort.py`, `kruskal.py`, and `dijkstra.py` to ensure the Streamlit app could run without import errors during initial UI development.
-   **Linear Search Implementation**: Implemented the `linear_search_generator` in `app/algorithms/linear_search.py` and its unit tests in `tests/test_linear_search.py`.
-   **Quick Sort Implementation**: Implemented the `quick_sort_generator` in `app/algorithms/quick_sort.py` and its unit tests in `tests/test_quick_sort.py`.
-   **Kruskal's Algorithm Implementation**: Implemented the `kruskal_generator` in `app/algorithms/kruskal.py` and its unit tests in `tests/test_kruskal.py`.
-   **Dijkstra's Algorithm Implementation**: Implemented the `dijkstra_generator` in `app/algorithms/dijkstra.py` and its unit tests in `tests/test_dijkstra.py`.
-   **Input Validators and IO Utilities**: Created `app/utils/validators.py` for input validation and `app/utils/io.py` for trace loading/saving.
-   **Sample Data Generators**: Developed `app/utils/sample_generators.py` for generating random arrays and graphs.
-   **Documentation**: Wrote `README.md` for project overview and setup, and `docs/API.md` for detailed API documentation and event schema.
-   **Sample Data and Traces**: Added `sample_data/sample_array.txt`, `sample_data/sample_graph.json`, and example trace JSON files in `examples/`.
-   **CI/CD Configuration**: Set up a basic GitHub Actions workflow in `.github/workflows/main.yml` for automated testing and linting.
-   **Integration Tests**: Added `tests/test_streamlit_app.py` for a smoke test of the Streamlit application.

