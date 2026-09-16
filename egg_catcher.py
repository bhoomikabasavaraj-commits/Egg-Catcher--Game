from itertools import cycle
from random import randrange
import tkinter as tk
from tkinter import messagebox

# --- Game Configuration ---
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 400
EGG_SPEED = 500
EGG_INTERVAL = 1500
DIFFICULTY_FACTOR = 0.95

score = 0
lives_remaining = 3
egg_speed = EGG_SPEED

# --- Setup Window and Canvas ---
root = tk.Tk()
root.title("Egg Catcher Master")
root.resizable(False, False)

c = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT,
              background="deep sky blue")

# Ground
c.create_rectangle(
    -5, CANVAS_HEIGHT - 100,
    CANVAS_WIDTH + 5, CANVAS_HEIGHT + 5,
    fill="sea green", width=0
)

# Sun
c.create_oval(-10, -10, 120, 120, fill="orange", width=0)

c.pack()

# --- Game Objects Setup ---
color_cycle = cycle([
    "light blue", "light green",
    "light pink", "peach puff",
    "light yellow"
])

egg_width = 45
egg_height = 55
egg_score = 10

# Basket
basket = c.create_arc(
    CANVAS_WIDTH / 2 - 50,
    CANVAS_HEIGHT - 65,
    CANVAS_WIDTH / 2 + 50,
    CANVAS_HEIGHT - 15,
    start=200,
    extent=140,
    fill="chocolate",
    width=3
)

# UI
score_text = c.create_text(
    10, 10,
    anchor="nw",
    font=("Arial", 16, "bold"),
    fill="dark blue",
    text=f"Score: {score}"
)

lives_text = c.create_text(
    CANVAS_WIDTH - 10,
    10,
    anchor="ne",
    font=("Arial", 16, "bold"),
    fill="red",
    text=f"Lives: {lives_remaining}"
)

eggs = []


def create_egg():
    """Create a new egg at random x position."""
    x = randrange(40, CANVAS_WIDTH - 40)
    y = 40

    egg = c.create_oval(
        x, y,
        x + egg_width,
        y + egg_height,
        fill=next(color_cycle),
        width=2
    )

    eggs.append(egg)
    root.after(EGG_INTERVAL, create_egg)


def move_eggs():
    """Move eggs downward."""
    global score, lives_remaining, egg_speed

    for egg in eggs.copy():
        c.move(egg, 0, 10)

        egg_pos = c.coords(egg)

        if egg_pos:
            # Check if caught
            if egg_caught(egg_pos):
                eggs.remove(egg)
                c.delete(egg)

                score += egg_score
                c.itemconfigure(score_text, text=f"Score: {score}")

                egg_speed = max(50, int(egg_speed * DIFFICULTY_FACTOR))

            # Check if missed
            elif egg_pos[3] > CANVAS_HEIGHT:
                eggs.remove(egg)
                c.delete(egg)

                lives_remaining -= 1
                c.itemconfigure(
                    lives_text,
                    text=f"Lives: {lives_remaining}"
                )

                if lives_remaining == 0:
                    game_over()
                    return

    root.after(egg_speed, move_eggs)


def egg_caught(egg_pos):
    """Check collision with basket."""
    basket_pos = c.coords(basket)

    egg_center_x = (egg_pos[0] + egg_pos[2]) / 2
    egg_bottom_y = egg_pos[3]

    return (
        basket_pos[0] < egg_center_x < basket_pos[2]
        and basket_pos[1] < egg_bottom_y < basket_pos[3] + 20
    )


def move_left(event):
    basket_pos = c.coords(basket)

    if basket_pos[0] > 0:
        c.move(basket, -20, 0)


def move_right(event):
    basket_pos = c.coords(basket)

    if basket_pos[2] < CANVAS_WIDTH:
        c.move(basket, 20, 0)


def game_over():
    messagebox.showinfo(
        "Game Over",
        f"Final Score: {score}"
    )
    root.destroy()


# Keyboard Controls
root.bind("<Left>", move_left)
root.bind("<Right>", move_right)

# Start Game
create_egg()
move_eggs()

root.mainloop()
