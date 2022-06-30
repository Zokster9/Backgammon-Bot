from figures import Figures


class Board:
    def __init__(self):
        self.black = Figures.black_figure()
        self.white = Figures.white_figure()
        triangle_1 = [self.black, self.black]
        triangle_2 = list()
        triangle_3 = list()
        triangle_4 = list()
        triangle_5 = list()
        triangle_6 = [self.white, self.white, self.white, self.white, self.white]
        triangle_7 = list()
        triangle_8 = [self.white, self.white, self.white]
        triangle_9 = list()
        triangle_10 = list()
        triangle_11 = list()
        triangle_12 = [self.black, self.black, self.black, self.black, self.black]
        triangle_13 = [self.white, self.white, self.white, self.white, self.white]
        triangle_14 = list()
        triangle_15 = list()
        triangle_16 = list()
        triangle_17 = [self.black, self.black, self.black]
        triangle_18 = list()
        triangle_19 = [self.black, self.black, self.black, self.black, self.black]
        triangle_20 = list()
        triangle_21 = list()
        triangle_22 = list()
        triangle_23 = list()
        triangle_24 = [self.white, self.white]
        self.num_of_white = 15
        self.num_of_black = 15
        self.white_home_board = [triangle_1, triangle_2, triangle_3, triangle_4, triangle_5, triangle_6]
        self.black_home_board = [triangle_19, triangle_20, triangle_21, triangle_22, triangle_23, triangle_24]
        self.bar = [self.black]
        self.triangles = [triangle_1, triangle_2, triangle_3, triangle_4, triangle_5, triangle_6, triangle_7,
                          triangle_8,
                          triangle_9, triangle_10, triangle_11, triangle_12, triangle_13, triangle_14, triangle_15,
                          triangle_16,
                          triangle_17, triangle_18, triangle_19, triangle_20, triangle_21, triangle_22, triangle_23,
                          triangle_24]


class BoardDrawer:
    @staticmethod
    def generate_table(triangles, bar):
        print('      13        14        15        16        17        18          19        20        21        22        23        24     ')
        print('=============================================================================================================================')
        bar_index = 0
        print(BoardDrawer.fill_first_triangle_row(triangles, 12, 17, 1, bar, bar_index))
        bar_index += 1
        print(BoardDrawer.fill_second_triangle_row(triangles, 12, 17, 1, bar, bar_index))
        bar_index += 1
        print(BoardDrawer.fill_third_triangle_row(triangles, 12, 17, 1, bar, bar_index))
        bar_index += 1
        print(BoardDrawer.fill_fourth_triangle_row(triangles, 12, 17, 1, bar, bar_index))
        bar_index += 1
        print(BoardDrawer.fill_fifth_triangle_row(triangles, 12, 17, 1, bar, bar_index))
        bar_index += 1
        BoardDrawer.print_extra_rows(triangles, bar, bar_index)
        bar_index += 5
        print(BoardDrawer.fill_fifth_triangle_row(triangles, 11, 6, -1, bar, bar_index))
        bar_index += 1
        print(BoardDrawer.fill_fourth_triangle_row(triangles, 11, 6, -1, bar, bar_index))
        bar_index += 1
        print(BoardDrawer.fill_third_triangle_row(triangles, 11, 6, -1, bar, bar_index))
        bar_index += 1
        print(BoardDrawer.fill_second_triangle_row(triangles, 11, 6, -1, bar, bar_index))
        bar_index += 1
        print(BoardDrawer.fill_first_triangle_row(triangles, 11, 6, -1, bar, bar_index))
        bar_index += 1
        print('=============================================================================================================================')
        print('      12        11        10        09        08        07          06        05        04        03        02        01    ')

    @staticmethod
    def fill_extra_spots(triangles, i, j, lower_triangles_idx, upper_triangles_idx):
        spot = ' '
        if len(triangles[upper_triangles_idx]) == (5 + i):
            spot = triangles[upper_triangles_idx][5 + i - 1]
        elif len(triangles[lower_triangles_idx]) == (5 + j):
            spot = triangles[lower_triangles_idx][5 + j - 1]
        return spot

    @staticmethod
    def fill_bar_spot(bar, i):
        bar_spot = ' '
        if len(bar) >= (i + 1):
            bar_spot = bar[i]
        return f'|{bar_spot}|'

    @staticmethod
    def fill_first_triangle_row(triangles, first_triangle, last_triangle, step, bar, bar_index):
        row = '||'
        for i in range(first_triangle, last_triangle + step, step):
            if len(triangles[i]) == 0:
                row += '.........'
            else:
                row += f'....{triangles[i][0]}....'
            if i != last_triangle:
                row += ' '
        row += BoardDrawer.fill_bar_spot(bar, bar_index)
        for i in range(first_triangle + 6 * step, last_triangle + 6 * step + step, step):
            if len(triangles[i]) == 0:
                row += '.........'
            else:
                row += f'....{triangles[i][0]}....'
            if i != last_triangle + 6 * step:
                row += ' '
        row += '||'
        return row

    @staticmethod
    def fill_second_triangle_row(triangles, first_triangle, last_triangle, step, bar, bar_index):
        row = '|| '
        for i in range(first_triangle, last_triangle + step, step):
            if len(triangles[i]) < 2:
                row += '.......'
            else:
                row += f'...{triangles[i][1]}...'
            if i != last_triangle:
                row += '   '
            else:
                row += ' '
        row += BoardDrawer.fill_bar_spot(bar, bar_index) + ' '
        for i in range(first_triangle + 6 * step, last_triangle + 6 * step + step, step):
            if len(triangles[i]) < 2:
                row += '.......'
            else:
                row += f'...{triangles[i][1]}...'
            if i != last_triangle + 6 * step:
                row += '   '
            else:
                row += ' '
        row += '||'
        return row

    @staticmethod
    def fill_third_triangle_row(triangles, first_triangle, last_triangle, step, bar, bar_index):
        row = '||  '
        for i in range(first_triangle, last_triangle + step, step):
            if len(triangles[i]) < 3:
                row += '.....'
            else:
                row += f'..{triangles[i][2]}..'
            if i != last_triangle:
                row += '     '
            else:
                row += '  '
        row += BoardDrawer.fill_bar_spot(bar, bar_index) + '  '
        for i in range(first_triangle + 6 * step, last_triangle + 6 * step + step, step):
            if len(triangles[i]) < 3:
                row += '.....'
            else:
                row += f'..{triangles[i][2]}..'
            if i != last_triangle + 6 * step:
                row += '     '
            else:
                row += '  '
        row += '||'
        return row

    @staticmethod
    def fill_fourth_triangle_row(triangles, first_triangle, last_triangle, step, bar, bar_index):
        row = '||   '
        for i in range(first_triangle, last_triangle + step, step):
            if len(triangles[i]) < 4:
                row += '...'
            else:
                row += f'.{triangles[i][3]}.'
            if i != last_triangle:
                row += '       '
            else:
                row += '   '
        row += BoardDrawer.fill_bar_spot(bar, bar_index) + '   '
        for i in range(first_triangle + 6 * step, last_triangle + 6 * step + step, step):
            if len(triangles[i]) < 4:
                row += '...'
            else:
                row += f'.{triangles[i][3]}.'
            if i != last_triangle + 6 * step:
                row += '       '
            else:
                row += '   '
        row += '||'
        return row

    @staticmethod
    def fill_fifth_triangle_row(triangles, first_triangle, last_triangle, step, bar, bar_index):
        row = '||    '
        for i in range(first_triangle, last_triangle + step, step):
            if len(triangles[i]) < 5:
                row += '.'
            else:
                row += f'{triangles[i][4]}'
            if i != last_triangle:
                row += '         '
            else:
                row += '    '
        row += BoardDrawer.fill_bar_spot(bar, bar_index) + '    '
        for i in range(first_triangle + 6 * step, last_triangle + 6 * step + step, step):
            if len(triangles[i]) < 5:
                row += '.'
            else:
                row += f'{triangles[i][4]}'
            if i != last_triangle + 6 * step:
                row += '         '
            else:
                row += '    '
        row += '||'
        return row

    @staticmethod
    def print_extra_rows(triangles, bar, bar_index):
        n = 10
        for i in range(1, n):
            j = n - i
            upper_triangles_idx = 12
            lower_triangles_idx = 11
            spot_1 = BoardDrawer.fill_extra_spots(triangles, i, j, lower_triangles_idx, upper_triangles_idx)
            spot_2 = BoardDrawer.fill_extra_spots(triangles, i, j, lower_triangles_idx - 1, upper_triangles_idx + 1)
            spot_3 = BoardDrawer.fill_extra_spots(triangles, i, j, lower_triangles_idx - 2, upper_triangles_idx + 2)
            spot_4 = BoardDrawer.fill_extra_spots(triangles, i, j, lower_triangles_idx - 3, upper_triangles_idx + 3)
            spot_5 = BoardDrawer.fill_extra_spots(triangles, i, j, lower_triangles_idx - 4, upper_triangles_idx + 4)
            spot_6 = BoardDrawer.fill_extra_spots(triangles, i, j, lower_triangles_idx - 5, upper_triangles_idx + 5)
            spot_7 = BoardDrawer.fill_extra_spots(triangles, i, j, lower_triangles_idx - 6, upper_triangles_idx + 6)
            spot_8 = BoardDrawer.fill_extra_spots(triangles, i, j, lower_triangles_idx - 7, upper_triangles_idx + 7)
            spot_9 = BoardDrawer.fill_extra_spots(triangles, i, j, lower_triangles_idx - 8, upper_triangles_idx + 8)
            spot_10 = BoardDrawer.fill_extra_spots(triangles, i, j, lower_triangles_idx - 9, upper_triangles_idx + 9)
            spot_11 = BoardDrawer.fill_extra_spots(triangles, i, j, lower_triangles_idx - 10, upper_triangles_idx + 10)
            spot_12 = BoardDrawer.fill_extra_spots(triangles, i, j, lower_triangles_idx - 11, upper_triangles_idx + 11)
            row = f'||    {spot_1}         {spot_2}         {spot_3}         {spot_4}         {spot_5}         {spot_6}    ' \
                  + BoardDrawer.fill_bar_spot(bar, bar_index) + f'    {spot_7}         {spot_8}         {spot_9}         {spot_10}         {spot_11}         {spot_12}    ||'
            print(row)
            bar_index += 1
