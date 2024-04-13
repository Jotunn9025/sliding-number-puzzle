import random
import tkinter as tk
from tkinter import messagebox

class PuzzleGame:
    def __init__(self, rows, cols):
        self.root = tk.Tk()
        self.root.title(f"{rows}x{cols} Sliding Puzzle Game")
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()
        self.rows = rows
        self.cols = cols
        self.board = [[i + j * cols + 1 for i in range(cols)] for j in range(rows)]
        self.board[rows - 1][cols - 1] = None
        self.empty_pos = (rows - 1, cols - 1)
        self.tile_width = 50
        self.tile_height = 50
        self.tiles = {}
        self.moves = 0

        self.new_game_button = tk.Button(self.root, text="New Game", command=self.new_game)
        self.new_game_button.pack(side=tk.RIGHT)

        self.moves_label = tk.Label(self.root, text="Moves: 0")
        self.moves_label.pack(side=tk.RIGHT)

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(self.rows):
            for col in range(self.cols):
                x0 = col * self.tile_width
                y0 = row * self.tile_height
                x1 = x0 + self.tile_width
                y1 = y0 + self.tile_height
                number = self.board[row][col]
                self.tiles[number] = self.canvas.create_rectangle(x0, y0, x1, y1, fill="#135D66", outline="#77B0AA")
                if number is not None:
                    self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=str(number), font=("Times New Roman", 10), fill="#E3FEF7")

    def is_valid_move(self, row, col):
        r, c = self.empty_pos
        return (row == r and abs(col - c) == 1) or (col == c and abs(row - r) == 1)

    def move(self, row, col):
        if self.is_valid_move(row, col):
            self.board[self.empty_pos[0]][self.empty_pos[1]] = self.board[row][col]
            self.board[row][col] = None
            self.empty_pos = (row, col)
            self.moves += 1
            self.update_moves_label()
            return True
        return False

    def shuffle_board(self):
        for _ in range(1000):
            moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            row, col = self.empty_pos
            dx, dy = random.choice(moves)
            new_row, new_col = row + dx, col + dy
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                self.move(new_row, new_col)
        self.draw_board()
        self.moves = 0
        self.update_moves_label()

    def on_click(self, event):
        col = event.x // self.tile_width
        row = event.y // self.tile_height
        if self.move(row, col):
            self.draw_board()
            if self.check_win():
                self.show_win_message()

    def check_win(self):
        current_value = 0
        for row in self.board:
            for col in row:
                if col is not None:
                    if col != current_value + 1:
                        return False
                    current_value = col
        return True

    def show_win_message(self):
        messagebox.showinfo("Congratulations!", "You have solved the puzzle in {} moves.".format(self.moves))
        self.new_game()

    def new_game(self):
        self.board = [[i + j * self.cols + 1 for i in range(self.cols)] for j in range(self.rows)]
        self.board[self.rows - 1][self.cols - 1] = None
        self.empty_pos = (self.rows - 1, self.cols - 1)
        self.shuffle_board()

    def update_moves_label(self):
        self.moves_label.config(text="Moves: {}".format(self.moves))

    def play(self):
        self.shuffle_board()
        self.canvas.bind("<Button-1>", self.on_click)
        self.root.mainloop()

if __name__ == "__main__":
    game = PuzzleGame(6, 6)
    game.play()
