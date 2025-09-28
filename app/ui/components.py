
import streamlit as st
from typing import Callable, List, Any, Dict
import re

def playback_controls(on_play: Callable, on_pause: Callable, on_step_forward: Callable, on_step_back: Callable, on_seek: Callable, current_step_index: int, total_steps: int, is_playing: bool, speed: float):
    """Renders playback controls for the visualization.

    Args:
        on_play (Callable): Callback function for play button.
        on_pause (Callable): Callback function for pause button.
        on_step_forward (Callable): Callback function for step forward button.
        on_step_back (Callable): Callback function for step back button.
        on_seek (Callable): Callback function for seeking to a specific step.
        current_step_index (int): The current 0-based index of the event.
        total_steps (int): Total number of events in the trace.
        is_playing (bool): Current playback state.
        speed (float): Current playback speed.
    """
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])
 
    with col1:
        if st.button(" ⏮ Back "): on_step_back()
    with col2:
        if is_playing:
            if st.button(" ⏸ Pause "): on_pause()
        else:
            if st.button(" ◀ Play "): on_play()
    with col3:
        if st.button(" Forward ⏭ "): on_step_forward()
    with col4:
        st.selectbox(
            "Speed",
            options=[0.5, 1.0, 2.0, 4.0],
            index=1, # Default to 1.0x
            format_func=lambda x: f"{x}x",
            key="playback_speed_selector",
            on_change=lambda: st.session_state.update(playback_speed=st.session_state.playback_speed_selector)
        )
        st.session_state.playback_speed = st.session_state.playback_speed_selector

    with col5:
        # Slider for seeking through steps
        new_step_index = st.slider(
            "Step",
            min_value=0,
            max_value=total_steps - 1 if total_steps > 0 else 0,
            value=current_step_index,
            step=1,
            key="step_slider",
            on_change=lambda: on_seek(st.session_state.step_slider)
        )

def data_input_form(algorithm_type: str , algorithm_name : str) -> Dict[str, Any]:
    """Renders input forms for algorithm data based on type.

    Args:
        algorithm_type (str): Type of algorithm (e.g., "array", "graph").

    Returns:
        Dict[str, Any]: Dictionary containing user input data.
    """
    data = {}
    st.subheader("Input Data")

    if algorithm_type == "array":
        input_method = st.radio("Choose input method:", ("Manual Input", "Generate Random"), key="array_input_method")

        if input_method == "Manual Input":
            array_str = st.text_input("Enter array elements (comma-separated integers):", "3,1,4,1,5,9,2,6", key="manual_array_input")
            try:
                data["array"] = [int(x.strip()) for x in array_str.split(",") if x.strip()]
            except ValueError:
                st.error("Invalid array input. Please enter comma-separated integers.")
                data["array"] = []
            if algorithm_name != "Quick Sort" and algorithm_name != "Merge Sort":
                target_value = st.text_input("Enter Target Value for Linear Search:", key="linear_search_target")
                if target_value :
                    try:
                        data["target"] = int(target_value)
                    except ValueError:
                        st.error("Invalid target value. Please enter an integer.")
                else:
                    data["target"] = None
            else:
                data["target"] = None
        else: # Generate Random
            col1, col2 = st.columns(2)
            with col1:
                size = st.number_input("Array Size:", min_value=1, max_value=100, value=10, step=1, key="random_array_size")
            with col2:
                min_val = st.number_input("Min Value:", value=0, key="random_array_min_val")
                max_val = st.number_input("Max Value:", value=100, key="random_array_max_val")
            if st.button("Generate Random Array"): # This button will trigger a re-run and new random array
                import random
                st.session_state.generated_array = [random.randint(min_val, max_val) for _ in range(size)]
            if "generated_array" in st.session_state:
                data["array"] = st.session_state.generated_array
                st.write(f"Generated Array: {data['array']}")
            else:
                # Initial generation if not already present
                import random
                st.session_state.generated_array = [random.randint(min_val, max_val) for _ in range(size)]
                data["array"] = st.session_state.generated_array
                st.write(f"Generated Array: {data['array']}")

    elif algorithm_type == "graph":
        st.warning("Graph input methods are not fully implemented yet. Please use sample data or manual input for now.")
        graph_input_method = st.radio("Choose input method:", ("Manual Adjacency List", "Upload Edge List (CSV/JSON)", "Generate Random"), key="graph_input_method")

        if graph_input_method == "Manual Adjacency List":
            
            start_node_input = st.text_input("Enter Start Node (e.g., A):", key="dijkstra_start_node_manual")
            if start_node_input:
                data["start_node"] = start_node_input.strip()
            else:
                st.error("Start node cannot be empty for Dijkstra's algorithm.")
                data["start_node"] = None

            
            st.info("Enter graph as an adjacency list. Format: `Node: (Neighbor, Weight), (Neighbor, Weight)` per line.")
            graph_str = st.text_area(
                "Example: A: (B,1), (C,4)\nB: (A,1), (C,2)",
                height=150,
                key="manual_graph_input"
            )

            parsed_graph = {}
            if graph_str.strip():
                for line in graph_str.split("\n"):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        node, edges_str = line.split(":", 1)
                        node = node.strip()
                        edges = []
                        matches = re.findall(r"\(?\s*([A-Za-z0-9_]+)\s*,\s*([0-9]+)\s*\)?", edges_str)
                        for neighbor, weight in matches:
                            edges.append((neighbor.strip(), int(weight.strip())))
                        parsed_graph[node] = edges

                    except Exception:
                        st.error(f"Error parsing line: {line}. Please check format.")
                        parsed_graph = {}
                        break
            data["graph"] = parsed_graph


        elif graph_input_method == "Upload Edge List (CSV/JSON)":
            uploaded_file = st.file_uploader("Upload edge list file (CSV or JSON)", type=["csv", "json"])
            if uploaded_file is not None:
                st.info("File upload parsing not fully implemented.")
                # Placeholder for actual file parsing logic
                data["graph"] = {}

        else: # Generate Random
            col1, col2 = st.columns(2)
            with col1:
                num_nodes = st.number_input("Number of Nodes:", min_value=2, max_value=20, value=5, step=1, key="random_graph_nodes")
            with col2:
                density = st.slider("Edge Density:", min_value=0.1, max_value=1.0, value=0.5, step=0.1, key="random_graph_density")
            weight_range = st.slider("Weight Range:", min_value=1, max_value=100, value=(1, 10), key="random_graph_weight_range")
            if st.button("Generate Random Graph"): # This button will trigger a re-run and new random graph
                import random
                nodes = [chr(65 + i) for i in range(num_nodes)] # A, B, C...
                generated_graph = {node: [] for node in nodes}
                for i in range(num_nodes):
                    for j in range(i + 1, num_nodes):
                        if random.random() < density:
                            weight = random.randint(weight_range[0], weight_range[1])
                            generated_graph[nodes[i]].append((nodes[j], weight))
                            generated_graph[nodes[j]].append((nodes[i], weight)) # Undirected
                st.session_state.generated_graph = generated_graph
            if "generated_graph" in st.session_state:
                data["graph"] = st.session_state.generated_graph
                st.write(f"Generated Graph: {data['graph']}")
            else:
                # Initial generation if not already present
                import random
                nodes = [chr(65 + i) for i in range(num_nodes)]
                generated_graph = {node: [] for node in nodes}
                for i in range(num_nodes):
                    for j in range(i + 1, num_nodes):
                        if random.random() < density:
                            weight = random.randint(weight_range[0], weight_range[1])
                            generated_graph[nodes[i]].append((nodes[j], weight))
                            generated_graph[nodes[j]].append((nodes[i], weight)) # Undirected
                st.session_state.generated_graph = generated_graph
                data["graph"] = st.session_state.generated_graph
                st.write(f"Generated Graph: {data['graph']}")
                # ✅ إضافة خانة Start Node لإجبار المستخدم يحددها
            start_node_input = st.text_input("Enter Start Node (e.g., A):", key="dijkstra_start_node_random")
            if start_node_input:
                data["start_node"] = start_node_input
            else:
                st.error("Start node cannot be empty for Dijkstra's algorithm.")
                data["start_node"] = None
    return data

def trace_io_buttons(on_load: Callable, on_save: Callable):
    """Renders buttons for loading and saving algorithm traces."""

    st.subheader("Trace Management")

    uploaded_file = st.file_uploader("Load Trace (JSON)", type=["json"], key="trace_uploader")
    if uploaded_file is not None:
        on_load(uploaded_file.getvalue().decode("utf-8"))

    if st.button("Save Current Trace", key="save_trace_button"):
        on_save()



def algorithm_analysis_panel(algorithm_name: str):
    """Displays a panel with time/space complexity and pedagogical notes.

    Args:
        algorithm_name (str): The name of the algorithm.
    """
    st.subheader(f"Analysis: {algorithm_name}")
    analysis_data = {
        "Merge Sort": {
            "Time Complexity": "O(n log n) in all cases (best, average, worst)",
            "Space Complexity": "O(n) due to temporary array",
            "Notes": "Merge Sort is a stable sorting algorithm. It is often preferred for sorting linked lists due to its efficient handling of sequential access. It's a divide-and-conquer algorithm."
        },
        "Quick Sort": {
            "Time Complexity": "O(n log n) average, O(n^2) worst-case",
            "Space Complexity": "O(log n) average (for recursion stack), O(n) worst-case",
            "Notes": "Quick Sort is an in-place, unstable sorting algorithm. It is generally faster in practice than other O(n log n) algorithms because of better cache performance and fewer swaps. It's also a divide-and-conquer algorithm."
        },
        "Linear Search": {
            "Time Complexity": "O(n) average and worst-case, O(1) best-case",
            "Space Complexity": "O(1)",
            "Notes": "Linear search is the simplest searching algorithm. It checks each element in the list sequentially until a match is found or the whole list has been searched."
        },
        "Kruskal (MST)": {
            "Time Complexity": "O(E log E) or O(E log V) where E is edges, V is vertices",
            "Space Complexity": "O(V + E)",
            "Notes": "Kruskal's algorithm finds a Minimum Spanning Tree (MST) for a connected, undirected graph. It's a greedy algorithm that adds the smallest weight edge that does not form a cycle."
        },
        "Dijkstra (SSSP)": {
            "Time Complexity": "O(E + V log V) with a Fibonacci heap, O(E log V) with a binary heap",
            "Space Complexity": "O(V + E)",
            "Notes": "Dijkstra's algorithm finds the shortest paths from a single source node to all other nodes in a graph with non-negative edge weights. It's a greedy algorithm."
        }
    }

    algo_info = analysis_data.get(algorithm_name, {"Time Complexity": "N/A", "Space Complexity": "N/A", "Notes": "No specific analysis available."})

    st.markdown(f"**Time Complexity:** {algo_info['Time Complexity']}")
    st.markdown(f"**Space Complexity:** {algo_info['Space Complexity']}")
    st.markdown(f"**Notes:** {algo_info['Notes']}")