import pygame
import random
import sys

# CONFIG
WIDTH, HEIGHT = 700, 700
ROWS, COLS = 30, 30
CELL = WIDTH // COLS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (70, 70, 70)
YELLOW = (255, 255, 0)
RED = (255, 80, 80)
BLUE = (80, 80, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Floyd-Warshall Maze Demo")
clock = pygame.time.Clock()

# MAZE GENERATION

maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]

def neighbors(r, c):
    dirs = [(2,0),(-2,0),(0,2),(0,-2)]
    for dr,dc in dirs:
        nr,nc = r+dr, c+dc
        if 0 <= nr < ROWS and 0 <= nc < COLS:
            yield nr, nc

def carve_maze(r, c):
    maze[r][c] = 0
    neigh = list(neighbors(r, c))
    random.shuffle(neigh)
    for nr, nc in neigh:
        if maze[nr][nc] == 1:
            maze[(r+nr)//2][(c+nc)//2] = 0
            carve_maze(nr, nc)

carve_maze(0, 0)

EXTRA_OPENINGS = 0.10

wall_cells = [(r, c) for r in range(ROWS) for c in range(COLS) if maze[r][c] == 1]
random.shuffle(wall_cells)

remove_count = int(len(wall_cells) * EXTRA_OPENINGS)

for i in range(remove_count):
    r, c = wall_cells[i]
    maze[r][c] = 0

# PRINT MAZE TO CONSOLE
print("\nMaze Matrix (1 = wall, 0 = open):\n")
for row in maze:
    print(" ".join(str(v) for v in row))
print("\n")

# GRAPH BUILDING

N = ROWS * COLS
INF = 10**9

dist = [[INF]*N for _ in range(N)]
next_node = [[-1]*N for _ in range(N)]

def idx(r,c): return r*COLS + c

for r in range(ROWS):
    for c in range(COLS):
        if maze[r][c] == 1:
            continue
        u = idx(r,c)
        dist[u][u] = 0
        next_node[u][u] = u

        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr,nc = r+dr, c+dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and maze[nr][nc] == 0:
                v = idx(nr,nc)
                dist[u][v] = 1
                next_node[u][v] = v

# Run Floyd Warshall
print("Running Floyd-Warshall...")

for k in range(N):
    for i in range(N):
        if dist[i][k] == INF:
            continue
        for j in range(N):
            if dist[k][j] == INF:
                continue
            if dist[i][j] > dist[i][k] + dist[k][j]:
                dist[i][j] = dist[i][k] + dist[k][j]
                next_node[i][j] = next_node[i][k]

# Draws heatmap
def draw_grid_with_heatmap(start, end):
    screen.fill(BLACK)

    max_dist = 0
    heatmap = [[-1 for _ in range(COLS)] for _ in range(ROWS)]

    if start is not None:
        for r in range(ROWS):
            for c in range(COLS):
                node = idx(r, c)
                d = dist[start][node]
                if d >= INF:
                    heatmap[r][c] = -1
                else:
                    heatmap[r][c] = d
                    max_dist = max(max_dist, d)

    for r in range(ROWS):
        for c in range(COLS):
            rect = (c*CELL, r*CELL, CELL, CELL)
            if maze[r][c] == 1:
                pygame.draw.rect(screen, BLACK, rect)
            else:
                if heatmap[r][c] == -1:
                    color = WHITE
                else:

                    t = heatmap[r][c] / max_dist if max_dist > 0 else 0
                    r_col = min(255, int(t * 255))
                    g_col = min(255, int((1-t) * 255))
                    b_col = 255 - r_col
                    color = (r_col, g_col, b_col)
                pygame.draw.rect(screen, color, rect)

                if heatmap[r][c] != -1:
                    font = pygame.font.SysFont(None, CELL // 2)
                    text = font.render(str(heatmap[r][c]), True, BLACK)
                    text_rect = text.get_rect(center=(c*CELL + CELL//2, r*CELL + CELL//2))
                    screen.blit(text, text_rect)

    if end is not None:
        r = end // COLS
        c = end % COLS
        pygame.draw.rect(screen, RED, (c*CELL, r*CELL, CELL, CELL))

    for i in range(ROWS):
        pygame.draw.line(screen, GREY, (0, i*CELL), (WIDTH, i*CELL))
    for j in range(COLS):
        pygame.draw.line(screen, GREY, (j*CELL, 0), (j*CELL, HEIGHT))

    pygame.display.flip()


# PATH RECONSTRUCTION

def get_path(u, v):
    if next_node[u][v] == -1:
        return []
    path = [u]
    while u != v:
        u = next_node[u][v]
        path.append(u)
    return path

# DRAWING

def draw_grid(path_nodes, start, end):
    screen.fill(BLACK)

    for r in range(ROWS):
        for c in range(COLS):
            rect = (c*CELL, r*CELL, CELL, CELL)
            if maze[r][c] == 1:
                pygame.draw.rect(screen, BLACK, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)

    for p in path_nodes:
        rr = p // COLS
        cc = p % COLS
        pygame.draw.rect(screen, YELLOW, (cc*CELL, rr*CELL, CELL, CELL))

    if start is not None:
        r = start // COLS
        c = start % COLS
        pygame.draw.rect(screen, BLUE, (c*CELL, r*CELL, CELL, CELL))

    if end is not None:
        r = end // COLS
        c = end % COLS
        pygame.draw.rect(screen, RED, (c*CELL, r*CELL, CELL, CELL))

    for i in range(ROWS):
        pygame.draw.line(screen, GREY, (0, i*CELL), (WIDTH, i*CELL))
    for j in range(COLS):
        pygame.draw.line(screen, GREY, (j*CELL, 0), (j*CELL, HEIGHT))

    pygame.display.flip()



# MAIN LOOP

start = None
end = None
path = []


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            r = my // CELL
            c = mx // CELL
            node = idx(r, c)
            if maze[r][c] == 1:
                continue

            if event.button == 1:
                start = node

            if event.button == 3:
                end = node

            if start is not None and end is not None:
                path = get_path(start, end)

    #Swap the commented out lines to see the 2 models
    draw_grid_with_heatmap(start, end)
    #This One
    # draw_grid(path, start, end)
    clock.tick(60)


