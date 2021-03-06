from board import Board
from dice import Dice
from figures import Figures
from copy import deepcopy


def set_for_loop(player_figure):
    if player_figure == Figures.white_figure():
        n = 23
        m = -1
        step = -1
    else:
        n = 0
        m = 24
        step = 1
    return n, m, step


def get_opponent_figure(player_figure):
    if player_figure == Figures.white_figure():
        return Figures.black_figure()
    return Figures.white_figure()


def simulate_move(game_board, move, player_figure=None):
    if move[0] == 'bar':
        game_board.bar.remove(player_figure)
        do_move(player_figure, game_board, move)
    else:
        checker = game_board.triangles[move[0]].pop()
        do_move(checker, game_board, move)


def do_move(checker, game_board, move):
    if move[1] == 'bear':
        if checker == Figures.white_figure():
            game_board.num_of_white -= 1
        else:
            game_board.num_of_black -= 1
    elif move[2]:
        bar_checker = game_board.triangles[move[1]].pop()
        game_board.bar.append(bar_checker)
        game_board.triangles[move[1]].append(checker)
    else:
        game_board.triangles[move[1]].append(checker)


def undo_move(game_board, move, player_figure):
    if move[1] == 'bear':
        game_board.triangles[move[0]].append(player_figure)
        if player_figure == Figures.white_figure():
            game_board.num_of_white += 1
        else:
            game_board.num_of_black += 1
    else:
        checker = game_board.triangles[move[1]].pop()
        if move[2]:
            opponent_figure = get_opponent_figure(player_figure)
            game_board.bar.remove(opponent_figure)
            game_board.triangles[move[1]].append(opponent_figure)
        if move[0] == 'bar':
            game_board.bar.append(checker)
        else:
            game_board.triangles[move[0]].append(checker)


def generate_bar_move(game_board, die, moves, player_figure):
    if player_figure == Figures.white_figure():
        bar_exit_triangle = 24 - die
    else:
        bar_exit_triangle = -1 + die
    if len(game_board.triangles[bar_exit_triangle]) == 0:
        moves.append({die: ['bar', bar_exit_triangle, False]})
    else:
        try:
            game_board.triangles[bar_exit_triangle].index(player_figure)
            moves.append({die: ['bar', bar_exit_triangle, False]})
        except ValueError:
            opponent_figure = get_opponent_figure(player_figure)
            try:
                game_board.triangles[bar_exit_triangle].index(opponent_figure)
                if game_board.triangles[bar_exit_triangle].count(opponent_figure) == 1:
                    moves.append({die: ['bar', bar_exit_triangle, True]})
                return
            except ValueError:
                return


def generate_first_move(game_board, die, moves, player_figure):
    if game_board.bar.count(player_figure) > 0:
        generate_bar_move(game_board, die, moves, player_figure)
    else:
        n, m, step = set_for_loop(player_figure)
        for i in range(n, m, step):
            if len(game_board.triangles[i]) == 0:
                continue
            else:
                try:
                    game_board.triangles[i].index(player_figure)
                    next_triangle = i + step * die
                    if next_triangle < 0 or next_triangle > 23:
                        if player_figure == Figures.black_figure():
                            if next_triangle > 23 and game_board.are_all_black_checkers_on_home_board():
                                moves.append({die: [i, 'bear', False]})
                        else:
                            if next_triangle < 0 and game_board.are_all_white_checkers_on_home_board():
                                moves.append({die: [i, 'bear', False]})
                        continue
                    if len(game_board.triangles[next_triangle]) == 0:
                        moves.append({die: [i, next_triangle, False]})  # i - source triangle, next_triangle - destination triangle, hit or not
                    else:
                        try:
                            game_board.triangles[next_triangle].index(player_figure)
                            moves.append({die: [i, next_triangle, False]})
                        except ValueError:
                            opponent_figure = get_opponent_figure(player_figure)
                            try:
                                game_board.triangles[next_triangle].index(opponent_figure)
                                if game_board.triangles[next_triangle].count(opponent_figure) == 1:
                                    moves.append({die: [i, next_triangle, True]})
                                continue
                            except ValueError:
                                continue
                except ValueError:
                    continue


def generate_equal_dice_bar_move(game_board, die, moves, new_moves, player_figure, key):
    if player_figure == Figures.white_figure():
        bar_exit_triangle = 24 - die
    else:
        bar_exit_triangle = -1 + die
    if len(game_board.triangles[bar_exit_triangle]) == 0:
        moves[die + key] = ['bar', bar_exit_triangle, False]
        new_moves.append(deepcopy(moves))
    else:
        try:
            game_board.triangles[bar_exit_triangle].index(player_figure)
            moves[die + key] = ['bar', bar_exit_triangle, False]
            new_moves.append(deepcopy(moves))
        except ValueError:
            opponent_figure = get_opponent_figure(player_figure)
            try:
                game_board.triangles[bar_exit_triangle].index(opponent_figure)
                if game_board.triangles[bar_exit_triangle].count(opponent_figure) == 1:
                    moves[die + key] = ['bar', bar_exit_triangle, True]
                    new_moves.append(deepcopy(moves))
                return
            except ValueError:
                return


class Moves:
    def __init__(self):
        self.moves = list()
        self.one_die_moves = list()
        self.both_die_valid = False
        self.die1_valid = False
        self.die2_valid = False
        self.equal_die_valid_counter = 0

    def generate_second_die_move(self, game_board: Board, die1, die2, player_figure):
        n, m, step = set_for_loop(player_figure)
        for moves in self.one_die_moves:
            for die in list(moves.keys()):
                if die == die1:
                    move = moves[die]
                    simulate_move(game_board, move, player_figure)
                    if game_board.bar.count(player_figure) > 0:
                        new_move = []
                        generate_bar_move(game_board, die2, new_move, player_figure)
                        if len(new_move) != 0:
                            key, item = list(new_move[0].items())[0]
                            self.moves.append({die1: [move[0], move[1], move[2]], key: [item[0], item[1], item[2]]})
                    else:
                        for i in range(n, m, step):
                            if len(game_board.triangles[i]) == 0:
                                continue
                            else:
                                try:
                                    game_board.triangles[i].index(player_figure)
                                    next_triangle = i + step * die2
                                    if next_triangle < 0 or next_triangle > 23:
                                        if player_figure == Figures.black_figure():
                                            if next_triangle > 23 and game_board.are_all_black_checkers_on_home_board():
                                                self.moves.append({die1: [move[0], move[1], move[2]], die2: [i, 'bear', False]})
                                        else:
                                            if next_triangle < 0 and game_board.are_all_white_checkers_on_home_board():
                                                self.moves.append({die1: [move[0], move[1], move[2]], die2: [i, 'bear', False]})
                                        continue
                                    if len(game_board.triangles[next_triangle]) == 0:
                                        self.moves.append({die1: [move[0], move[1], move[2]], die2: [i, next_triangle, False]})
                                    else:
                                        try:
                                            game_board.triangles[next_triangle].index(player_figure)
                                            self.moves.append({die1: [move[0], move[1], move[2]], die2: [i, next_triangle, False]})
                                        except ValueError:
                                            opponent_figure = get_opponent_figure(player_figure)
                                            try:
                                                game_board.triangles[next_triangle].index(opponent_figure)
                                                if game_board.triangles[next_triangle].count(opponent_figure) == 1:
                                                    self.moves.append({die1: [move[0], move[1], move[2]], die2: [i, next_triangle, True]})
                                                continue
                                            except ValueError:
                                                continue
                                except ValueError:
                                    continue
                    undo_move(game_board, move, player_figure)

    def generate_moves(self, game_board: Board, dice: Dice, player_figure):
        if dice.die1 == dice.die2:
            self.generate_equal_dice_moves(game_board, dice, player_figure)
            return
        size = 0
        generate_first_move(game_board, dice.die1, self.one_die_moves, player_figure)
        if len(self.one_die_moves) != 0:
            self.die1_valid = True
            self.generate_second_die_move(game_board, dice.die1, dice.die2, player_figure)
            if len(self.moves) != 0:
                self.die2_valid = True
                self.both_die_valid = True
            else:
                self.moves = deepcopy(self.one_die_moves)
                size = len(self.moves)
        self.one_die_moves = list()
        generate_first_move(game_board, dice.die2, self.one_die_moves, player_figure)
        if len(self.one_die_moves) != 0:
            self.die2_valid = True
            self.generate_second_die_move(game_board, dice.die2, dice.die1, player_figure)
            if len(self.moves) > size:
                self.die1_valid = True
                self.both_die_valid = True
            else:
                self.moves.extend(self.one_die_moves)
        if len(self.moves) != 0:
            if self.both_die_valid:
                for move in list(self.moves):
                    if len(move.keys()) != 2:
                        self.moves.remove(move)
            elif self.die2_valid and self.die1_valid:
                if dice.die1 > dice.die2:
                    for move in list(self.moves):
                        if list(move.keys())[0] != dice.die1:
                            self.moves.remove(move)
                else:
                    for move in list(self.moves):
                        if list(move.keys())[0] != dice.die2:
                            self.moves.remove(move)
        self.one_die_moves = list()

    def generate_equal_dice_moves(self, game_board, dice, player_figure):
        size = len(self.moves)
        for i in range(0, 4):
            self.generate_equal_dice_move(game_board, dice.die1, player_figure)
            if len(self.moves) == 0:
                break
            else:
                if len(self.moves) > size or len(self.moves[0].keys()) > self.equal_die_valid_counter:
                    self.equal_die_valid_counter += 1
                    size = len(self.moves)
                else:
                    break
        for moves in list(self.moves):
            if len(moves.keys()) < self.equal_die_valid_counter:
                self.moves.remove(moves)

    def generate_equal_dice_move(self, game_board, die, player_figure):
        if len(self.moves) == 0:
            generate_first_move(game_board, die, self.moves, player_figure)
        else:
            old_moves = deepcopy(self.moves)
            new_moves = list()
            for moves in list(self.moves):
                self.moves.remove(moves)
                current_moves = deepcopy(moves)
                for key, move in list(moves.items()):
                    simulate_move(game_board, move, player_figure)
                n, m, step = set_for_loop(player_figure)
                if game_board.bar.count(player_figure) > 0:
                    generate_equal_dice_bar_move(game_board, die, moves, new_moves, player_figure, self.equal_die_valid_counter)
                else:
                    for i in range(n, m, step):
                        if len(game_board.triangles[i]) == 0:
                            continue
                        else:
                            try:
                                game_board.triangles[i].index(player_figure)
                                next_triangle = i + step * die
                                if next_triangle < 0 or next_triangle > 23:
                                    if player_figure == Figures.black_figure():
                                        if next_triangle > 23 and game_board.are_all_black_checkers_on_home_board():
                                            moves[die + self.equal_die_valid_counter] = [i, 'bear', False]
                                            new_moves.append(deepcopy(moves))
                                    else:
                                        if next_triangle < 0 and game_board.are_all_white_checkers_on_home_board():
                                            moves[die + self.equal_die_valid_counter] = [i, 'bear', False]
                                            new_moves.append(deepcopy(moves))
                                    continue
                                if len(game_board.triangles[next_triangle]) == 0:
                                    moves[die + self.equal_die_valid_counter] = [i, next_triangle, False]
                                    new_moves.append(deepcopy(moves))
                                else:
                                    try:
                                        game_board.triangles[next_triangle].index(player_figure)
                                        moves[die + self.equal_die_valid_counter] = [i, next_triangle, False]
                                        new_moves.append(deepcopy(moves))
                                    except ValueError:
                                        opponent_figure = get_opponent_figure(player_figure)
                                        try:
                                            game_board.triangles[next_triangle].index(opponent_figure)
                                            if game_board.triangles[next_triangle].count(opponent_figure) == 1:
                                                moves[die + self.equal_die_valid_counter] = [i, next_triangle, True]
                                                new_moves.append(deepcopy(moves))
                                            continue
                                        except ValueError:
                                            continue
                            except ValueError:
                                continue
                current_moves = dict(reversed(list(current_moves.items())))
                for key, move in list(current_moves.items()):
                    undo_move(game_board, move, player_figure)
            if len(new_moves) != 0:
                self.moves.extend(new_moves)
            else:
                self.moves.extend(old_moves)
