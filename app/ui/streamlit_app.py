import streamlit as st
import time
import json
from typing import List, Dict, Any, Optional

import matplotlib.pyplot as plt
from app.visualization.engine import VisualizationEngine
from app.visualization.renderers import render_array_bars, render_graph
from app.algorithms.merge_sort import merge_sort_generator
# Import other algorithm generators here as they are implemented
from app.algorithms.linear_search import linear_search_generator
from app.algorithms.quick_sort import quick_sort_generator
from app.algorithms.kruskal import kruskal_generator
from app.algorithms.dijkstra import dijkstra_generator

from app.ui.components import playback_controls, data_input_form, trace_io_buttons, algorithm_analysis_panel
from app.utils.types import Event

st.set_page_config(layout="wide", page_title="AlgoVisEdu")

# --- Session State Initialization ---
if "algorithm_name" not in st.session_state: st.session_state.algorithm_name = "Merge Sort"
if "trace" not in st.session_state: st.session_state.trace = []
if "engine" not in st.session_state: st.session_state.engine = None
if "current_step_index" not in st.session_state: st.session_state.current_step_index = 0
if "is_playing" not in st.session_state: st.session_state.is_playing = False
if "playback_speed" not in st.session_state: st.session_state.playback_speed = 1.0
if "generated_array" not in st.session_state: st.session_state.generated_array = None
if "generated_graph" not in st.session_state: st.session_state.generated_graph = None

# --- Algorithm Mapping ---
algorithms = {
    "Merge Sort": {"generator": merge_sort_generator, "type": "array"},
    "Quick Sort": {"generator": quick_sort_generator, "type": "array"},
    "Linear Search": {"generator": linear_search_generator, "type": "array"},
    "Kruskal (MST)": {"generator": kruskal_generator, "type": "graph"},
    "Dijkstra (SSSP)": {"generator": dijkstra_generator, "type": "graph"},
}

# --- Callbacks ---
def generate_trace(algo_name: str, input_data: Dict[str, Any]):
    """Generates a new trace for the selected algorithm and input data."""
    st.session_state.is_playing = False
    generator_func = algorithms[algo_name]["generator"]
    try:
        if algorithms[algo_name]["type"] == "array":
            if not input_data.get("array"): raise ValueError("Array input cannot be empty.")
            if algo_name == "Linear Search":
                target = input_data.get("target")
                if target is None: raise ValueError("Target value is required for Linear Search.")
                trace_events = list(generator_func(list(input_data["array"]), target))
            else:
                trace_events = list(generator_func(list(input_data["array"])))
        elif algorithms[algo_name]["type"] == "graph":
            if not input_data.get("graph"): raise ValueError("Graph input cannot be empty.")
            if algo_name == "Dijkstra (SSSP)":
                start_node = input_data.get("start_node")
                if not start_node: raise ValueError("Start node is required for Dijkstra's algorithm.")
                trace_events = list(generator_func(input_data["graph"], start_node))
            else:
                trace_events = list(generator_func(input_data["graph"]))
        else:
            trace_events = []

        st.session_state.trace = trace_events
        st.session_state.engine = VisualizationEngine(trace_events)
        st.session_state.current_step_index = 0
        st.success(f"Trace generated for {algo_name}!")
    except Exception as e:
        st.error(f"Error generating trace: {e}")
        st.session_state.trace = []
        st.session_state.engine = None
        st.session_state.current_step_index = 0

def load_trace_from_json(json_string: str):
    """Loads a trace from a JSON string."""
    st.session_state.is_playing = False
    try:
        events_data = json.loads(json_string)
        events = [Event(step=d["step"], type=d["type"], details=d["details"], data={k: v for k, v in d.items() if k not in ["step", "type", "details"]}) for d in events_data]
        st.session_state.trace = events
        st.session_state.engine = VisualizationEngine(events)
        st.session_state.current_step_index = 0
        st.success("Trace loaded successfully!")
    except json.JSONDecodeError:
        st.error("Invalid JSON file. Please upload a valid trace JSON.")
    except Exception as e:
        st.error(f"Error loading trace: {e}")

def save_current_trace():
    """Saves the current trace to a JSON file."""
    if st.session_state.engine:
        trace_json = st.session_state.engine.get_trace_json()
        st.download_button(
            label="Download Trace JSON",
            data=trace_json,
            file_name=f"{st.session_state.algorithm_name.replace(" ", "_").lower()}_trace.json",
            mime="application/json",
            key="download_trace_button"
        )
    else:
        st.warning("No trace to save. Generate or load a trace first.")

def step_forward():
    if st.session_state.engine and st.session_state.current_step_index < st.session_state.engine.step_count - 1:
        st.session_state.current_step_index += 1

def step_back():
    if st.session_state.engine and st.session_state.current_step_index > 0:
        st.session_state.current_step_index -= 1

def seek_to_step(step_index: int):
    if st.session_state.engine and 0 <= step_index < st.session_state.engine.step_count:
        st.session_state.current_step_index = step_index

# --- UI Layout ---
st.title("AlgoVisEdu: Algorithm Visualizer & Educator")

# Sidebar for algorithm selection and input
with st.sidebar:
    st.header("Configuration")
    selected_algo = st.selectbox(
        "Select Algorithm",
        list(algorithms.keys()),
        key="algo_selector",
        on_change=lambda: st.session_state.update(algorithm_name=st.session_state.algo_selector, trace=[], engine=None, current_step_index=0, is_playing=False)
    )
    st.session_state.algorithm_name = selected_algo

    algo_type = algorithms[st.session_state.algorithm_name]["type"]
    input_data = data_input_form(algo_type , st.session_state.algorithm_name)

    if st.button("Run Algorithm", type="primary"):
        generate_trace(st.session_state.algorithm_name, input_data)

    trace_io_buttons(load_trace_from_json, save_current_trace)

# Main content area
col_viz, col_details = st.columns([3, 1])

with col_viz:
    st.header("Visualization")
    if st.session_state.engine:
        st.session_state.engine.seek(st.session_state.current_step_index)
        snapshot = st.session_state.engine.get_snapshot()

        if algo_type == "array":
            fig = render_array_bars(snapshot, f"{st.session_state.algorithm_name} Visualization")
        elif algo_type == "graph":
            fig = render_graph(snapshot, f"{st.session_state.algorithm_name} Visualization")
        else:
            st.warning("Unsupported algorithm type for visualization.")
            fig = plt.figure()

        st.pyplot(fig)
        plt.close(fig) # Close the figure to prevent memory leaks

        # Playback controls
        playback_controls(
            on_play=lambda: st.session_state.update(is_playing=True),
            on_pause=lambda: st.session_state.update(is_playing=False),
            on_step_forward=step_forward,
            on_step_back=step_back,
            on_seek=seek_to_step,
            current_step_index=st.session_state.current_step_index,
            total_steps=st.session_state.engine.step_count,
            is_playing=st.session_state.is_playing,
            speed=st.session_state.playback_speed
        )

        # Auto-play logic
        if st.session_state.is_playing and st.session_state.current_step_index < st.session_state.engine.step_count - 1:
            time.sleep(0.3 / st.session_state.playback_speed)
            st.session_state.current_step_index += 1
            st.rerun()
        elif st.session_state.is_playing and st.session_state.current_step_index == st.session_state.engine.step_count - 1:
            st.session_state.is_playing = False # Stop playing at the end

    else:
        st.info("Select an algorithm and input data, then click 'Run Algorithm' to start visualization.")

with col_details:
    st.header("Event Details")
    if st.session_state.engine:
        current_event = st.session_state.engine.current_event
        st.markdown(f"**Step {current_event.step}:** {current_event.details}")
        if current_event.data:
            with st.expander("Raw Event Data"):
                st.json(current_event.to_json_serializable())

        # Display final output on the last step
        is_final_step = st.session_state.current_step_index == st.session_state.engine.step_count - 1
        if is_final_step and current_event.type == "done":
            st.header("Final Output")
            final_data = current_event.data
            algo_type = algorithms[st.session_state.algorithm_name]["type"]
            algo_name = st.session_state.algorithm_name

            if algo_type == "array":
                if "array" in final_data:
                    st.success(f"Final Array: `{final_data['array']}`")
                if algo_name == "Linear Search":
                    if "found" in final_data and final_data["found"]:
                        st.success(f"Target found at index: `{final_data.get('found_index', 'N/A')}`")
                    elif "found" in final_data:
                        st.info("Target not found in the array.")

            elif algo_type == "graph":
                if algo_name == "Kruskal (MST)" and "mst_edges" in final_data:
                    st.success("Minimum Spanning Tree (MST):")
                    st.code(json.dumps(final_data['mst_edges'], indent=2), language="json")
                elif algo_name == "Dijkstra (SSSP)" and "distances" in final_data:
                    st.success("Shortest Path Distances:")
                    distances_str = {str(k): (v if v != float('inf') else 'Infinity') for k, v in final_data['distances'].items()}
                    st.code(json.dumps(distances_str, indent=2), language="json")
    else:
        st.info("Event details will appear here.")

    st.header("Algorithm Analysis")
    algorithm_analysis_panel(st.session_state.algorithm_name)


# Placeholder for matplotlib to avoid issues when not displaying a plot
import matplotlib.pyplot as plt
plt.close('all')