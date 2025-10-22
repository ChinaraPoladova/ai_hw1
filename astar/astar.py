"""
A* search program (three modes) in Python.

Usage:
    python astar.py <input_file>

Runs:
 - UCS (h = 0)
 - A* (Euclidean)
 - A* (Manhattan)

Outputs per mode:
MODE: <UCS | A* Euclidean | A* Manhattan>
Optimal cost: <number | NO PATH>
Path: <S -> ... -> D>    (omitted if NO PATH)
Expanded: <int>
Pushes: <int>
Max frontier: <int>
Runtime (s): <float>
"""

import heapq
import time
from typing import Callable, Dict, List, Tuple

from types import Graph, PathResult
from graph import parse_graph_file
 import heuristics


def astar_search(graph: Graph, start: int, goal: int,
                 heuristic: Callable[[object, object], float]) -> PathResult:
    t0 = time.perf_counter()

    # initialize g-costs to +inf
    g_cost: Dict[int, float] = {nid: float("inf") for nid in graph.nodes}
    if start not in graph.nodes or goal not in graph.nodes:
        t1 = time.perf_counter()
        return PathResult(False, 0.0, [], 0, 0, 0, t1 - t0)

    g_cost[start] = 0.0
    parent: Dict[int, int] = {}

    # heap entries: (f, node_id, g)
    # tie-break deterministically by node_id when f equal
    heap: List[Tuple[float, int, float]] = []
    start_f = heuristic(graph.nodes[start], graph.nodes[goal])
    heapq.heappush(heap, (start_f, start, 0.0))
    pushes = 1
    expanded = 0
    max_frontier = max(1, len(heap))

    while heap:
        f, nid, g = heapq.heappop(heap)

        # Skip stale entries: expand only if popped g equals best-known g
        if g > g_cost.get(nid, float("inf")):
            continue

        expanded += 1

        # goal test
        if nid == goal:
            t1 = time.perf_counter()
            # reconstruct path
            path: List[int] = []
            cur = goal
            while cur != start:
                path.append(cur)
                cur = parent[cur]
            path.append(start)
            path.reverse()
            return PathResult(True, g_cost[goal], path, expanded, pushes, max_frontier, t1 - t0)

        # expand neighbors
        for edge in graph.adj.get(nid, []):
            tentative = g + edge.weight
            if tentative < g_cost.get(edge.to, float("inf")):
                g_cost[edge.to] = tentative
                parent[edge.to] = nid
                f2 = tentative + heuristic(graph.nodes[edge.to], graph.nodes[goal])
                heapq.heappush(heap, (f2, edge.to, tentative))
                pushes += 1

        if len(heap) > max_frontier:
            max_frontier = len(heap)

    t1 = time.perf_counter()
    return PathResult(False, 0.0, [], expanded, pushes, max_frontier, t1 - t0)


def print_result(mode: str, res: PathResult):
    print(f"MODE: {mode}")
    if not res.found:
        print("Optimal cost: NO PATH")
    else:
        # pretty print integer costs without decimals when appropriate
        cost_str = f"{res.cost:.6f}"
        if abs(res.cost - round(res.cost)) < 1e-9:
            cost_str = f"{int(round(res.cost))}"
        print(f"Optimal cost: {cost_str}")
        print("Path: " + " -> ".join(str(n) for n in res.path))
    print(f"Expanded: {res.expanded}")
    print(f"Pushes: {res.pushes}")
    print(f"Max frontier: {res.max_frontier}")
    print(f"Runtime (s): {res.runtime_s:.6f}")
    print()


def main(argv=None):
    import sys
    argv = argv if argv is not None else sys.argv
    if len(argv) < 2:
        print("Usage: python astar.py <input_file>")
        return 1

    path = argv[1]
    graph = parse_graph_file(path)

    r1 = astar_search(graph, graph.source, graph.destination, heuristics.h_zero)
    print_result("UCS (h=0)", r1)

    r2 = astar_search(graph, graph.source, graph.destination, heuristics.h_euclidean)
    print_result("A* Euclidean", r2)

    r3 = astar_search(graph, graph.source, graph.destination, heuristics.h_manhattan)
    print_result("A* Manhattan", r3)

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))