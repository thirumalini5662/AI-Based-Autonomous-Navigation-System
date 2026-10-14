import heapq


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def astar(environment, start, goal):
    # Returns (path, expanded_nodes). Empty path means no route.
    if not environment.is_free(start) or not environment.is_free(goal):
        return [], 0

    open_heap = [(0, start)]
    came_from = {}
    g_score = {start: 0}
    visited = set()
    expanded = 0

    while open_heap:
        _, current = heapq.heappop(open_heap)
        if current in visited:
            continue

        visited.add(current)
        expanded += 1

        if current == goal:
            return reconstruct_path(came_from, current), expanded

        for neighbor in environment.neighbors(current):
            tentative_g = g_score[current] + 1
            if tentative_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + manhattan(neighbor, goal)
                heapq.heappush(open_heap, (f_score, neighbor))

    return [], expanded
