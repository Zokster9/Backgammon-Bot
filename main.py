from random import randint
from board import Board, BoardDrawer
from dice import Dice, Die, DiceDrawer
from figures import Figures
from moves import Moves
import pprint


def get_ordinal_for_num(num):
    if num == 1:
        return 'first'
    elif num == 2:
        return 'second'
    elif num == 3:
        return 'third'
    elif num == 4:
        return 'fourth'


def figures_on_bar(game_board: Board, player_figure):
    if len(game_board.bar) == 0:
        return False
    try:
        game_board.bar.index(player_figure)
        return True
    except ValueError:
        return False


def player_enter_die_value(game_dice):
    while True:
        die = input('Enter the value of the die you want to play first: ')
        try:
            die = int(die)
            if die != game_dice.die1 and die != game_dice.die2:
                print(f'You must choose either a die with value {game_dice.die1} or {game_dice.die2}!')
                continue
            return die
        except ValueError:
            print('Value of the die must be a number!')
            continue


def player_enter_triangle_num(game_board, num='first'):
    while True:
        triangle = input(f'Enter the {num} triangle number from where you wish to move the checker: ')
        try:
            triangle = int(triangle)
            if not 1 <= triangle <= 24:
                print('Value of the triangle number must between 1-24!')
                continue
            if game_board.triangles[triangle - 1].count(Figures.white_figure()) == 0:
                print('You must choose a triangle with your own checkers')
                continue
            return triangle
        except ValueError:
            print('Value of the triangle number must be a number!')
            continue


def player_input(game_board: Board, game_dice: Dice, valid_moves: Moves):
    if figures_on_bar(game_board, Figures.white_figure()):
        print()
    else:
        if game_dice.die1 != game_dice.die2:
            die = player_enter_die_value(game_dice)
            triangle_1 = player_enter_triangle_num(game_board)
            if die == game_dice.die1:
                player_make_a_move(game_dice.die1, game_board, triangle_1, valid_moves)
            else:
                player_make_a_move(game_dice.die2, game_board, triangle_1, valid_moves)
            BoardDrawer.generate_table(game_board.triangles, game_board.bar)
            print()
            triangle_2 = player_enter_triangle_num(game_board, 'second')
            if die == game_dice.die1:
                player_make_a_move(game_dice.die2, game_board, triangle_2, valid_moves)
            else:
                player_make_a_move(game_dice.die1, game_board, triangle_2, valid_moves)
        else:
            num_of_moves = valid_moves.equal_die_valid_counter
            print(f"You will have {num_of_moves} moves to do with these dice!!")
            for i in range(0, num_of_moves):
                triangle = player_enter_triangle_num(game_board, get_ordinal_for_num(i + 1))
                player_make_a_move(game_dice.die1 + i, game_board, triangle, valid_moves)
                BoardDrawer.generate_table(game_board.triangles, game_board.bar)
                print()


def player_make_a_move(die, game_board, triangle, valid_moves):
    for moves in valid_moves.moves:
        move = moves.get(die, None)
        if move is not None:
            if move[0] == triangle - 1:
                move_checker(game_board, move)
                break


def move_checker(game_board, move):
    checker = game_board.triangles[move[0]].pop()
    if move[2]:
        bar_checker = game_board.triangles[move[1]].pop()
        game_board.bar.append(bar_checker)
    game_board.triangles[move[1]].append(checker)


def random_bot_makes_a_move(game_board: Board, valid_moves: Moves):
    move_idx = randint(0, len(valid_moves.moves) - 1)
    moves = valid_moves.moves[move_idx]
    for key, move in moves.items():
        if move[0] == 'bar':
            game_board.bar.remove(Figures.black_figure())
            if move[2]:
                bar_checker = game_board.triangles[move[1]].pop()
                game_board.bar.append(bar_checker)
            game_board.triangles[move[1]].append(Figures.black_figure())
        else:
            move_checker(game_board, move)


def get_player_figure(player_goes_next):
    if player_goes_next:
        return Figures.white_figure()
    return Figures.black_figure()


def game(game_board: Board, game_dice: Dice, player_goes_next):
    game_over = False
    while not game_over:
        BoardDrawer.generate_table(game_board.triangles, game_board.bar)
        DiceDrawer.draw_dice(game_dice.die1, game_dice.die2)
        moves = Moves()
        print()
        moves.generate_moves(game_board, game_dice, get_player_figure(player_goes_next))
        if len(moves.moves) > 0:
            if player_goes_next:
                player_input(game_board, game_dice, moves)
                player_goes_next = False
            else:
                random_bot_makes_a_move(game_board, moves)
                player_goes_next = True
        else:
            if player_goes_next:
                print('You have no valid moves. You must skip a turn!')
                player_goes_next = False
            else:
                print('Bot has no valid moves. Bot must skip a turn!')
                player_goes_next = True
        game_dice.roll_dice()


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
