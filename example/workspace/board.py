class Board:
    def __init__(self):
        self.grid = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]

    def clear(self):
        self.grid = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]

    def display(self):
        print("   0 1 2")
        for i in range(3):
            print(f"{i}  {self.grid[i][0]}|{self.grid[i][1]}|{self.grid[i][2]}")
            if i < 2:
                print("   -+-+-")

    def update(self, row, col, symbol):
        self.grid[row][col] = symbol

    def is_full(self):
        for row in self.grid:
            if " " in row:
                return False
        return True
