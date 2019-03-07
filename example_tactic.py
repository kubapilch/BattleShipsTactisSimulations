from tactic import game_tactic

class example_tactic(game_tactic):

    def __init__(self):
        # Call game tactic init and pass your tactic name as an argument
        super().__init__(name='My Tactic Name')

        # Do all initial setup here, you can specify your own variables but avoid names:
        # self.name
        # self.__last_shot

        # Also you can't create your own functions with names:
        # def take_shot
        # def last_shot

        # Your code goes here:

    
    def take_shot(self, board):
        """
        Override this method to determine where to shot, it has to return tuple with X and Y cordinates
        ex. (X, Y), remember that the first X and Y cordinate is 0 and the last is len(board)-1
        
        Checking if the place that you have picked have been shot already is a good practice even though
        the game will check it for you and ask for another one, make sure that this won't 
        go into infinite loop.

        Board is a list of list, you can acces each cell like: board[y_cord][x_cord].

        Cells number mining:
        0 - Haven't been shot yet
        2 - Shot and missed
        3 - Shot and Hit
        4 - Sunk ship

        1 is used as ab ship inside game class board, board passed as an argument to take_shot method won't have marked ships as 1,
        instead this cell will be 0
        """


        return (0, 0)
    
    # This line can be marked as error in your editor(it is in mine, VS Code but ignore it)
    @game_tactic.last_shot.setter
    def last_shot(self, last):
        """
        Override this to get feedback about your last shot, given argument is a tuple with four variables,
        (X_cord, Y_cord, Bool_if_hit, Bool_if_sunk)
        """
        # Remember to first call super class method
        super().last_shot(last)

        # Your code goes here:
