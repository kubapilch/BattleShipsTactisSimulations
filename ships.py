from tactic import game_tactic
from random import choice
from pprint import pprint

class ShipsGame():
    def __init__(self, tactic:game_tactic, number_of_games=1):
        self.tactic = tactic
        self.number_of_games = number_of_games
        self.ships = []

    def place_ships(self, board, ships_lenght=[4, 3, 3, 2, 2, 2, 1, 1, 1, 1,]):
        self.ships = []

        # TODO: refactor this massive if statement, maybe
        # for i in range(-1, 1):
        #   for y in range(-1, 1):
        for ship_lenght in sorted(ships_lenght, reverse=True):
            # Find place for this ship
            while True:
                alingment = choice(['v', 'h'])

                y = choice(range(len(board)))
                x = choice(range(len(board[y])))

                if not board[y][x] == 1:
                    # Place horizontaly
                    if alingment == 'h':
                        # Check if will be out of bounds if palced here
                        if x + ship_lenght <= len(board[0]):
                            for cell_x in range(x, x+ship_lenght):
                                # Middle
                                if board[y][cell_x]:
                                    # Break the inner-loop, try again
                                    break

                                # Right middle
                                if not cell_x+1 >= len(board[y]) and board[y][cell_x+1]:
                                    # Break the inner-loop, try again
                                    break

                                # Top right
                                if not (cell_x+1 >= len(board[y]) or y-1 < 0) and board[y-1][cell_x+1]:
                                    # Break the inner-loop, try again
                                    break
                                
                                # Bottom right
                                if not (cell_x+1 >= len(board[y]) or y+1 >= len(board)) and board[y+1][cell_x+1]:
                                    # Break the inner-loop, try again
                                    break

                                # Bottom middle
                                if not y+1 >= len(board) and board[y+1][cell_x]:
                                    # Break the inner-loop, try again
                                    break
                                
                                # Top middle
                                if not y-1 < 0 and board[y-1][cell_x]:
                                    # Break the inner-loop, try again
                                    break
                                
                                # Left top
                                if not (y-1 < 0 or cell_x - 1 < 0) and board[y-1][cell_x-1]:
                                    # Break the inner-loop, try again
                                    break
                                
                                # Left middle
                                if not cell_x - 1 < 0 and board[y][cell_x-1]:
                                    # Break the inner-loop, try again
                                    break

                                # Left bottom
                                if not (y+1 >= len(board) or cell_x - 1 < 0) and board[y+1][cell_x-1]:
                                    # Break the inner-loop, try again
                                    break

                            else:
                                # Break main loop, place found
                                break

                    # Place vericaly
                    if alingment == 'v':
                        # Check if will be out of bounds if placed here
                        if y + ship_lenght <= len(board):
                            for cell_y in range(y, y+ship_lenght):
                                # Middle
                                if board[cell_y][x]:
                                    # Break the inner-loop, try again
                                    break

                                # Right middle
                                if not x+1 >= len(board[y]) and board[cell_y][x+1]:
                                    # Break the inner-loop, try again
                                    break

                                # Top right
                                if not (cell_y-1 < 0 or x+1 >= len(board[y])) and board[cell_y-1][x+1]:
                                    # Break the inner-loop, try again
                                    break
                                
                                # Bottom right
                                if (not (cell_y+1 >= len(board) or x+1 >= len(board[y]))) and board[cell_y+1][x+1]:
                                    # Break the inner-loop, try again
                                    break

                                # Bottom middle
                                if not cell_y+1 >= len(board) and board[cell_y+1][x]:
                                    # Break the inner-loop, try again
                                    break
                                
                                # Top middle
                                if not cell_y-1 < 0 and board[cell_y-1][x]:
                                    # Break the inner-loop, try again
                                    break
                                
                                # Left top
                                if not (cell_y-1 < 0 or x - 1 < 0) and board[cell_y-1][x-1]:
                                    # Break the inner-loop, try again
                                    break
                                
                                # Left middle
                                if not x - 1 < 0 and board[cell_y][x-1]:
                                    # Break the inner-loop, try again
                                    break

                                # Left bottom
                                if not (cell_y+1 >= len(board) or x - 1 < 0) and board[cell_y+1][x-1]:
                                    # Break the inner-loop, try again
                                    break
                            else:
                                # Break main loop, place found
                                break

            cordinates = []

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
        for row in board:
            if 1 in row:
                return True
        pprint(board)
        return False        

    @staticmethod
    def create_board(size=10):
        board = [[0]*size for _ in range(size)]
        return board

    def play(self):
        # Make variable to count number of shots
        total_number_of_shots = 0

        # Play specified number of games
        for game_number in range(1, self.number_of_games+1):

            print(f'Now playing game nr {game_number}')

            # Create board and place ships
            board = self.create_board()
            board = self.place_ships(board)

            # Load game tactic
            this_game_tactic = self.tactic

            # Create board that will contain only shots to pass to tactic
            tactic_board = [[0]*len(board) for _ in range(len(board))]
            
            # Number of shots in this game
            number_of_shots = 0

            # Play the game until all ships are sunk
            while self.check_if_ships_left(board):
                
                # Make sure that tactic didn't choose place that has been shot
                while True:
                    x, y = this_game_tactic.take_shot(tactic_board)

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

        print(f"Simulations for {self.tactic.name} ended, number of shots required to win: {total_number_of_shots/self.number_of_games}")

class ship():
    def __init__(self, lenght, cordinates):
        self.cordinates = cordinates
        self.lenght = lenght
        self.sunk = False
        self.sunk_cells = 0

    def mark_hit(self):
        self.sunk_cells += 1
        if self.sunk_cells == self.lenght:
            self.sunk = True

        return self.sunk
    
    def check_if_hit(self, x, y):
        for cell in self.cordinates:
            if cell == (x, y):
                return True

        return False

ShipsGame(tactic=game_tactic(name='Random Tactic'), number_of_games=100).play()