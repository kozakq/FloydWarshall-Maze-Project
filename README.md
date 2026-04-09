# Floyd-Warshall Maze Visualization (Python / Pygame)

A Python application that generates a random maze, computes all-pairs shortest paths using the Floyd-Warshall algorithm, and visualizes distances and paths using Pygame.

---

## Features

### Maze Generation
- Generates a randomized maze using recursive backtracking
- Grid size: 30x30
- Additional random openings improve connectivity
- Maze is printed to console as a matrix (1 = wall, 0 = open) :contentReference[oaicite:1]{index=1}

---

### Graph Construction
- Each open cell is treated as a node in a graph
- Edges exist between adjacent walkable cells (up, down, left, right)
- Uses adjacency matrix representation
- Initializes:
  - Distance matrix (`dist`)
  - Path reconstruction matrix (`next_node`) :contentReference[oaicite:2]{index=2}

---

### Floyd-Warshall Algorithm
- Computes shortest paths between all pairs of nodes
- Time complexity: O(N³)
- Stores:
  - Minimum distance between all nodes
  - Next node for path reconstruction :contentReference[oaicite:3]{index=3}

---

### Visualization (Pygame)

#### Heatmap Mode (Default)
- Displays distance from selected start node to all reachable nodes
- Color gradient:
  - Green → close
  - Red → far
- Distance values displayed in each cell

#### Path Mode (Optional)
- Displays shortest path between start and end nodes
- Path highlighted in yellow

---

### User Interaction

- Left click → set start node
- Right click → set end node
- Automatically computes and displays:
  - Distance heatmap
  - Shortest path

---

## How It Works

1. Generate maze grid
2. Convert grid into graph
3. Run Floyd-Warshall to compute all shortest paths
4. Use `next_node` matrix to reconstruct paths
5. Render results with Pygame

---

## Requirements

- Python 3.x
- Pygame

Install dependencies:

```bash
pip install pygame
