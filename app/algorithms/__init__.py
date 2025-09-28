"""
This module makes the algorithm generator functions available
for easy import from the app.algorithms package.
"""
from .dijkstra import dijkstra_generator
from .kruskal import kruskal_generator
from .quick_sort import quick_sort_generator
from .merge_sort import merge_sort_generator
from .linear_search import linear_search_generator

__all__ = [
    "dijkstra_generator",
    "kruskal_generator",
    "quick_sort_generator",
    "merge_sort_generator",
    "linear_search_generator",
]