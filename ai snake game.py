import tkinter as tk
import random
import heapq

# Window size
WIDTH = 400
HEIGHT = 400
SIZE = 20

root = tk.Tk()
root.title("AI Snake Game using A* Algorithm")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# Snake
snake = [(100, 100)]
score = 0

# Food
food = (
    random.randint(0, (WIDTH - SIZE)//SIZE) * SIZE,
    random.randint(0, (HEIGHT - SIZE)//SIZE) * SIZE
)

# ---------------- A* ALGORITHM ---------------- #

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(node):
    x, y = node
    neighbors = [
        (x + SIZE, y),
        (x - SIZE, y),
        (x, y + SIZE),
        (x, y - SIZE)
    ]

    valid = []

    for nx, ny in neighbors:
        if (
            0 <= nx < WIDTH and
            0 <= ny < HEIGHT and
            (nx, ny) not in snake
        ):
            valid.append((nx, ny))

    return valid

def astar(start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            path = []

            while current in came_from:
                path.append(current)
                current = came_from[current]

            path.reverse()
            return path

        for neighbor in get_neighbors(current):
            temp_g = g_score[current] + 1

            if neighbor not in g_score or temp_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                f_score[neighbor] = temp_g + heuristic(neighbor, goal)

                heapq.heappush(
                    open_set,
                    (f_score[neighbor], neighbor)
                )

    return []

# ---------------- DRAW FUNCTION ---------------- #

def draw():
    canvas.delete("all")

    # Food
    canvas.create_oval(
        food[0], food[1],
        food[0] + SIZE, food[1] + SIZE,
        fill="red"
    )

    # Snake
    for x, y in snake:
        canvas.create_rectangle(
            x, y,
            x + SIZE, y + SIZE,
            fill="green"
        )

    # Score
    canvas.create_text(
        60, 10,
        text=f"Score: {score}",
        fill="white",
        font=("Arial", 12)
    )

# ---------------- MOVE FUNCTION ---------------- #

def move():
    global food, score

    head = snake[0]

    path = astar(head, food)

    if path:
        new_head = path[0]
    else:
        canvas.create_text(
            WIDTH//2,
            HEIGHT//2,
            text="GAME OVER",
            fill="white",
            font=("Arial", 20)
        )
        return

    # Collision check
    if (
        new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT or
        new_head in snake
    ):
        canvas.create_text(
            WIDTH//2,
            HEIGHT//2,
            text="GAME OVER",
            fill="white",
            font=("Arial", 20)
        )
        return

    snake.insert(0, new_head)

    # Eat food
    if new_head == food:
        score += 1

        while True:
            food = (
                random.randint(0, (WIDTH - SIZE)//SIZE) * SIZE,
                random.randint(0, (HEIGHT - SIZE)//SIZE) * SIZE
            )

            if food not in snake:
                break

    else:
        snake.pop()

    draw()

    root.after(120, move)

# Start Game
draw()
move()

root.mainloop()