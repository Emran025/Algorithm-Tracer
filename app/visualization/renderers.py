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
    """Renders a graph, highlighting nodes and edges based on the current event.

    Args:
        snapshot (Dict[str, Any]): The snapshot dictionary from the VisualizationEngine,
                                   expected to contain a 'graph' key and 'current_event_data'.
        title (str): Title for the plot.

    Returns:
        plt.Figure: A Matplotlib Figure object.
    """
    graph_data = snapshot.get("graph", {})
    event_data = snapshot.get("current_event_data", {})
    distances = snapshot.get("distances", {})
    mst_edges = snapshot.get("mst_edges", [])

    G = nx.DiGraph() if snapshot.get("current_event_type") in ["relax", "set_distance"] else nx.Graph()

    # Add nodes and edges
    for u, neighbors in graph_data.items():
        G.add_node(u)
        for v, weight in neighbors:
            G.add_edge(u, v, weight=weight)

    pos = nx.spring_layout(G, seed=42) # For consistent layout

    fig, ax = plt.subplots(figsize=(10, 8))

    if not G.nodes:
        ax.text(0.5, 0.5, "Graph is empty", horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        ax.set_title(title)
        return fig

    # Default drawing
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=700, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color='gray', width=1, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', ax=ax)

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='green', ax=ax)

    # Highlight based on event type
    if snapshot.get("current_event_type") == "visit":
        node = event_data.get("u")
        if node in G.nodes: nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color='red', node_size=700, ax=ax)
    elif snapshot.get("current_event_type") == "consider_edge":
        u, v = event_data.get("u"), event_data.get("v")
        if G.has_edge(u, v): nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color='red', width=2, ax=ax)
        if G.has_edge(v, u) and not G.is_directed(): nx.draw_networkx_edges(G, pos, edgelist=[(v, u)], edge_color='red', width=2, ax=ax)
    elif snapshot.get("current_event_type") == "add_mst_edge":
        u, v = event_data.get("u"), event_data.get("v")
        if G.has_edge(u, v): nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color='blue', width=3, ax=ax)
        if G.has_edge(v, u) and not G.is_directed(): nx.draw_networkx_edges(G, pos, edgelist=[(v, u)], edge_color='blue', width=3, ax=ax)

    # Draw MST edges if available
    if mst_edges:
        nx.draw_networkx_edges(G, pos, edgelist=mst_edges, edge_color='blue', width=3, ax=ax)

    # Display distances if available (e.g., Dijkstra)
    if distances:
        for node, dist in distances.items():
            if node in pos:
                x, y = pos[node]
                ax.text(x, y + 0.1, f"D:{dist}", bbox=dict(facecolor='yellow', alpha=0.5), horizontalalignment='center')

    ax.set_title(f"{title} - Step: {snapshot.get('current_event_details', '')}")
    ax.axis('off')
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
    plt.show()

    array_snapshot_swap_example = {
        "array": [10, 5, 20, 30, 15],
        "current_event_type": "swap",
        "current_event_details": "Swapping elements at index 1 and 2",
        "current_event_data": {"i": 1, "j": 2}
    }
    fig_array_swap = render_array_bars(array_snapshot_swap_example, "Merge Sort Step (Swap)")
    plt.show()

    # Example usage for graph rendering
    graph_snapshot_example = {
        "graph": {
            "A": [("B", 1), ("C", 4)],
            "B": [("A", 1), ("C", 2), ("D", 5)],
            "C": [("A", 4), ("B", 2), ("D", 1)],
            "D": [("B", 5), ("C", 1)]
        },
        "current_event_type": "visit",
        "current_event_details": "Visiting node A",
        "current_event_data": {"u": "A"},
        "distances": {"A": 0, "B": float('inf'), "C": float('inf'), "D": float('inf')}
    }
    fig_graph = render_graph(graph_snapshot_example, "Dijkstra Step")
    plt.show()

    graph_snapshot_edge_example = {
        "graph": {
            "A": [("B", 1), ("C", 4)],
            "B": [("A", 1), ("C", 2), ("D", 5)],
            "C": [("A", 4), ("B", 2), ("D", 1)],
            "D": [("B", 5), ("C", 1)]
        },
        "current_event_type": "consider_edge",
        "current_event_details": "Considering edge B-C with weight 2",
        "current_event_data": {"u": "B", "v": "C", "weight": 2},
        "distances": {"A": 0, "B": 1, "C": float('inf'), "D": float('inf')}
    }
    fig_graph_edge = render_graph(graph_snapshot_edge_example, "Dijkstra Step (Edge)")
    plt.show()

    mst_graph_snapshot_example = {
        "graph": {
            "A": [("B", 1), ("C", 4)],
            "B": [("A", 1), ("C", 2), ("D", 5)],
            "C": [("A", 4), ("B", 2), ("D", 1)],
            "D": [("B", 5), ("C", 1)]
        },
        "current_event_type": "add_mst_edge",
        "current_event_details": "Adding edge A-B to MST",
        "current_event_data": {"u": "A", "v": "B", "weight": 1},
        "mst_edges": [("A", "B")]
    }
    fig_mst_graph = render_graph(mst_graph_snapshot_example, "Kruskal Step (MST Edge)")
    plt.show()

