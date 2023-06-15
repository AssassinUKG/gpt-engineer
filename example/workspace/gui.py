import tkinter as tk
from tkinter import messagebox

class GUI:
    def __init__(self, game):
        self.game = game
        self.window = tk.Tk()
        self.window.title("Naughts and Crosses")
        self.window.resizable(False, False)
        self.board_buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_widgets()

    def create_widgets(self):
        self.board_frame = tk.Frame(self.window)
        self.board_frame.pack(padx=10, pady=10)
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.board_frame, text="", font=("Arial", 24), width=2, height=1,
                                   command=lambda row=i, col=j: self.on_board_button_click(row, col))
                button.grid(row=i, column=j, padx=5, pady=5)
                self.board_buttons[i][j] = button

        self.status_label = tk.Label(self.window, text="Player 1's turn", font=("Arial", 16))
        self.status_label.pack(pady=10)

        self.reset_button = tk.Button(self.window, text="Reset", font=("Arial", 16), command=self.on_reset_button_click)
        self.reset_button.pack(pady=10)

    def run(self):
        self.window.mainloop()

    def on_board_button_click(self, row, col):
        winner = self.game.make_move(row, col)
        if winner:
            self.show_winner_message(winner)
        else:
            self.update_board()

    def on_reset_button_click(self):
        self.game.reset()
        self.update_board()

    def update_board(self):
        for i in range(3):
            for j in range(3):
                self.board_buttons[i][j].configure(text=self.game.board.grid[i][j])
        self.status_label.configure(text=f"{self.game.current_player.name}'s turn")

    def show_winner_message(self, winner):
        if winner == "Tie":
            messagebox.showinfo("Game Over", "It's a tie!")
        else:
            messagebox.showinfo("Game Over", f"{winner.name} wins!")
        self.game.reset()
        self.update_board()
