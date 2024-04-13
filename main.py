import random
import tkinter as tk
from tkinter import simpledialog, messagebox

class PuzzleGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.configure(bg='#00282f')
        self.root.title("Sliding Puzzle Game")
        self.canvas = tk.Canvas(self.root, bg="#00282f", highlightbackground="#77B0AA")
        self.canvas.pack()
        self.rows = 0
        self.cols = 0
        self.board = []
        self.empty_pos = ()
        self.tile_width = 0
        self.tile_height = 0
        self.tiles = {}
        self.moves = 0
        self.invert_wasd = tk.BooleanVar()
        
        self.new_game_button = tk.Button(self.root, text="New Game", command=self.ask_dimensions, fg="#E3FEF7", bg="#135D66")
        self.new_game_button.pack(side=tk.LEFT, padx=10, pady=2)

        self.invert_checkbox = tk.Checkbutton(self.root, text="Invert WASD", variable=self.invert_wasd, fg="#E3FEF7", bg="#00282f", selectcolor="#00282f", activeforeground="#E3FEF7", activebackground="#00282f")
        self.invert_checkbox.pack(side=tk.LEFT, padx=10, pady=2)

        self.moves_label = tk.Label(self.root, text="Moves: 0", fg="#E3FEF7", bg="#135D66")
        self.moves_label.pack(side=tk.RIGHT, padx=10, pady=2)

    def ask_dimensions(self):
        self.rows = simpledialog.askinteger("Input", "Enter number of rows:", parent=self.root, minvalue=2)
        self.cols = simpledialog.askinteger("Input", "Enter number of columns:", parent=self.root, minvalue=2)
        if self.rows is not None and self.cols is not None:
            self.initialize_board()
            self.play()

    def initialize_board(self):
        self.canvas.config(width=self.cols * 50, height=self.rows * 50)
        self.board = [[i + j * self.cols + 1 for i in range(self.cols)] for j in range(self.rows)]
        self.board[self.rows - 1][self.cols - 1] = None
        self.empty_pos = (self.rows - 1, self.cols - 1)
        self.tile_width = 50
        self.tile_height = 50

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(self.rows):
            for col in range(self.cols):
                x0 = col * self.tile_width
                y0 = row * self.tile_height
                x1 = x0 + self.tile_width
                y1 = y0 + self.tile_height
                number = self.board[row][col]
                if number is not None:
                    self.tiles[number] = self.canvas.create_rectangle(x0, y0, x1, y1, fill="#135D66", outline="#77B0AA")
                    self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=str(number), font=("Times New Roman", 10), fill="#E3FEF7")
                else:
                    self.tiles[number] = self.canvas.create_rectangle(x0, y0, x1, y1, fill="#77B0AA", outline="#77B0AA")

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

    def on_key_press(self, event):
        if self.invert_wasd.get():
            if event.char.lower() == "w":
                self.move(self.empty_pos[0] - 1, self.empty_pos[1])
            elif event.char.lower() == "s":
                self.move(self.empty_pos[0] + 1, self.empty_pos[1]) 
            elif event.char.lower() == "a":
                self.move(self.empty_pos[0], self.empty_pos[1] - 1)
            elif event.char.lower() == "d":
                self.move(self.empty_pos[0], self.empty_pos[1] + 1)
        else:
            if event.char.lower() == "w":
                self.move(self.empty_pos[0] + 1, self.empty_pos[1])
            elif event.char.lower() == "s":
                self.move(self.empty_pos[0] - 1, self.empty_pos[1]) 
            elif event.char.lower() == "a":
                self.move(self.empty_pos[0], self.empty_pos[1] + 1)
            elif event.char.lower() == "d":
                self.move(self.empty_pos[0], self.empty_pos[1] - 1)
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
        self.initialize_board()
        self.shuffle_board()

    def update_moves_label(self):
        self.moves_label.config(text="Moves: {}".format(self.moves))

    def play(self):
        self.shuffle_board()
        self.canvas.bind("<Button-1>", self.on_click)
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.mainloop()

if __name__ == "__main__":
    game = PuzzleGame()
    game.ask_dimensions()
