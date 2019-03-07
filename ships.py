from tactic import game_tactic
from random import choice

class ShipsGame():
    def __init__(self, tactic:game_tactic, number_of_games=1, ships_lenght=[4, 3, 3, 2, 2, 2, 1, 1, 1, 1], display_game_nr=True):
        self.tactic = tactic
        self.number_of_games = number_of_games
        self.ships = []
        self.ships_lenght = ships_lenght
        self.display_game_nr = display_game_nr

    def place_ships(self, board):
        """
        Place ships on board and return
        """
        self.ships = []

        for ship_lenght in sorted(self.ships_lenght, reverse=True):
            
            # Find place for this ship
            while True:
                
                alingment = choice(['v', 'h'])

                y = choice(range(len(board)))
                x = choice(range(len(board[y])))
                
                taken = False

                if not board[y][x] == 1:
                    
                    # Place horizontaly
                    if alingment == 'h':
                        
                        # Check if will be out of bounds if palced here
                        if x + ship_lenght <= len(board[0]):
                            
                            for cell_x in range(x, x+ship_lenght):
                                
                                for row in range(-1, 2):
                                    for col in range(-1, 2):
                                        
                                        # Check if index out of range
                                        if y + row < 0 or y + row >= len(board):
                                            continue
                                        
                                        if cell_x + col < 0 or cell_x + col >= len(board):
                                            continue
                                        
                                        if board[y + row][cell_x + col] == 1:
                                            taken = True
                                else:
                                    if taken:
                                        # Place is taken, break cell_x loop to avoid running else:
                                        # Look for another spot
                                        break
                            else:
                                # Place found break while loop
                                break

                    # Place vericaly
                    if alingment == 'v':
                        
                        # Check if will be out of bounds if placed here
                        if y + ship_lenght <= len(board):
                            
                            # Iterate by all cells in ship
                            for cell_y in range(y, y+ship_lenght):
                                
                                for row in range(-1, 2):
                                    for col in range(-1, 2):
                                        
                                        # Check if index out of range
                                        if cell_y + row < 0 or cell_y + row >= len(board):
                                            continue
                                        
                                        if x + col < 0 or x + col >= len(board):
                                            continue
                                        
                                        if board[cell_y + row][x + col]:
                                            taken = True
                                else:
                                   if taken:
                                        # Place is taken, break cell_y loop to avoid running else:
                                        # Look for another spot
                                        break
                            else:
                                # Place found break while loop
                                break

            cordinates = []

            # Create ship object with given cordinates and add it to self.ships
            for cord in range(ship_lenght):
                if alingment == 'h':
                    board[y][x+cord] = 1
                    cordinates.append((x+cord, y))
                else:
                    board[y+cord][x] = 1
                    cordinates.append((x, y+cord))

            self.ships.append(ship(ship_lenght, cordinates))

        return board

    @staticmethod
    def check_if_ships_left(board):
        """
        Check if there are alive ships on a board
        """
        for row in board:
            if 1 in row:
                return True

        return False        

    @staticmethod
    def create_board(size=10):
        board = [[0]*size for _ in range(size)]
        return board

    def play(self):
        """
        Main game function
        """
        # Make variable to count number of shots
        total_number_of_shots = 0

        # Play specified number of games
        for game_number in range(1, self.number_of_games+1):

            if self.display_game_nr:
                print(f'Now playing game nr {game_number}')

            # Create board and place ships
            board = self.create_board()
            board = self.place_ships(board)

            # Load game tactic
            this_game_tactic = self.tactic()

            # Create board that will contain only shots to pass to tactic
            tactic_board = [[0]*len(board) for _ in range(len(board))]
            
            # Number of shots in this game
            number_of_shots = 0

            # Play the game until all ships are sunk
            while self.check_if_ships_left(board):
                
                # Make sure that tactic didn't choose place that has been shot
                while True:
                    x, y = this_game_tactic.take_shot(board=tactic_board)

                    shot = [x, y, False, False]

                    if board[y][x] < 2:
                        break

                # Check if there is a ship
                if board[y][x] == 1:
                    # Mark a hit on both boards (3) and in shot variavble that will be set as last_shot
                    #  in a tactic variable ge give feedback
                    board[y][x] = 3
                    tactic_board[y][x] = 3
                    shot[2] = True

                    # Find exact ship that has been hit
                    for ship in self.ships:
                        
                        if ship.check_if_hit(x, y):
                            
                            # Mark a hit in ship class and check if ship sunk
                            if ship.mark_hit():
                                # Mark sunk in last_shot variable
                                shot[3] = True
                                
                                # Mark all ship cells in both boards as sunk (4)
                                for cell in ship.cordinates:
                                    board[cell[1]][cell[0]] = 4
                                    tactic_board[cell[1]][cell[0]] = 4

                else:
                    # Mark missed shot on both boards (2)
                    board[y][x] = 2
                    tactic_board[y][x] = 2
                
                # Add shot
                number_of_shots += 1
                
                # Give feedback to tactic class about the shot
                this_game_tactic.last_shot = tuple(shot)
            
            # Sum up shots
            total_number_of_shots += number_of_shots

        print(f"Simulations for {this_game_tactic.name} ended, average number of shots required to win: {total_number_of_shots/self.number_of_games}")

class ship():
    def __init__(self, lenght, cordinates):
        self.cordinates = cordinates
        self.lenght = lenght
        self.sunk = False
        self.sunk_cells = 0

    def mark_hit(self):
        """
        Set cell as hit and check if ship is sunk, returns bool
        """
        self.sunk_cells += 1

        if self.sunk_cells == self.lenght:
            self.sunk = True

        return self.sunk
    
    def check_if_hit(self, x, y):
        """
        Checks if given cordinates refers to a ship, returns bool
        """
        for cell in self.cordinates:
            if cell == (x, y):
                return True

        return False
