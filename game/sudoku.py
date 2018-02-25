class Sudoku:
    def __init__(self, initial_value):
        self.m_values = initial_value
        if not self.is_valid():
            raise ValueError('Invalid initial values')

    def is_valid(self):
        size = len(self.m_values)
        if size is not 9:
            return False
        is_square = all(len(row) == size for row in self.m_values)
        if is_square:
            for row in self.m_values:
                for value in row:
                    if value == '':
                        return False
        return True

    def is_complete(self):
        return all(len(self.m_values[row][col]) == 1 for col in range(len(self.m_values[0])) for row in
                   range(len(self.m_values)))

    def get_values(self):
        return self.m_values

    def update_value(self, x, y, new_value):
        self.m_values[x][y] = new_value

    def get_possible_values(self, x, y):
        pv = []
        for v in list(self.m_values[x][y]):
            pv.append(str(v))
        return pv

    def update_possible_values(self, x, y, value):
        # update row
        for idx in range(len(self.m_values[0])):
            if idx != y:
                self.__remove_possible_value(x, idx, value)
        # update col
        for idx in range(len(self.m_values)):
            if idx != x:
                self.__remove_possible_value(idx, y, value)
        # update box
        box_x, box_y = (x // 3) * 3, (y // 3) * 3
        for idx_x in range(3):
            for idx_y in range(3):
                if box_x + idx_x != x and box_y + idx_y != y:
                    self.__remove_possible_value(box_x + idx_x, box_y + idx_y, value)

    def __remove_possible_value(self, x, y, value):
        self.m_values[x][y] = str(self.m_values[x][y]).replace(value, "")

    def deepcopy(self):
        return Sudoku([x[:] for x in self.m_values])
