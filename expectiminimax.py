from copy import deepcopy

from board import Board
from dice import Dice, Die
from figures import Figures
from moves import Moves, undo_move
from math import inf


def boards_same(board1, board2):
    for i in range(0, len(board1.triangles)):
        if board1.triangles[i] != board2.triangles[i]:
            print(i)
            return False
    return True


def make_move(game_board: Board, moves, maximizing_player):
    for key, move in moves.items():
        if move[0] == 'bar':
            if maximizing_player:
                checker = Figures.black_figure()
                game_board.bar.remove(checker)
            else:
                checker = Figures.white_figure()
                game_board.bar.remove(checker)
        else:
            checker = game_board.triangles[move[0]].pop()
        if move[1] == 'bear':
            if checker == Figures.white_figure():
                game_board.num_of_white -= 1
            else:
                game_board.num_of_black -= 1
        else:
            if move[2]:
                bar_checker = game_board.triangles[move[1]].pop()
                game_board.bar.append(bar_checker)
            game_board.triangles[move[1]].append(checker)


def weighted_result(made_moves, game_dice):
    if game_dice.die1 != game_dice.die2:
        return sum(made_moves) * (2 / 36)
    else:
        return sum(made_moves) * (1 / 36)


def get_player_figure(maximizing_player):
    if maximizing_player:
        return Figures.black_figure()
    else:
        return Figures.white_figure()


def heuristic_value(game_board):
    difference_num_checkers = game_board.num_of_white - game_board.num_of_black
    difference_num_bar_checkers = game_board.bar.count(Figures.white_figure()) - game_board.bar.count(Figures.black_figure())
    difference_num_checkers_home_board = game_board.get_num_black_checkers_on_home_board() - game_board.get_num_white_checkers_on_home_board()
    difference_num_of_points = game_board.get_num_black_points() - game_board.get_num_white_points()
    difference_num_of_blots = game_board.get_num_white_bloats() - game_board.get_num_black_bloats()
    return 10 * difference_num_checkers + 15 * difference_num_bar_checkers + 3 * difference_num_checkers_home_board + difference_num_of_points + difference_num_of_blots


def find_best_move(made_moves):
    max_index = 0
    max_val = -inf
    for moves in made_moves:
        for key, score in moves.items():
            if score > max_val:
                max_index = key
                max_val = score
    return max_index


def expectiminimax(game_board: Board, node_type, depth, maximizing_player, game_dice: Dice = None, valid_moves: Moves = None, first_time=False):
    made_moves = list()
    result = None
    if node_type == 'MAX':
        if depth == 0:
            return heuristic_value(game_board)
        if first_time:
            i = 0
            for moves in valid_moves.moves:
                make_move(game_board, moves, maximizing_player)
                made_moves.append({i: expectiminimax(game_board, 'MIN', depth - 1, False)})
                reversed_moves = deepcopy(moves)
                reversed_moves = dict(reversed(list(reversed_moves.items())))
                for key, move in reversed_moves.items():
                    undo_move(game_board, move, get_player_figure(maximizing_player))
                i += 1
            return find_best_move(made_moves)
        else:
            dice = Dice(Die(), Die())
            for i in range(1, 7):
                for j in range(1, 7):
                    dice.die1 = i
                    dice.die2 = j
                    made_moves.append(expectiminimax(game_board, 'CHANCE', depth - 1, True, dice))
            result = max(made_moves)
    elif node_type == 'MIN':
        if depth == 0:
            return heuristic_value(game_board)
        dice = Dice(Die(), Die())
        for i in range(1, 7):
            for j in range(1, 7):
                dice.die1 = i
                dice.die2 = j
                made_moves.append(expectiminimax(game_board, 'CHANCE', depth - 1, False, dice))
        result = min(made_moves)
    elif node_type == 'CHANCE':
        if depth == 0:
            return heuristic_value(game_board)
        valid_moves = Moves()
        if maximizing_player:
            valid_moves.generate_moves(game_board, game_dice, Figures.black_figure())
        else:
            valid_moves.generate_moves(game_board, game_dice, Figures.white_figure())
        if len(valid_moves.moves) == 0:
            if maximizing_player:
                return -100
            else:
                return 100
        else:
            for moves in valid_moves.moves:
                make_move(game_board, moves, maximizing_player)
                if maximizing_player:
                    made_moves.append(expectiminimax(game_board, 'MIN', depth - 1, not maximizing_player))
                else:
                    made_moves.append(expectiminimax(game_board, 'MAX', depth - 1, not maximizing_player))
                reversed_moves = deepcopy(moves)
                reversed_moves = dict(reversed(list(reversed_moves.items())))
                for key, move in reversed_moves.items():
                    undo_move(game_board, move, get_player_figure(maximizing_player))
            result = weighted_result(made_moves, game_dice)
    return result
