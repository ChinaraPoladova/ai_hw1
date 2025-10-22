"""
Graph parser and builder.

Input format:
 - Ignore blank lines and lines starting with '#'
 - Lines can appear in any order:
   Vertex: "<id>,<cell_id>"        (one comma)
   Edge:   "<u>,<v>,<w>"           (two commas)
   Source: "S,<id>"
   Dest:   "D,<id>"

cell_id encodes coordinates:
  x = cell_id // 10
  y = cell_id % 10

Edges are undirected and weights assumed non-negative.
"""

from types import Graph, Node, Edge
from typing import TextIO


def parse_graph_file(path: str) -> Graph:
    g = Graph()
    with open(path, "r", encoding="utf-8") as fh:
        _parse_stream(fh, g)
    return g


def _parse_stream(fh: TextIO, g: Graph):
    for raw in fh:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        # Source
        if line.startswith("S"):
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 2:
                try:
                    g.source = int(parts[1])
                except ValueError:
                    pass
            continue

        # Destination
        if line.startswith("D"):
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 2:
                try:
                    g.destination = int(parts[1])
                except ValueError:
                    pass
            continue

        commas = line.count(",")
        parts = [p.strip() for p in line.split(",")]

        # Vertex line: id,cell_id
        if commas == 1 and len(parts) >= 2:
            try:
                vid = int(parts[0])
                cell = int(parts[1])
                node = Node(id=vid, x=cell // 10, y=cell % 10)
                g.nodes[vid] = node
            except ValueError:
                # malformed vertex line — ignore
                pass
            continue

        # Edge line: u,v,w  (undirected)
        if commas >= 2 and len(parts) >= 3:
            try:
                u = int(parts[0])
                v = int(parts[1])
                w = float(parts[2])
                g.adj.setdefault(u, []).append(Edge(to=v, weight=w))
                g.adj.setdefault(v, []).append(Edge(to=u, weight=w))
            except ValueError:
                # malformed edge line — ignore
                pass
            continue

        # Otherwise unknown line — ignore
        continue