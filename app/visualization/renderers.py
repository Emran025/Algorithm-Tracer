import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from typing import List, Dict, Any, Tuple, Optional

def render_array_bars(snapshot: Dict[str, Any], title: str = "Array Visualization") -> plt.Figure:
    """Renders an array as a bar chart, highlighting specific indices.

    Args:
        snapshot (Dict[str, Any]): The snapshot dictionary from the VisualizationEngine,
                                   expected to contain an 'array' key and 'current_event_data'.
        title (str): Title for the plot.

    Returns:
        plt.Figure: A Matplotlib Figure object.
    """
    arr = snapshot.get("array", [])
    event_data = snapshot.get("current_event_data", {})

    fig, ax = plt.subplots(figsize=(10, 6))
    if not arr:
        ax.text(0.5, 0.5, "Array is empty", horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        ax.set_title(title)
        return fig

    x = np.arange(len(arr))
    bars = ax.bar(x, arr, color='skyblue')

    # Highlight elements involved in the current event
    highlight_color = 'red'
    compare_color = 'orange'
    pivot_color = 'purple'
    source_color = 'green'

    if snapshot.get("current_event_type") == "compare":
        i, j = event_data.get("i"), event_data.get("j")
        if i is not None and 0 <= i < len(arr): bars[i].set_color(compare_color)
        if j is not None and 0 <= j < len(arr): bars[j].set_color(compare_color)
    elif snapshot.get("current_event_type") == "swap":
        i, j = event_data.get("i"), event_data.get("j")
        if i is not None and 0 <= i < len(arr): bars[i].set_color(highlight_color)
        if j is not None and 0 <= j < len(arr): bars[j].set_color(highlight_color)
    elif snapshot.get("current_event_type") == "overwrite":
        idx = event_data.get("index")
        src_idx = event_data.get("source_index")
        if idx is not None and 0 <= idx < len(arr): bars[idx].set_color(highlight_color)
        if src_idx is not None and 0 <= src_idx < len(arr): bars[src_idx].set_color(source_color)
    elif snapshot.get("current_event_type") == "set_pivot":
        idx = event_data.get("index")
        if idx is not None and 0 <= idx < len(arr): bars[idx].set_color(pivot_color)
    elif snapshot.get("current_event_type") == "found":
        idx = event_data.get("index")
        if idx is not None and 0 <= idx < len(arr): bars[idx].set_color('lime')

    ax.set_xticks(x)
    ax.set_xticklabels([str(val) for val in arr]) # Show values on x-axis labels
    ax.set_xlabel("Index / Value")
    ax.set_ylabel("Value")
    ax.set_title(f"{title} - Step: {snapshot.get('current_event_details', '')}")
    ax.set_ylim(0, max(arr) * 1.2 if arr else 1)

    # Add value labels on top of bars
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 0.05, round(yval, 2), ha='center', va='bottom')

    plt.tight_layout()
    return fig

def render_graph(snapshot: Dict[str, Any], title: str = "Graph Visualization") -> plt.Figure:
    """Renders a graph using rich visual metadata from a snapshot.

    This function is declarative: it draws the graph based on the colors, widths,
    and labels provided in the snapshot, without needing to know the underlying
    algorithm logic.

    Args:
        snapshot (Dict[str, Any]): The snapshot dictionary from the VisualizationEngine.
                                   It is expected to contain keys like 'graph_snapshot',
                                   'node_colors', 'edge_colors', 'edge_widths', and 'node_labels'.
        title (str): Title for the plot.

    Returns:
        plt.Figure: A Matplotlib Figure object.
    """
    graph_data = snapshot.get("graph_snapshot", {})
    if not graph_data:
        fig, ax = plt.subplots(figsize=(12, 10))
        ax.text(0.5, 0.5, "Graph is empty or not provided in this step.",
                horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        ax.set_title(title)
        return fig

    # Determine if the graph is directed (for Dijkstra) or not (for Kruskal)
    # A simple heuristic: if any edge u->v doesn't have a v->u counterpart.
    is_directed = False
    if snapshot.get("current_event_type") in ["visit", "relax"]: # Event types specific to Dijkstra
        is_directed = True

    G = nx.DiGraph() if is_directed else nx.Graph()

    # Add nodes and edges from the raw graph data
    for u, neighbors in graph_data.items():
        G.add_node(u)
        for v, weight in neighbors:
            G.add_edge(u, v, weight=weight)

    pos = nx.spring_layout(G, seed=42, k=0.9)  # For consistent and spaced-out layout

    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_title(f"{title}: {snapshot.get('current_event_details', '')}", fontsize=16, weight='bold')
    ax.axis('off')

    # Get visual properties from the snapshot
    node_colors = snapshot.get("node_colors", {})
    edge_colors_map = snapshot.get("edge_colors", {})
    edge_widths_map = snapshot.get("edge_widths", {})
    node_labels = snapshot.get("node_labels", {n: str(n) for n in G.nodes()})

    # Prepare lists for drawing, ensuring order matches G.nodes() and G.edges()
    final_node_colors = [node_colors.get(n, 'gray') for n in G.nodes()]

    final_edge_colors = []
    final_edge_widths = []
    for u, v in G.edges():
        edge_tuple = tuple(sorted((u, v)))
        final_edge_colors.append(edge_colors_map.get(edge_tuple, 'gray'))
        final_edge_widths.append(edge_widths_map.get(edge_tuple, 1.0))

    # Draw the graph with specified styles
    nx.draw_networkx_nodes(
        G, pos, node_color=final_node_colors, node_size=800,
        edgecolors="black", linewidths=1.0, ax=ax
    )
    nx.draw_networkx_edges(
        G, pos, edge_color=final_edge_colors, width=final_edge_widths,
        arrows=is_directed, arrowstyle='-|>', arrowsize=20, ax=ax
    )

    # Draw node labels (potentially multi-line)
    nx.draw_networkx_labels(
        G, pos, labels=node_labels, font_size=10, font_weight='bold',
        font_color='black', ax=ax
    )

    # Draw edge weight labels
    edge_weight_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_weight_labels, font_color='#333333',
        font_size=9, bbox=dict(facecolor='white', alpha=0.5, edgecolor='none', boxstyle='round,pad=0.2'),
        ax=ax
    )

    plt.tight_layout()
    return fig


if __name__ == '__main__':
    # Example usage for array rendering
    array_snapshot_example = {
        "array": [10, 20, 5, 30, 15],
        "current_event_type": "compare",
        "current_event_details": "Comparing elements at index 1 and 2",
        "current_event_data": {"i": 1, "j": 2}
    }
    fig_array = render_array_bars(array_snapshot_example, "Merge Sort Step")
    # plt.show() # Uncomment to display during local testing

    # Example usage for the new, rich graph rendering
    rich_graph_snapshot = {
        "graph_snapshot": {
            'A': [('B', 4), ('C', 2)], 'B': [('A', 4), ('E', 3)],
            'C': [('A', 2), ('D', 2), ('F', 4)], 'D': [('C', 2), ('E', 3)],
            'E': [('B', 3), ('D', 3), ('F', 1)], 'F': [('C', 4), ('E', 1)]
        },
        "node_colors": {
            'A': '#cccccc', 'B': '#cccccc', 'C': '#ff9933', 'D': '#66b3ff',
            'E': '#66b3ff', 'F': '#66b3ff'
        },
        "edge_colors": {
            ('A', 'B'): '#333333', ('A', 'C'): '#333333', ('C', 'D'): '#3399ff',
            ('C', 'F'): '#b3b3b3', ('B', 'E'): '#b3b3b3', ('D', 'E'): '#b3b3b3',
            ('E', 'F'): '#b3b3b3'
        },
        "edge_widths": {
            ('A', 'B'): 3.0, ('A', 'C'): 3.0, ('C', 'D'): 2.5,
            ('C', 'F'): 1.5, ('B', 'E'): 1.5, ('D', 'E'): 1.5, ('E', 'F'): 1.5
        },
        "node_labels": {
            'A': 'A\n(0)', 'B': 'B\n(4)', 'C': 'C\n(2)',
            'D': 'D\n(∞)', 'E': 'E\n(∞)', 'F': 'F\n(∞)'
        },
        "current_event_type": "visit",
        "current_event_details": "Visiting Node C, considering edge C->D"
    }

    fig_rich_graph = render_graph(rich_graph_snapshot, "Dijkstra's Algorithm")
    plt.show() # Display the rich graph visualization

    # Example for Kruskal's with different colors
    kruskal_snapshot = {
        "graph_snapshot": {
            "A": [("B", 7), ("D", 5)], "B": [("C", 8)], "D": [("F", 6)], "C": [("E", 5)], "E": [], "F": []
        },
        "node_colors": {
            'A': '#440154', 'B': '#440154', 'D': '#440154', 'F': '#440154', # Set 1
            'C': '#21908d', 'E': '#21908d' # Set 2
        },
        "edge_colors": {
            ('A', 'D'): '#333333', ('C', 'E'): '#333333', ('D', 'F'): '#333333',
            ('A', 'B'): '#ff6666' # Rejected edge
        },
        "edge_widths": {
            ('A', 'D'): 3.0, ('C', 'E'): 3.0, ('D', 'F'): 3.0, ('A', 'B'): 2.5
        },
        "node_labels": {'A':'A', 'B':'B', 'C':'C', 'D':'D', 'E':'E', 'F':'F'},
        "current_event_type": "reject_edge",
        "current_event_details": "Rejecting edge A-B (forms a cycle)"
    }
    fig_kruskal_graph = render_graph(kruskal_snapshot, "Kruskal's Algorithm")
    plt.show()

