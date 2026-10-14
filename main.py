from pathlib import Path
from .config import GRID_WIDTH, GRID_HEIGHT, START, GOAL, RANDOM_SEED, OBSTACLE_DENSITY, RESULT_PATH
from .environment import GridEnvironment
from .planner import astar
from .navigator import Navigator
from .visualization import create_figure


def run():
    print("=" * 60)
    print("AI-Based Autonomous Navigation System")
    print("=" * 60)
    print(f"Environment: {GRID_WIDTH} x {GRID_HEIGHT} grid")
    print(f"Start: {START}")
    print(f"Goal:  {GOAL}")

    env = GridEnvironment(
        GRID_WIDTH, GRID_HEIGHT,
        obstacle_density=OBSTACLE_DENSITY,
        seed=RANDOM_SEED,
        start=START, goal=GOAL
    )

    print("Planning path with A*...")
    path, expanded = astar(env, START, GOAL)

    if not path:
        print("No path found. Try changing RANDOM_SEED or OBSTACLE_DENSITY.")
        return

    print("Path found successfully.")
    print(f"Path length: {len(path)} cells")
    print(f"Expanded nodes: {expanded}")
    print("Starting autonomous navigation...")
    print("Controls: RIGHT = next step | R = reset | S = save screenshot")

    navigator = Navigator(path)
    Path(RESULT_PATH).parent.mkdir(parents=True, exist_ok=True)

    fig = create_figure(env, path, navigator, RESULT_PATH)
    fig.savefig(RESULT_PATH, dpi=180, bbox_inches="tight")

    import matplotlib.pyplot as plt
    plt.show()

    print("Navigation completed.")
    print(f"Final result image: {RESULT_PATH}")


if __name__ == "__main__":
    run()
