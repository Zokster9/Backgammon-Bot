from random import randint
from timeit import default_timer as timer

from board import Board
from dice import Dice, Die
from expectiminimax import expectiminimax
from figures import Figures
from moves import Moves

expectiminimax_won = 0
random_bot_won = 0
turn_counter = 0
total_time = 0


def figures_on_bar(game_board: Board, player_figure):
    if len(game_board.bar) == 0:
        return False
    try:
        game_board.bar.index(player_figure)
        return True
    except ValueError:
        return False


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
            game_board.bar.remove(Figures.white_figure())
            if move[2]:
                bar_checker = game_board.triangles[move[1]].pop()
                game_board.bar.append(bar_checker)
            game_board.triangles[move[1]].append(Figures.white_figure())
        else:
            move_checker(game_board, move, Figures.white_figure())


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


def get_player_figure(random_bot_goes_first):
    if random_bot_goes_first:
        return Figures.white_figure()
    return Figures.black_figure()


def game(game_board: Board, game_dice: Dice, random_bot_goes_first):
    global expectiminimax_won, random_bot_won, turn_counter, total_time
    game_over = False
    while not game_over:
        moves = Moves()
        moves.generate_moves(game_board, game_dice, get_player_figure(random_bot_goes_first))
        if len(moves.moves) > 0:
            if random_bot_goes_first:
                random_bot_makes_a_move(game_board, moves)
                if game_board.num_of_white == 0:
                    game_over = True
                random_bot_goes_first = False
            else:
                turn_counter += 1
                start_time = timer()
                if game_dice.die1 == game_dice.die2:
                    index = expectiminimax(game_board, 'MAX', 1, True, valid_moves=moves, first_time=True)
                else:
                    index = expectiminimax(game_board, 'MAX', 3, True, valid_moves=moves, first_time=True)
                total_time += timer() - start_time
                print(timer() - start_time)
                expectiminimax_bot_makes_move(game_board, moves, index)
                if game_board.num_of_black == 0:
                    game_over = True
                random_bot_goes_first = True
        else:
            if random_bot_goes_first:
                random_bot_goes_first = False
            else:
                random_bot_goes_first = True
        game_dice.roll_dice()
    if game_board.num_of_white == 0:
        random_bot_won += 1
        print('Random won')
    else:
        expectiminimax_won += 1
        print('Expecti won')


if __name__ == '__main__':
    n = 100
    for i in range(0, n):
        print(f'Game number: {i + 1}')
        random_bot_turn = False
        board = Board()
        dice = Dice(Die(), Die())
        while True:
            dice.roll_dice()
            if dice.die1 > dice.die2:
                random_bot_turn = True
                break
            elif dice.die1 < dice.die2:
                break
        game(board, dice, random_bot_turn)
    expectiminimax_win_percentage = round((expectiminimax_won / n) * 100, 2)
    random_bot_win_percentage = round((random_bot_won / n) * 100, 2)
    average_turn_time = round(total_time / turn_counter, 2)
    print(f'Expectiminimax won {expectiminimax_won} times.')
    print(f'Random bot won {random_bot_won} times.')
    print(f'Expectiminimax won {expectiminimax_win_percentage} percent of games.')
    print(f'Random bot won {random_bot_win_percentage} percent of games.')
    print(f'Expectiminimax bot average turn time: {average_turn_time}')
    f = open('results/againts_random_bot.txt', 'a')
    f.write(f'Expectiminimax won {expectiminimax_won} times.\n')
    f.write(f'Random bot won {random_bot_won} times.\n')
    f.write(f'Expectiminimax won {expectiminimax_win_percentage} percent of games.\n')
    f.write(f'Random bot won {random_bot_win_percentage} percent of games.\n')
    f.write(f'Expectiminimax bot average turn time: {average_turn_time}\n')
    f.close()
