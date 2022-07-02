from random import randint
from timeit import default_timer as timer

from board import Board, BoardDrawer
from dice import Dice, Die, DiceDrawer
from expectiminimax import expectiminimax
from figures import Figures
from moves import Moves


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


def player_enter_die_value(game_dice, game_board):
    if figures_on_bar(game_board, Figures.white_figure()):
        while True:
            die = input('Enter the value of the die with which you want to enter from the bar: ')
            try:
                die = int(die)
                if die != game_dice.die1 and die != game_dice.die2:
                    print(f'You must choose either a die with value {game_dice.die1} or {game_dice.die2}!')
                    continue
                else:
                    triangle = 24 - die
                    if game_board.triangles[triangle].count(Figures.black_figure()) > 1:
                        print('You must choose a die with which you wont land on more than 1 opponent checker!')
                        continue
                return die
            except ValueError:
                print('Value of the die must be a number!')
                continue
    else:
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


def both_die_valid_input(game_board, game_dice, valid_moves, made_moves, num_made_moves):
    while True:
        if figures_on_bar(game_board, Figures.white_figure()):
            die = player_enter_die_value(game_dice, game_board)
            if die == game_dice.die1:
                player_make_a_move(game_dice.die1, game_board, 24 - die, valid_moves, made_moves)
            else:
                player_make_a_move(game_dice.die2, game_board, 24 - die, valid_moves, made_moves)
            if len(made_moves) == num_made_moves:
                print('Invalid move! Try again')
            else:
                break
        else:
            die = player_enter_die_value(game_dice, game_board)
            triangle_1 = player_enter_triangle_num(game_board)
            if die == game_dice.die1:
                player_make_a_move(game_dice.die1, game_board, triangle_1, valid_moves, made_moves)
            else:
                player_make_a_move(game_dice.die2, game_board, triangle_1, valid_moves, made_moves)
            if len(made_moves) == num_made_moves:
                print('Invalid move! Try again')
            else:
                break
    num_made_moves = len(made_moves)
    BoardDrawer.generate_table(game_board.triangles, game_board.bar)
    print()
    while True:
        if figures_on_bar(game_board, Figures.white_figure()):
            input(f'You can only enter the checker to triangle {25 - game_dice.die2}')
            if die == game_dice.die1:
                player_make_a_move(game_dice.die2, game_board, 24 - game_dice.die2, valid_moves, made_moves)
            else:
                player_make_a_move(game_dice.die1, game_board, 24 - game_dice.die2, valid_moves, made_moves)
            if len(made_moves) == num_made_moves:
                print('Invalid move! Try again')
            else:
                break
        else:
            triangle_2 = player_enter_triangle_num(game_board, 'second')
            if die == game_dice.die1:
                player_make_a_move(game_dice.die2, game_board, triangle_2, valid_moves, made_moves)
            else:
                player_make_a_move(game_dice.die1, game_board, triangle_2, valid_moves, made_moves)
            if len(made_moves) == num_made_moves:
                print('Invalid move! Try again')
            else:
                break


def one_die_input(game_board, die, valid_moves, made_moves, num_made_moves):
    print(f'You can only play the die with the value of {die}.')
    while True:
        if figures_on_bar(game_board, Figures.white_figure()):
            input(f'You can only enter the checker to triangle {25 - die}')
            player_make_a_move(die, game_board, 24 - die, valid_moves, made_moves)
            if len(made_moves) == num_made_moves:
                print('Invalid move! Try again')
            else:
                break
        else:
            triangle = player_enter_triangle_num(game_board)
            player_make_a_move(die, game_board, triangle, valid_moves, made_moves)
            if len(made_moves) == num_made_moves:
                print('Invalid move! Try again')
            else:
                break
    BoardDrawer.generate_table(game_board.triangles, game_board.bar)
    print()


def player_input(game_board: Board, game_dice: Dice, valid_moves: Moves):
    made_moves = list()
    num_made_moves = 0
    if game_dice.die1 != game_dice.die2:
        if valid_moves.both_die_valid:
            both_die_valid_input(game_board, game_dice, valid_moves, made_moves, num_made_moves)
        elif valid_moves.die1_valid and valid_moves.die2_valid:
            if game_dice.die1 > game_dice.die2:
                one_die_input(game_board, game_dice.die1, valid_moves, made_moves, num_made_moves)
            else:
                one_die_input(game_board, game_dice.die2, valid_moves, made_moves, num_made_moves)
        elif valid_moves.die1_valid:
            one_die_input(game_board, game_dice.die1, valid_moves, made_moves, num_made_moves)
        elif valid_moves.die2_valid:
            one_die_input(game_board, game_dice.die2, valid_moves, made_moves, num_made_moves)
    else:
        num_of_moves = valid_moves.equal_die_valid_counter
        print(f"You will have {num_of_moves} moves to do with these dice!!")
        for i in range(0, num_of_moves):
            while True:
                if figures_on_bar(game_board, Figures.white_figure()):
                    input(f'You can only enter the checker to triangle {25 - game_dice.die1}')
                    player_make_a_move(game_dice.die1, game_board, 24 - game_dice.die1, valid_moves, made_moves)
                    if len(made_moves) == num_made_moves:
                        print('Invalid move! Try again')
                    else:
                        break
                else:
                    triangle = player_enter_triangle_num(game_board, get_ordinal_for_num(i + 1))
                    player_make_a_move(game_dice.die1 + i, game_board, triangle, valid_moves, made_moves)
                    if len(made_moves) == num_made_moves:
                        print('Invalid move! Try again')
                    else:
                        break
            num_made_moves = len(made_moves)
            BoardDrawer.generate_table(game_board.triangles, game_board.bar)
            print()


def player_make_a_move(die, game_board, triangle, valid_moves, made_moves):
    moves_made_before = len(made_moves)
    move_made = False
    for moves in valid_moves.moves:
        i = 0
        for key, move in moves.items():
            if moves_made_before == i:
                if key == die:
                    if move[0] == 'bar':
                        if move[1] == triangle:
                            made_moves.append({key: move[0]})
                            move_checker(game_board, move, Figures.white_figure())
                            move_made = True
                            break
                    elif move[0] == triangle - 1:
                        made_moves.append({key: move[0]})
                        move_checker(game_board, move, Figures.white_figure())
                        move_made = True
                        break
            else:
                made_move_key, made_move_source = list(made_moves[i].items())[0]
                if made_move_key == key and made_move_source == move[0]:
                    i += 1
                    continue
                else:
                    break
        if move_made:
            break


def move_checker(game_board, move, figure):
    if move[0] == 'bar':
        game_board.bar.remove(figure)
        checker = figure
    else:
        checker = game_board.triangles[move[0]].pop()
    if move[1] == 'bear':
        if figure == Figures.white_figure():
            game_board.num_of_white -= 1
        else:
            game_board.num_of_black -= 1
    else:
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
            move_checker(game_board, move, Figures.black_figure())


def expectiminimax_bot_makes_move(game_board: Board, valid_moves: Moves, index):
    moves = valid_moves.moves[index]
    for key, move in moves.items():
        if move[0] == 'bar':
            game_board.bar.remove(Figures.black_figure())
            if move[2]:
                bar_checker = game_board.triangles[move[1]].pop()
                game_board.bar.append(bar_checker)
            game_board.triangles[move[1]].append(Figures.black_figure())
        else:
            move_checker(game_board, move, Figures.black_figure())


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
                if game_board.num_of_white == 0:
                    game_over = True
                player_goes_next = False
            else:
                # random_bot_makes_a_move(game_board, moves)
                start_time = timer()
                index = expectiminimax(game_board, 'MAX', 3, True, valid_moves=moves, first_time=True)
                print(timer() - start_time)
                expectiminimax_bot_makes_move(game_board, moves, index)
                if game_board.num_of_black == 0:
                    game_over = True
                player_goes_next = True
        else:
            if player_goes_next:
                print('You have no valid moves. You must skip a turn!')
                player_goes_next = False
            else:
                print('Bot has no valid moves. Bot must skip a turn!')
                player_goes_next = True
        game_dice.roll_dice()
    if game_board.num_of_white == 0:
        print('YOU HAVE WON HOORAY!')
    else:
        print('BOT HAS WON ;(')


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
