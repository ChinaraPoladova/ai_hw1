```markdown
A* (Three Modes) — Python implementation

This directory contains a Python implementation of A* that runs in three modes:
 - UCS (h = 0)
 - A* with Euclidean heuristic
 - A* with Manhattan heuristic

Files
- astar.py        — main A* implementation and CLI
- graph.py        — input parsing and graph construction
- heuristics.py   — pluggable heuristic functions
- types.py        — Node, Edge, Graph, PathResult dataclasses
- astar_small.txt — small test graph (5 nodes)
- astar_medium.txt— medium test graph (~30 nodes)

Build / Run
No build needed. Run with Python 3.8+.

Examples:
  python astar.py astar_small.txt
  python astar.py astar_medium.txt

Behavior & Implementation Notes
- Priority: f(n) = g(n) + h(n)
- Frontier (heap) entries are tuples (f, node_id, g). The second field (node_id) acts as
  a deterministic tie-breaker when f values are equal.
- Duplicate heap entries are allowed. An entry is expanded only when the popped g equals
  the best-known g for that node (stale entries are skipped).
- Heuristics are "pluggable" and must have signature h(node, goal).
  Implemented heuristics:
    - h_zero: returns 0 (UCS behaviour)
    - h_euclidean: Euclidean distance between grid coordinates
    - h_manhattan: Manhattan distance between grid coordinates
- Stats tracked & printed:
    Expanded = number of pops actually expanded
    Pushes = number of heap pushes
    Max frontier = peak heap size
    Runtime (s) = wall-clock time measured with time.perf_counter()

Input format
- Ignore blank lines and lines starting with #
- Lines can appear in any order:
  Vertex: <id>,<cell_id>
  Edge: <u>,<v>,<w>
  Source: S,<id>
  Destination: D,<id>

Coordinates:
- cell_id encodes grid coordinates:
  x = cell_id // 10
  y = cell_id % 10

Notes for the written analysis (include in your homework write-up)
1) Optimality
   - If heuristics are admissible and consistent, UCS and both A* runs should return the same optimal cost.
   - If costs differ across runs, inspect whether some edges have weights smaller than the geometric distances (which can make heuristics inadmissible).

2) Efficiency
   - Compare Expanded and Runtime across modes.
   - Expect (when heuristics are admissible and Manhattan dominates Euclidean):
     UCS (h=0) ≥ A* Euclidean ≥ A* Manhattan in expansions/runtime.

3) Heuristic validity
   - For Euclidean to be admissible, you would need every edge weight w(u,v) ≥ Euclidean(u,v).
   - For Manhattan to be admissible, every edge weight w(u,v) ≥ Manhattan(u,v).

Notes about this implementation
- Names and some identifiers were refactored to provide a clean and readable Python structure:
  - astar_search (main algorithm)
  - parse_graph_file (parser)
  - Types dataclasses (Node, Edge, Graph, PathResult)
  - heuristics module provides pluggable heuristics
- The core algorithmic behavior (f = g + h, duplicate entries allowed, deterministic tie-break) follows the assignment requirements.

If you want, I can:
- Run these files and paste the outputs for the included test files and provide the short analysis section filled with concrete numbers.
- Add an additional test file that demonstrates NO PATH or an example where heuristics are inadmissible.
```