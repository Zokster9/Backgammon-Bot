from figures import BlackFigure, WhiteFigure


class Board:
    def __init__(self):
        self.black = BlackFigure.figure()
        self.white = WhiteFigure.figure()
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
        self.white_home_board = [triangle_1, triangle_2, triangle_3, triangle_4, triangle_5, triangle_6]
        self.black_home_board = [triangle_19, triangle_20, triangle_21, triangle_22, triangle_23, triangle_24]
        self.bar = []
        self.triangles = [triangle_1, triangle_2, triangle_3, triangle_4, triangle_5, triangle_6, triangle_7,
                          triangle_8,
                          triangle_9, triangle_10, triangle_11, triangle_12, triangle_13, triangle_14, triangle_15,
                          triangle_16,
                          triangle_17, triangle_18, triangle_19, triangle_20, triangle_21, triangle_22, triangle_23,
                          triangle_24]


class BoardDrawer:
    def __init__(self, triangles, bar):
        self.triangles = triangles
        self.bar = bar

    def generate_table(self):
        print('      13        14        15        16        17        18          19        20        21        22        23        24     ')
        print('=============================================================================================================================')
        bar_index = 0
        print(self.fill_first_triangle_row(12, 17, 1, bar_index))
        bar_index += 1
        print(self.fill_second_triangle_row(12, 17, 1, bar_index))
        bar_index += 1
        print(self.fill_third_triangle_row(12, 17, 1, bar_index))
        bar_index += 1
        print(self.fill_fourth_triangle_row(12, 17, 1, bar_index))
        bar_index += 1
        print(self.fill_fifth_triangle_row(12, 17, 1, bar_index))
        bar_index += 1
        self.print_extra_rows(bar_index)
        bar_index += 5
        print(self.fill_fifth_triangle_row(11, 6, -1, bar_index))
        bar_index += 1
        print(self.fill_fourth_triangle_row(11, 6, -1, bar_index))
        bar_index += 1
        print(self.fill_third_triangle_row(11, 6, -1, bar_index))
        bar_index += 1
        print(self.fill_second_triangle_row(11, 6, -1, bar_index))
        bar_index += 1
        print(self.fill_first_triangle_row(11, 6, -1, bar_index))
        bar_index += 1
        print('=============================================================================================================================')
        print('      12        11        10        09        08        07          06        05        04        03        02        01    ')

    def fill_extra_spots(self, i, j, lower_triangles_idx, upper_triangles_idx):
        spot = ' '
        if len(self.triangles[upper_triangles_idx]) == (5 + i):
            spot = self.triangles[upper_triangles_idx][5 + i - 1]
        elif len(self.triangles[lower_triangles_idx]) == (5 + j):
            spot = self.triangles[lower_triangles_idx][5 + j - 1]
        return spot

    def fill_bar_spot(self, i):
        bar_spot = ' '
        if len(self.bar) >= (i + 1):
            bar_spot = self.bar[i]
        return f'|{bar_spot}|'

    def fill_first_triangle_row(self, first_triangle, last_triangle, step, bar_index):
        row = '||'
        for i in range(first_triangle, last_triangle + step, step):
            if len(self.triangles[i]) == 0:
                row += '.........'
            else:
                row += f'....{self.triangles[i][0]}....'
            if i != last_triangle:
                row += ' '
        row += self.fill_bar_spot(bar_index)
        for i in range(first_triangle + 6 * step, last_triangle + 6 * step + step, step):
            if len(self.triangles[i]) == 0:
                row += '.........'
            else:
                row += f'....{self.triangles[i][0]}....'
            if i != last_triangle + 6 * step:
                row += ' '
        row += '||'
        return row

    def fill_second_triangle_row(self, first_triangle, last_triangle, step, bar_index):
        row = '|| '
        for i in range(first_triangle, last_triangle + step, step):
            if len(self.triangles[i]) < 2:
                row += '.......'
            else:
                row += f'...{self.triangles[i][1]}...'
            if i != last_triangle:
                row += '   '
            else:
                row += ' '
        row += self.fill_bar_spot(bar_index) + ' '
        for i in range(first_triangle + 6 * step, last_triangle + 6 * step + step, step):
            if len(self.triangles[i]) < 2:
                row += '.......'
            else:
                row += f'...{self.triangles[i][1]}...'
            if i != last_triangle + 6 * step:
                row += '   '
            else:
                row += ' '
        row += '||'
        return row

    def fill_third_triangle_row(self, first_triangle, last_triangle, step, bar_index):
        row = '||  '
        for i in range(first_triangle, last_triangle + step, step):
            if len(self.triangles[i]) < 3:
                row += '.....'
            else:
                row += f'..{self.triangles[i][2]}..'
            if i != last_triangle:
                row += '     '
            else:
                row += '  '
        row += self.fill_bar_spot(bar_index) + '  '
        for i in range(first_triangle + 6 * step, last_triangle + 6 * step + step, step):
            if len(self.triangles[i]) < 3:
                row += '.....'
            else:
                row += f'..{self.triangles[i][2]}..'
            if i != last_triangle + 6 * step:
                row += '     '
            else:
                row += '  '
        row += '||'
        return row

    def fill_fourth_triangle_row(self, first_triangle, last_triangle, step, bar_index):
        row = '||   '
        for i in range(first_triangle, last_triangle + step, step):
            if len(self.triangles[i]) < 4:
                row += '...'
            else:
                row += f'.{self.triangles[i][3]}.'
            if i != last_triangle:
                row += '       '
            else:
                row += '   '
        row += self.fill_bar_spot(bar_index) + '   '
        for i in range(first_triangle + 6 * step, last_triangle + 6 * step + step, step):
            if len(self.triangles[i]) < 4:
                row += '...'
            else:
                row += f'.{self.triangles[i][3]}.'
            if i != last_triangle + 6 * step:
                row += '       '
            else:
                row += '   '
        row += '||'
        return row

    def fill_fifth_triangle_row(self, first_triangle, last_triangle, step, bar_index):
        row = '||    '
        for i in range(first_triangle, last_triangle + step, step):
            if len(self.triangles[i]) < 5:
                row += '.'
            else:
                row += f'{self.triangles[i][4]}'
            if i != last_triangle:
                row += '         '
            else:
                row += '    '
        row += self.fill_bar_spot(bar_index) + '    '
        for i in range(first_triangle + 6 * step, last_triangle + 6 * step + step, step):
            if len(self.triangles[i]) < 5:
                row += '.'
            else:
                row += f'{self.triangles[i][4]}'
            if i != last_triangle + 6 * step:
                row += '         '
            else:
                row += '    '
        row += '||'
        return row

    def print_extra_rows(self, bar_index):
        n = 10
        for i in range(1, n):
            j = n - i
            upper_triangles_idx = 12
            lower_triangles_idx = 11
            spot_1 = self.fill_extra_spots(i, j, lower_triangles_idx, upper_triangles_idx)
            spot_2 = self.fill_extra_spots(i, j, lower_triangles_idx - 1, upper_triangles_idx + 1)
            spot_3 = self.fill_extra_spots(i, j, lower_triangles_idx - 2, upper_triangles_idx + 2)
            spot_4 = self.fill_extra_spots(i, j, lower_triangles_idx - 3, upper_triangles_idx + 3)
            spot_5 = self.fill_extra_spots(i, j, lower_triangles_idx - 4, upper_triangles_idx + 4)
            spot_6 = self.fill_extra_spots(i, j, lower_triangles_idx - 5, upper_triangles_idx + 5)
            spot_7 = self.fill_extra_spots(i, j, lower_triangles_idx - 6, upper_triangles_idx + 6)
            spot_8 = self.fill_extra_spots(i, j, lower_triangles_idx - 7, upper_triangles_idx + 7)
            spot_9 = self.fill_extra_spots(i, j, lower_triangles_idx - 8, upper_triangles_idx + 8)
            spot_10 = self.fill_extra_spots(i, j, lower_triangles_idx - 9, upper_triangles_idx + 9)
            spot_11 = self.fill_extra_spots(i, j, lower_triangles_idx - 10, upper_triangles_idx + 10)
            spot_12 = self.fill_extra_spots(i, j, lower_triangles_idx - 11, upper_triangles_idx + 11)
            row = f'||    {spot_1}         {spot_2}         {spot_3}         {spot_4}         {spot_5}         {spot_6}    ' \
                  + self.fill_bar_spot(bar_index) + f'    {spot_7}         {spot_8}         {spot_9}         {spot_10}         {spot_11}         {spot_12}    ||'
            print(row)
            bar_index += 1


if __name__ == '__main__':
    board = Board()
    boardDrawer = BoardDrawer(board.triangles, board.bar)
    boardDrawer.generate_table()
