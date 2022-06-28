from board import Board, BoardDrawer
from dice import Dice, Die, DiceDrawer
from figures import Figures


def figures_on_bar(game_board: Board, player_figure):
    if len(game_board.bar) == 0:
        return False
    for figure in game_board.bar:
        if figure == player_figure:
            return True
    return False


def player_input(game_board: Board, game_dice: Dice):
    if figures_on_bar(game_board, Figures.white_figure()):
        print()
    else:
        print()


def game(game_board: Board, game_dice: Dice, player_goes_next):
    game_over = False
    while not game_over:
        board_drawer = BoardDrawer(game_board.triangles, game_board.bar)
        board_drawer.generate_table()
        DiceDrawer.draw_dice(game_dice.die1, game_dice.die2)
        print()
        if player_goes_next:
            input('User')
        else:
            input('Bot')


if __name__ == '__main__':
    players_turn = False
    board = Board()
    dice = Dice(Die(), Die())
    print('Welcome to Backgammon! You will be playing against a very sophisticated bot ;)')
    print('Since you are new here you will be the white player! Roll the die so we can determine who goes first!')
    while True:
        input('Press Enter to roll the die...')
        dice.roll_dice()
        print('Your die:')
        print(DiceDrawer.draw_die(dice.die1))
        print('Bots die:')
        print(DiceDrawer.draw_die(dice.die2))
        if dice.die1 == dice.die2:
            print('It\'s a tie, so you have to roll again.')
        elif dice.die1 > dice.die2:
            print('Your die is greater so you start the game.')
            players_turn = True
            break
        elif dice.die1 < dice.die2:
            print('Bots die is greater so it starts the game.')
            break
    input('Press Enter to start the game...')
    print()
    game(board, dice, players_turn)
