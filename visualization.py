from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation


def create_figure(environment, path, navigator, result_path):
    fig, ax = plt.subplots(figsize=(12, 7))
    cmap = ListedColormap(["white", "black"])

    ax.imshow(
        environment.grid, cmap=cmap, origin="lower",
        interpolation="nearest",
        extent=[-0.5, environment.width-0.5, -0.5, environment.height-0.5]
    )

    if path:
        xs = [p[0] for p in path]
        ys = [p[1] for p in path]
        ax.plot(xs, ys, linewidth=2.5, label="A* planned path")

    sx, sy = environment.start
    gx, gy = environment.goal
    ax.scatter([sx], [sy], s=140, marker="s", label="Start")
    ax.scatter([gx], [gy], s=140, marker="s", label="Goal")

    agent, = ax.plot(
        [navigator.position[0]], [navigator.position[1]],
        marker="o", markersize=10, linestyle="None",
        label="Autonomous agent"
    )

    status = ax.text(
        0.99, 0.02, "", transform=ax.transAxes,
        ha="right", va="bottom",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
    )

    ax.set_title("AI-Based Autonomous Navigation System")
    ax.set_xlabel("X coordinate")
    ax.set_ylabel("Y coordinate")
    ax.set_xticks(range(0, environment.width, 2))
    ax.set_yticks(range(0, environment.height, 2))
    ax.grid(True, alpha=0.18)
    ax.legend(loc="upper left")

    def update():
        p = navigator.position
        if p:
            agent.set_data([p[0]], [p[1]])
            status.set_text(
                f"Progress: {navigator.progress():.0f}%\n"
                f"Remaining: {navigator.distance_remaining()} cells"
            )
        fig.canvas.draw_idle()

    def on_key(event):
        if event.key == "right":
            navigator.step()
            update()
        elif event.key == "r":
            navigator.index = 0
            update()
        elif event.key == "s":
            Path(result_path).parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(result_path, dpi=180, bbox_inches="tight")
            print(f"Screenshot saved to: {result_path}")

    fig.canvas.mpl_connect("key_press_event", on_key)

    def animate(_):
        if not navigator.finished:
            navigator.step()
            update()
        return agent, status

    animation = FuncAnimation(
        fig, animate, frames=max(1, len(path)),
        interval=80, repeat=False, blit=False
    )
    fig._navigation_animation = animation
    update()
    return fig
