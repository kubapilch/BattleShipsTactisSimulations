# WarShips game tactic simulation

If you have ever wanted to write a warship game tactic, test yourself by writing the most efficient one or you want to write an AI for your game that will play with a user, now you can. Test efficiency of your tactic with my script!

# Installation
All you need to do is download all files from github.

# Usage
To run my script all you have to do is run `ships.py` file or import it into another file.
`from ships import ShipsGame`, then create gmae object `ShipGame()` and call play method `ShipGame().play()`. 

You can pass optional arguments:
* Tactic that you want to play with, default tactic is Random Tactic that randomly chooses cells, but I have also implemented a tactic that try to guess where to shoot. You can change tactic by passing the class name like `ShipGame(tactic=PriorityTactic)`. **Note: You have to pass only the name of the class without brackets**
* Number of games you want to simulate (recommended as much as possible when testing your tactic for better accuracy) ex. `ShipGame(number_of_games=1000)`
* Ships that you want to play with, you have to pass it as a list ex. `ShipGame(ships_lenght=[4, 4, 4, 3, 1, 1])`. The game will have three  four cells ships, one with three cells and two one cell ships.
* If you want to display currently playing game number, it is set as `True` by default because it is good for debugging. You can always change it by passing `ShipGame(display_game_nr=False)` 

# Example usage
```
from Ships import ShipGame
from Priority_Tactic import PriorityTactic

game = ShipGame(tactic=PriorityTactic, number_of_games=100)
game.play()
```
# Implementing your own tactic
To implement your own tactic you have to create a subclass of `game_tactic` and then override a couple of methods. You can see a model in `example_tactic.py`. 

Methods that you have to override:
* `def __init__(self)` you can do all setup here, one thing to remember is to write `super().__init__(name='Your Tactic Name')` at the begining of this method.
* `def take_shot(self, board)` the main method of your tactic, it will be called every turn to pick another target. It has to return a tuple with coordinates (X, Y). Be aware that boards in my game are accessed like `board[Y_coord][X_coord]`. What it means is that board is a list of list and each list is a row so to access certain cell you have to get the row first and later the column. Each cell in board game can be an integer from 0-4 excluding 1
    * 0 - Undiscovered cell
    * 2 - Shot and missed
    * 3 - Shot and hit
    * 4 - Shot and the entire ship is sunk

    **It is a good practice to check every time you pick a target if it has been shot already. The game will do it for you and call `take_shot` again, but it is very likely it will go into an infinite loop.**
* ```
    @game_tactic.last_shot.setter
    def last_shot(self, last)
    ```
    This property is set after every shot with a feedback about it. `last` is a tuple with coordinates, bool if hit and bool if sunk, (X, Y, hit, sunk). You can use it to create guessing boards etc.
    Remember to call `super().last_shot = last` at the beginning of this method. Avoid using `self.__last_shot` as a variable name because it is used inside `game_tactic`.

