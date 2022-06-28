from random import randint
from colorama import init, Fore, Back, Style

init(autoreset=True)


class Die:
    def __init__(self):
        self._value = randint(1, 6)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def roll_die(self):
        self._value = randint(1, 6)

    def __str__(self):
        return str(self._value)


class Dice:
    def __init__(self, die1: Die, die2: Die):
        self._die1 = die1
        self._die2 = die2

    def roll_dice(self, first_turn=False):
        if first_turn:
            return
        self._die1.roll_die()
        self._die2.roll_die()

    def roll_die1(self):
        self._die1.roll_die()

    def roll_die2(self):
        self._die2.roll_die()

    @property
    def die1(self):
        return self._die1.value

    @property
    def die2(self):
        return self._die2.value

    @die1.setter
    def die1(self, value):
        self._die1.value = value

    @die2.setter
    def die2(self, value):
        self._die2.value = value


class DiceDrawer:
    def __init__(self, die1_value, die2_value):
        self._die1_value = die1_value
        self._die2_value = die2_value

    def draw_dice(self):
        print('Dice:')
        print(DiceDrawer.draw_die(self._die1_value))
        print()
        print(DiceDrawer.draw_die(self._die2_value))

    @staticmethod
    def draw_die(value):
        style = Style.BRIGHT + Back.WHITE + Fore.BLACK
        reset = Style.RESET_ALL
        if value == 1:
            return style + "   " + reset + "\n" + style + " o " + reset + "\n" + style + "   " + reset
        elif value == 2:
            return style + "o  " + reset + "\n" + style + "   " + reset + "\n" + style + "  o" + reset
        elif value == 3:
            return style + "o  " + reset + "\n" + style + " o " + reset + "\n" + style + "  o" + reset
        elif value == 4:
            return style + "o o" + reset + "\n" + style + "   " + reset + "\n" + style + "o o" + reset
        elif value == 5:
            return style + "o o" + reset + "\n" + style + " o " + reset + "\n" + style + "o o" + reset
        elif value == 6:
            return style + "o o" + reset + "\n" + style + "o o" + reset + "\n" + style + "o o" + reset
