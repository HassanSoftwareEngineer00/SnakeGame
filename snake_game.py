

import tkinter as tk
from tkinter import messagebox
import random


class SnakeGame:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.root.resizable(False, False)
        
        self.GAME_WIDTH = 600
        self.GAME_HEIGHT = 600
        self.SPEED = 100
        self.SPACE_SIZE = 20
        self.BODY_PARTS = 3
        self.SNAKE_COLOR = "#FFC400"
        self.FOOD_COLOR = "#AFFCEB"
        self.BACKGROUND_COLOR = "#000000"
        
        self.score = 0
        self.direction = 'down'
        self.game_running = False
        
        self.setup_ui()
        self.start_new_game()
    
    def setup_ui(self):
        self.score_label = tk.Label(
            self.root,
            text=f"Score: {self.score}",
            font=('consolas', 20),
            bg='#1a1a1a',
            fg='white',
            pady=10
        )
        self.score_label.pack()
        
        self.canvas = tk.Canvas(
            self.root,
            bg=self.BACKGROUND_COLOR,
            height=self.GAME_HEIGHT,
            width=self.GAME_WIDTH
        )
        self.canvas.pack()
        
        button_frame = tk.Frame(self.root, bg='#1a1a1a')
        button_frame.pack(fill='x', pady=10)
        
        self.start_button = tk.Button(
            button_frame,
            text="Start Game",
            font=('consolas', 14),
            command=self.start_new_game,
            bg='#00FF00',
            fg='black',
            padx=20
        )
        self.start_button.pack(side='left', padx=20)
        
        self.pause_button = tk.Button(
            button_frame,
            text="Pause",
            font=('consolas', 14),
            command=self.toggle_pause,
            bg='#FFA500',
            fg='black',
            padx=20
        )
        self.pause_button.pack(side='left', padx=20)
        
        instructions = tk.Label(
            self.root,
            text="Use Arrow Keys to control the snake",
            font=('consolas', 12),
            bg='#1a1a1a',
            fg='white',
            pady=5
        )
        instructions.pack()
        
        self.root.bind('<Left>', lambda event: self.change_direction('left'))
        self.root.bind('<Right>', lambda event: self.change_direction('right'))
        self.root.bind('<Up>', lambda event: self.change_direction('up'))
        self.root.bind('<Down>', lambda event: self.change_direction('down'))
        
        self.root.bind('<a>', lambda event: self.change_direction('left'))
        self.root.bind('<d>', lambda event: self.change_direction('right'))
        self.root.bind('<w>', lambda event: self.change_direction('up'))
        self.root.bind('<s>', lambda event: self.change_direction('down'))
        
        self.root.configure(bg='#1a1a1a')
    
    def start_new_game(self):
        self.canvas.delete('all')
        self.score = 0
        self.direction = 'down'
        self.score_label.config(text=f"Score: {self.score}")
        
        self.snake = Snake(self)
        
        self.food = Food(self)
        
        self.game_running = True
        self.start_button.config(bg='#00FF00')  
        self.pause_button.config(bg='#00FF00')  
        self.next_turn()
    
    def toggle_pause(self):
        self.game_running = not self.game_running
        if self.game_running:
            self.pause_button.config(text="Pause", bg='#00FF00')  
            self.start_button.config(bg='#00FF00')  
            self.next_turn()
        else:
            self.pause_button.config(text="Resume", bg='#FF0000')  
            self.start_button.config(bg='#FF0000')  
    
    def next_turn(self):
        if not self.game_running:
            return
        
        x, y = self.snake.coordinates[0]
        
        if self.direction == "up":
            y -= self.SPACE_SIZE
        elif self.direction == "down":
            y += self.SPACE_SIZE
        elif self.direction == "left":
            x -= self.SPACE_SIZE
        elif self.direction == "right":
            x += self.SPACE_SIZE
        
        self.snake.coordinates.insert(0, (x, y))
        
        square = self.canvas.create_rectangle(
            x, y, x + self.SPACE_SIZE, y + self.SPACE_SIZE,
            fill=self.SNAKE_COLOR
        )
        
        self.snake.squares.insert(0, square)
        
        if x == self.food.coordinates[0] and y == self.food.coordinates[1]:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.canvas.delete("food")
            self.food = Food(self)
        else:
            del self.snake.coordinates[-1]
            self.canvas.delete(self.snake.squares[-1])
            del self.snake.squares[-1]
        
        if self.check_collisions():
            self.game_over()
        else:
            self.root.after(self.SPEED, self.next_turn)
    
    def change_direction(self, new_direction):
        if new_direction == 'left' and self.direction != 'right':
            self.direction = new_direction
        elif new_direction == 'right' and self.direction != 'left':
            self.direction = new_direction
        elif new_direction == 'up' and self.direction != 'down':
            self.direction = new_direction
        elif new_direction == 'down' and self.direction != 'up':
            self.direction = new_direction
    
    def check_collisions(self):
        x, y = self.snake.coordinates[0]
        
        if x < 0 or x >= self.GAME_WIDTH:
            return True
        elif y < 0 or y >= self.GAME_HEIGHT:
            return True
        
        for body_part in self.snake.coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                return True
        
        return False
    
    def game_over(self):
        self.game_running = False
        self.canvas.delete('all')
        self.canvas.create_text(
            self.GAME_WIDTH / 2,
            self.GAME_HEIGHT / 2,
            font=('consolas', 70),
            text="GAME OVER",
            fill="red",
            tag="gameover"
        )
        self.canvas.create_text(
            self.GAME_WIDTH / 2,
            self.GAME_HEIGHT / 2 + 80,
            font=('consolas', 30),
            text=f"Final Score: {self.score}",
            fill="white",
            tag="gameover"
        )


class Snake:
    
    def __init__(self, game):
        self.game = game
        self.body_size = game.BODY_PARTS
        self.coordinates = []
        self.squares = []
        
        for i in range(0, game.BODY_PARTS):
            self.coordinates.append([0, 0])
        
        for x, y in self.coordinates:
            square = game.canvas.create_rectangle(
                x, y, x + game.SPACE_SIZE, y + game.SPACE_SIZE,
                fill=game.SNAKE_COLOR, tag="snake"
            )
            self.squares.append(square)


class Food:
    def __init__(self, game):
        self.game = game   
        x = random.randint(0, (game.GAME_WIDTH / game.SPACE_SIZE) - 1) * game.SPACE_SIZE
        y = random.randint(0, (game.GAME_HEIGHT / game.SPACE_SIZE) - 1) * game.SPACE_SIZE
        
        self.coordinates = [x, y]
        
        game.canvas.create_oval(
            x, y, x + game.SPACE_SIZE, y + game.SPACE_SIZE,
            fill=game.FOOD_COLOR, tag="food"
        )


def main():
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
