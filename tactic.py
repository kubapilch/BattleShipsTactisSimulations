from random import choice

class game_tactic():

    def __init__(self, name):
        self.name = name
        self.__last_shot:tuple

    def take_shot(self, board) -> tuple:
        """
        This function needs to be override to create new game tactic, function has to take one argument (board) and return a tuple
        of cordinates.
        """
        while True:
            # Pick random cordinates
            x = choice(range(10))
            y = choice(range(10))

            # Check if this cell has been shot before
            if board[y][x] == 0:
                break

        return (x, y)

    @property
    def last_shot(self):
        return self.__last_shot
    
    @last_shot.setter
    def last_shot(self, last):
        """
        Override to get feedback after every shot, last is a tuple that contains x cord, y cord, 
        bool that is True if a ship was hit and bool if the ship was sunk [x, y, bool, bool]
        """
        self.__last_shot = last

