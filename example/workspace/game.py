from player import Player
from board import Board

class Game:
    def __init__(self):
        self.players = [Player("Player 1", "X"), Player("Player 2", "O")]
        self.board = Board()
        self.current_player = self.players[0]

    def start(self):
        self.board.clear()
        self.current_player = self.players[0]

    def make_move(self, row, col):
        self.board.update(row, col, self.current_player.symbol)
        winner = self.check_winner()
        if winner:
            return winner
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]
        return None

    def check_winner(self):
        for i in range(3):
            if self.board.grid[i][0] == self.board.grid[i][1] == self.board.grid[i][2] != " ":
                return self.current_player
            if self.board.grid[0][i] == self.board.grid[1][i] == self.board.grid[2][i] != " ":
                return self.current_player
        if self.board.grid[0][0] == self.board.grid[1][1] == self.board.grid[2][2] != " ":
            return self.current_player
        if self.board.grid[0][2] == self.board.grid[1][1] == self.board.grid[2][0] != " ":
            return self.current_player
        if self.board.is_full():
            return "Tie"
        return None

    def reset(self):
        self.board.clear()
        self.current_player = self.players[0]
