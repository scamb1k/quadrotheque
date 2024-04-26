import random
from models.data_models import Frame, Color, Cell


class GameField:
    def __init__(self, field_size):
        """
        Конструктор класса GameField, инициализирующий игровое поле

        Args:
        field_size (int): Размер поля (количество ячеек в строке и столбце)

        Инициализирует поле игры размером field_size x field_size, заполняя его ячейками,
        цвета которых чередуются между красным и жёлтым. Также создаёт рамку в начальной позиции (0, 0)
        и выполняет первоначальное перемешивание поля
        """
        self.field_size = field_size  # Задаём размер поля
        # Создание поля с чередующимися цветами красный и желтый
        self.field = [[Cell(Color.RED if j % 2 == 0 else Color.YELLOW) for j in range(field_size)] for i in
                      range(field_size)]
        self.frame = Frame(0, 0)  # Создание рамки для манипуляций с ячейками
        self.shuffle()  # Перемешивание ячеек на поле

    def rotate(self):
        """
        Выполняет поворот ячеек в рамке на 90 градусов по часовой стрелке

        Метод делегирует(значит передает работу другому классу) поворот ячеек методу rotate класса Frame
        """
        self.frame.rotate(self.field, clockwise=True)

    def reverse_rotate(self):
        """
         Вращает ячейки в рамке на 90 градусов против часовой стрелки.

        clockwise (bool): Направление вращения ячеек в рамке. True - по часовой стрелке, False - против часовой стрелки
        """
        self.frame.rotate(self.field, clockwise=False)

    def setup_field(self):
        """
        Устанавливает начальное состояние поля с заданным распределением красных и жёлтых строк.
        """
        # Определение количества красных и жёлтых строк
        half_size = self.field_size // 2
        red_rows = half_size + (self.field_size % 2)  # Если размер нечётный, добавляем одну красную строку
        yellow_rows = half_size

        # Создание списка строк с заданным количеством красных и жёлтых
        colors = [Color.RED] * red_rows + [Color.YELLOW] * yellow_rows
        random.shuffle(colors)  # Перемешиваем распределение строк

        for i in range(self.field_size):
            self.field[i] = [Cell(colors[i]) for _ in range(self.field_size)]

        # Создание одной или двух "почти завершённых" строк
        for _ in range(random.randint(1, 2)):  # Случайный выбор создания 1 или 2 строк
            row = random.randint(0, self.field_size - 1)
            col = random.randint(0, self.field_size - 1)
            # Изменение цвета одной ячейки в строке
            self.field[row][col] = Cell(Color.YELLOW if colors[row] == Color.RED else Color.RED)

    def shuffle(self):
        """
        Выполняет лёгкое перемешивание поля, чтобы оно могло быть возвращено в выигрышное состояние за несколько ходов.
        """
        steps = random.randint(1, 3)  # Количество шагов для перемешивания
        for _ in range(steps):
            self.frame.i = random.randint(0, self.field_size - 3)
            self.frame.j = random.randint(0, self.field_size - 3)
            if random.choice([True, False]):
                self.rotate()  # Поворот по часовой стрелке
            else:
                self.reverse_rotate()  # Поворот против часовой стрелки

        # Сброс рамки в исходное положение
        self.frame.i, self.frame.j = 0, 0

    def check_rows(self):
        """
        Проверяет наличие полностью заполненных строк или столбцов одним цветом

        Возвращает:
        total_full_lines (int): Количество полностью заполненных строк и столбцов одним цветом

        Метод проходит по всем строкам и столбцам, считая количество ячеек каждого цвета и
        определяет, заполнены ли строки или столбцы одним цветом полностью
        """
        total_full_lines = 0
        # Проверка каждой строки на заполненность одним цветом
        for i in range(self.field_size):
            row_red_count = sum(1 for cell in self.field[i] if cell.color == Color.RED)
            row_yellow_count = sum(1 for cell in self.field[i] if cell.color == Color.YELLOW)
            if row_red_count == self.field_size or row_yellow_count == self.field_size:
                total_full_lines += 1

        # Проверка каждого столбца на заполненность одним цветом
        for j in range(self.field_size):
            column_red_count = sum(1 for i in range(self.field_size) if self.field[i][j].color == Color.RED)
            column_yellow_count = sum(1 for i in range(self.field_size) if self.field[i][j].color == Color.YELLOW)
            if column_red_count == self.field_size or column_yellow_count == self.field_size:
                total_full_lines += 1

        return total_full_lines
