"""
Shared types for the A* implementation.
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Node:
    id: int
    x: int
    y: int


@dataclass
class Edge:
    to: int
    weight: float


@dataclass
class Graph:
    nodes: Dict[int, Node]
    adj: Dict[int, List[Edge]]
    source: int
    destination: int

    def __init__(self):
        self.nodes = {}
        self.adj = {}
        self.source = -1
        self.destination = -1


@dataclass
class PathResult:
    found: bool
    cost: float
    path: List[int]
    expanded: int
    pushes: int
    max_frontier: int
    runtime_s: float