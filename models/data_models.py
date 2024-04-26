import copy
from enum import Enum

CELL_SIZE = 70
class Color(Enum):

    RED = 1
    YELLOW = 0

class Cell:
    """
    Cell класс ячеек на игровом поле. У каждой ячейки есть цвет и размер
    """
    def __init__(self, color=Color):
        super().__init__()
        self.size = CELL_SIZE
        self.color = color

class Frame:
    """
        Frame - рамка на игровом поле. Она определяет область, которую можно повернуть
       При повороте рамки, ячейки внутри рамки также поворачиваются"""
    def __init__(self, i=0, j=0):
        """
                Инициализация рамки. Принимает координаты верхнего левого угла рамки
                :param i: координата i"""
        self.i = i
        self.j = j

    def rotate(self, field, clockwise=True):
        i, j = self.i, self.j
        if clockwise:
            # Вращение по часовой стрелке
            temp = field[i][j]
            field[i][j] = field[i + 2][j]
            field[i + 2][j] = field[i + 2][j + 2]
            field[i + 2][j + 2] = field[i][j + 2]
            field[i][j + 2] = temp
            temp = field[i][j + 1]
            field[i][j + 1] = field[i + 1][j]
            field[i + 1][j] = field[i + 2][j + 1]
            field[i + 2][j + 1] = field[i + 1][j + 2]
            field[i + 1][j + 2] = temp
        else:
            # Вращение против часовой стрелки
            temp = field[i][j]
            field[i][j] = field[i][j + 2]
            field[i][j + 2] = field[i + 2][j + 2]
            field[i + 2][j + 2] = field[i + 2][j]
            field[i + 2][j] = temp
            temp = field[i][j + 1]
            field[i][j + 1] = field[i + 1][j + 2]
            field[i + 1][j + 2] = field[i + 2][j + 1]
            field[i + 2][j + 1] = field[i + 1][j]
            field[i + 1][j] = temp
