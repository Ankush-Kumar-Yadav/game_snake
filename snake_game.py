import tkinter as tk
import random

class SnakeGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Snake Game")
        self.root.geometry("400x400")

        self.canvas = tk.Canvas(self.root, bg="white", width=400, height=400)
        self.canvas.pack()

        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.food = self.generate_food()

        self.direction = "Right"
        self.next_direction = "Right"

        self.score = 0
        self.score_label = tk.Label(self.root, text="Score: 0")
        self.score_label.pack()

        self.game_over_label = tk.Label(self.root, text="", font=("Helvetica", 16))
        self.game_over_label.pack()

        self.restart_button = tk.Button(self.root, text="Restart Game", command=self.restart_game)
        self.restart_button.pack()

        self.root.bind("<Up>", self.set_direction_up)
        self.root.bind("<Down>", self.set_direction_down)
        self.root.bind("<Left>", self.set_direction_left)
        self.root.bind("<Right>", self.set_direction_right)

        self.root.after(100, self.update)

    def generate_food(self):
        x = random.randrange(1, 39) * 10
        y = random.randrange(1, 39) * 10
        return x, y

    def draw_snake(self):
        self.canvas.delete("snake")
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 10, segment[1] + 10, fill="green", tag="snake")

    def draw_food(self):
        self.canvas.create_oval(self.food[0], self.food[1], self.food[0] + 10, self.food[1] + 10, fill="red", tag="food")

    def update(self):
        if not self.game_over():
            self.direction = self.next_direction
            self.move_snake()
            self.check_collision()
            self.check_food_collision()
            self.draw_snake()
            self.draw_food()
            self.root.after(100, self.update)
        else:
            self.game_over_label.config(text="Game Over!")
            self.restart_button.config(state=tk.NORMAL)

    def move_snake(self):
        head = self.snake[0]
        new_head = (head[0] + (10 if self.direction == "Right" else -10),
                    head[1] + (10 if self.direction == "Down" else -10))
        self.snake.insert(0, new_head)
        if not self.check_food_collision():
            self.snake.pop()

    def check_food_collision(self):
        if self.snake[0] == self.food:
            self.food = self.generate_food()
            self.score += 10
            self.score_label.config(text="Score: {}".format(self.score))
            return True
        return False

    def check_collision(self):
        head = self.snake[0]
        if head[0] < 0 or head[0] >= 400 or head[1] < 0 or head[1] >= 400:
            self.game_over_label.config(text="Game Over!")
            self.restart_button.config(state=tk.NORMAL)
            return True
        for segment in self.snake[1:]:
            if head == segment:
                self.game_over_label.config(text="Game Over!")
                self.restart_button.config(state=tk.NORMAL)
                return True
        return False

    def set_direction_up(self, event):
        if self.direction != "Down":
            self.next_direction = "Up"

    def set_direction_down(self, event):
        if self.direction != "Up":
            self.next_direction = "Down"

    def set_direction_left(self, event):
        if self.direction != "Right":
            self.next_direction = "Left"

    def set_direction_right(self, event):
        if self.direction != "Left":
            self.next_direction = "Right"

    def restart_game(self):
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.food = self.generate_food()
        self.direction = "Right"
        self.next_direction = "Right"
        self.score = 0
        self.score_label.config(text="Score: 0")
        self.game_over_label.config(text="")
        self.restart_button.config(state=tk.DISABLED)
        self.update()

if __name__ == "__main__":
    game = SnakeGame()
    game.root.mainloop()
