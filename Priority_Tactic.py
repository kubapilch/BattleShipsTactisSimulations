from tactic import game_tactic

class PriorityTactic(game_tactic):

    def __init__(self):
        # Initialize the super class
        super().__init__(name='Priority tactic')

        # Create guessing board
        self.guessing_board = [[0]*10 for _ in range(10)]

    @property
    def highest_guess(self):
        highest = 0

        for row in self.guessing_board:
            # Check if current row highest point is higher that current highest if yes set new highest point
            highest = max(row) if max(row) > highest else highest

        return highest

    def take_shot(self, board):
        # Mark obvious cells as -1 to avoid shooting at them
        self.clear_obvious_points(board)

        while True:
            # Get the highest guessing score
            highest = self.highest_guess

            for y, row in enumerate(self.guessing_board):
                
                # Check if there is a highest value in this row
                if highest in row:
                    x = row.index(highest)

                    if board[y][x] == 0:
                        # Return cordinates
                        return (x, y)
                    else:
                        # This place has been shot already set as -1
                        self.guessing_board[y][x] = -1

    @game_tactic.last_shot.setter
    def last_shot(self, last):
        self.__last_shot = last

        self.guessing_board[last[1]][last[0]] = -2

        # Mark cross around as higher value

        # Left middle
        if last[0]-1 > 0 and self.guessing_board[last[1]][last[0]-1] >= 0:
            self.guessing_board[last[1]][last[0]-1] += 1

        # Top middle
        if last[1]-1 > 0 and self.guessing_board[last[1]-1][last[0]] >= 0:
            self.guessing_board[last[1]-1][last[0]] += 1

        # Bottom middle
        if last[1]+1 < len(last) and self.guessing_board[last[1]+1][last[0]] >= 0:
            self.guessing_board[last[1]+1][last[0]] += 1
        
        # Right middle
        if last[0]+1 < len(last) and self.guessing_board[last[1]][last[0]+1] >= 0:
            self.guessing_board[last[1]][last[0]+1] += 1
    
    def clear_obvious_points(self, board):
        for y, rows in enumerate(board):
            for x, cell in enumerate(rows):
                # Check if cell is sunk
                if cell == 4:
                    # Set sunk cell as -1
                    self.guessing_board[y][x] = -1

                    for row in range(-1, 2):
                        for column in range(-1, 2):
                            
                            # Check if index out of range
                            if y + row < 0 or y + row >= len(self.guessing_board):
                                continue

                            if x + column < 0 or x + column >= len(self.guessing_board):
                                continue

                            self.guessing_board[y+row][x+column] = -1
