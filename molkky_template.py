"""
COMP.CS.100 Ohjelmointi 1 / Programming 1

Code template for Mölkky.
"""


class Player:
    """
    Class Player: Implements a player that play the game molkky.
    The class defines what a player is.
    what information it contains and what operations can be
    carried out for it.
    """

    def __init__(self, name):
        """
        Constructor, initializes the newly created object.
        :param name: str, name of player
        """

        self.__name = name
        self.__points = 0
        self.__won = False
        self.__turn = 0
        self.__fail_score = 0
        self.__percentage = 0.0
        self.__penalty = False

    def print_information(self):
        """
        print out how many liter left in the tank
        and how many km does the car travel
        """
        print(f"The tank contains {self.__gas:.1f} liters of gas and the odometer shows {self.__odometer:.1f} kilometers.")

    def get_name(self):
        """
        Get the name of player.
        """
        return self.__name

    def get_points(self):
        """
        Get how many points player have.
        """
        return self.__points

    def has_won(self):
        """
        check if the player win the game
        """
        if self.__points == 50:
            self.__won = True
        return self.__won
    
    def get_turn(self):
        """
        Get how many turn player has been played
        """
        return float(self.__turn)
    
    def get_percentage(self):
        """
        Get how percen player got points
        """
        return ("{:.1f}".format(self.__percentage))
    
    def update_percentage(self):
        """
        update how percentage player have after a turn
        """
        if self.__fail_score == 0 and self.__turn != 0:
            self.__percentage = 100.0
        elif self.__fail_score == self.__turn:
            self.__percentage = 0.0
        else:
            self.__percentage = 100*(self.__turn - self.__fail_score)/self.__turn

    def is_penaltied(self):
        """
        check penalty
        """
        return self.__penalty

    def add_points(self, point):
        """
        Adding points for player
        :param point: int, how many point player gain
        """
        self.__penalty = False
        self.__turn += 1
        if point == 0:
            self.__fail_score += 1
        self.update_percentage()

        self.__points += point
        if self.__points > 50:
            print(f"{self.__name} gets penalty points!")
            self.__penalty = True
            self.__points = 25
        elif 40 <= self.__points <= 49:
            left = 50 - self.__points
            print(f"{self.__name} needs only {left} points. It's better to avoid knocking down the pins with higher points.")
        


def main():
    # Here we define two variables which are the objects initiated from the
    # class Player. This is how the constructor of the class Player
    # (the method that is named __init__) is called!

    player1 = Player("Matti")
    player2 = Player("Teppo")

    throw = 1
    while True:

        # if throw is an even number
        if throw % 2 == 0:
            in_turn = player1

        # else throw is an odd number
        else:
            in_turn = player2

        pts = int(input("Enter the score of player " + in_turn.get_name() +
                        " of throw " + str(throw) + ": "))

        in_turn.add_points(pts)

        # TODO:
        # c) Add a supporting feedback printout "Cheers NAME!" here.
        average = in_turn.get_points()/in_turn.get_turn()
        if pts > average and average > 0.0 and not in_turn.is_penaltied():
            print(f"Cheers {in_turn.get_name()}!")


        if in_turn.has_won():
            print("Game over! The winner is " + in_turn.get_name() + "!")
            return

        print("")
        print("Scoreboard after throw " + str(throw) + ":")
        print(player1.get_name() + ":", player1.get_points(), "p, hit percentage", player1.get_percentage())  # TODO: d)
        print(player2.get_name() + ":", player2.get_points(), "p, hit percentage", player2.get_percentage())  # TODO: d)
        print("")

        throw += 1


if __name__ == "__main__":
    main()
