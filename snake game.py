import tkinter as tk
import random

WIDTH = 400
HEIGHT = 400
SIZE = 20

root = tk.Tk()
root.title("AI Snake Game")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

snake = [(100, 100)]
direction = "Right"

food = (
    random.randint(0, (WIDTH - SIZE) // SIZE) * SIZE,
    random.randint(0, (HEIGHT - SIZE) // SIZE) * SIZE
)

score = 0

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
            x, y, x + SIZE, y + SIZE,
            fill="green"
        )

    canvas.create_text(
        50, 10,
        text=f"Score: {score}",
        fill="white"
    )

def move():
    global food, score

    head_x, head_y = snake[0]

    if direction == "Right":
        head_x += SIZE
    elif direction == "Left":
        head_x -= SIZE
    elif direction == "Up":
        head_y -= SIZE
    elif direction == "Down":
        head_y += SIZE

    new_head = (head_x, head_y)

    # Collision
    if (
        head_x < 0 or head_x >= WIDTH or
        head_y < 0 or head_y >= HEIGHT or
        new_head in snake
    ):
        canvas.create_text(
            WIDTH//2, HEIGHT//2,
            text="GAME OVER",
            fill="white",
            font=("Arial", 20)
        )
        return

    snake.insert(0, new_head)

    if new_head == food:
        score += 1
        food = (
            random.randint(0, (WIDTH - SIZE)//SIZE) * SIZE,
            random.randint(0, (HEIGHT - SIZE)//SIZE) * SIZE
        )
    else:
        snake.pop()

    draw()
    root.after(150, move)

def change_direction(event):
    global direction

    if event.keysym == "Up" and direction != "Down":
        direction = "Up"
    elif event.keysym == "Down" and direction != "Up":
        direction = "Down"
    elif event.keysym == "Left" and direction != "Right":
        direction = "Left"
    elif event.keysym == "Right" and direction != "Left":
        direction = "Right"

root.bind("<Key>", change_direction)

draw()
move()

root.mainloop()

