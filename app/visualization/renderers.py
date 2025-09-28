import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from typing import List, Dict, Any, Tuple, Optional

def render_array_bars(snapshot: Dict[str, Any], title: str = "Array Visualization") -> plt.Figure:
    """Renders an array as a bar chart using rich visual metadata.

    This function is declarative: it draws the bar chart based on the colors
    provided in the snapshot's 'bar_colors' list.

    Args:
        snapshot (Dict[str, Any]): The snapshot dictionary from the VisualizationEngine.
                                   Expected to contain 'array' and 'bar_colors' keys.
        title (str): Title for the plot.

    Returns:
        plt.Figure: A Matplotlib Figure object.
    """
    arr = snapshot.get("array", [])
    bar_colors = snapshot.get("bar_colors", [])

    fig, ax = plt.subplots(figsize=(10, 6))
    if not arr:
        ax.text(0.5, 0.5, "Array is empty", horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        ax.set_title(title)
        return fig

    x = np.arange(len(arr))

    # Use the provided colors, or default to skyblue if not available
    colors = bar_colors if len(bar_colors) == len(arr) else ['skyblue'] * len(arr)

    bars = ax.bar(x, arr, color=colors, edgecolor='black', linewidth=0.7)

    ax.set_xticks(x)
    # Set X-tick labels to be the index of the array
    ax.set_xticklabels(x)
    ax.set_xlabel("Index")
    ax.set_ylabel("Value")
    ax.set_title(f"{title}: {snapshot.get('current_event_details', '')}", fontsize=14, weight='bold')

    # Adjust y-limit to provide more space for labels
    max_val = max(arr) if arr else 1
    ax.set_ylim(0, max_val * 1.25)

    # Add value labels on top of bars
    for i, bar in enumerate(bars):
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + (max_val * 0.02), arr[i], ha='center', va='bottom', fontsize=9)

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
        G, pos, edge_color=final_edge_colors, width=final_edge_widths
        # ,
        # arrows=is_directed, arrowstyle='-|>', arrowsize=20, ax=ax
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
    # --- Example for the new, declarative array renderer ---
    rich_array_snapshot = {
        "array": [3, 1, 4, 1, 5, 9, 2, 6],
        "bar_colors": [
            '#cccccc', '#cccccc', '#cccccc', '#cccccc', # Partition
            '#9370db', # Pivot
            '#ff9933', # Compare
            'skyblue', 'skyblue'
        ],
        "current_event_details": "Comparing 9 with pivot 5"
    }
    fig_rich_array = render_array_bars(rich_array_snapshot, "Quick Sort")
    print("Displaying declarative array renderer example...")
    plt.show()

    # --- Example for the declarative graph renderer (Dijkstra) ---
    rich_graph_snapshot = {
        "graph_snapshot": {
            'A': [('B', 4), ('C', 2)], 'B': [('A', 4), ('E', 3)],
            'C': [('A', 2), ('D', 2), ('F', 4)], 'D': [('C', 2), ('E', 3)],
            'E': [('B', 3), ('D', 3), ('F', 1)], 'F': [('C', 4), ('E', 1)]
        },
        "node_colors": {
            'A': '#2ca02c', 'B': '#2ca02c', 'C': '#2ca02c',
            'D': '#2ca02c', 'E': '#e6e6e6', 'F': '#2ca02c'
        },
        "edge_colors": {
            ('A', 'C'): '#2ca02c', ('C', 'F'): '#2ca02c', ('F', 'E'): '#e6e6e6',
            ('A', 'B'): '#2ca02c', ('C', 'D'): '#2ca02c', ('B', 'E'): '#e6e6e6',
            ('D', 'E'): '#e6e6e6'
        },
        "edge_widths": { t: 3.0 if c == '#2ca02c' else 1.0 for t, c in rich_graph_snapshot["edge_colors"].items() },
        "node_labels": {
            'A': 'A\n(0)', 'B': 'B\n(4)', 'C': 'C\n(2)',
            'D': 'D\n(4)', 'E': 'E\n(7)', 'F': 'F\n(6)'
        },
        "current_event_details": "Algorithm Completed"
    }
    fig_rich_graph = render_graph(rich_graph_snapshot, "Dijkstra's Algorithm (Final State)")
    print("Displaying declarative graph renderer example (Dijkstra)...")
    plt.show()

