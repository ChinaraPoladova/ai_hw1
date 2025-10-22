"""
Pluggable heuristic implementations.
Each heuristic takes (node, goal) and returns a float.
"""

import math
from types import Node


def h_zero(node: Node, goal: Node) -> float:
    return 0.0


def h_euclidean(node: Node, goal: Node) -> float:
    dx = float(node.x - goal.x)
    dy = float(node.y - goal.y)
    return math.hypot(dx, dy)


def h_manhattan(node: Node, goal: Node) -> float:
    return float(abs(node.x - goal.x) + abs(node.y - goal.y))