import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPen, QColor, QPainter
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QAction, QApplication

from game.game_logic import GameField
from gui.rules_window import Rules
from models.data_models import Color, CELL_SIZE
from gui.settings_window import Settings

FIELD_SIZE = 5

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        print("Initializing Game Window...")
        self.init_ui()
        from PyQt5.QtWidgets import QGraphicsDropShadowEffect
        from PyQt5.QtGui import QColor

        self.shuffle_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ff0000;
                    color: #000000;
                    border-radius: 10px;
                    padding: 10px;
                    min-width: 200px;
                }
                QPushButton:hover {
                    background-color: #ffff00;
                }
                QPushButton:pressed {
                    background-color: #a3a3a3;
                }
            """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(5)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 50))

        self.shuffle_btn.setGraphicsEffect(shadow)

    def init_ui(self):
        print("Setting up UI...")
        self.setWindowTitle("Kvadroteka")
        self.setGeometry(100, 100, 900, 600)

        # Создание и настройка виджета для отображения количества шагов
        self.steps = 0
        self.step_counter = QLabel(f"Steps: {self.steps}", self)
        self.step_counter.setGeometry(150 + CELL_SIZE * FIELD_SIZE, 350, 200, 50)
        self.step_counter.setFont(QFont("Times New Roman", 20))

        # Создание кнопки для перемешивания поля
        self.shuffle_btn = QPushButton('Shuffle', self)
        self.shuffle_btn.setGeometry(150 + CELL_SIZE * FIELD_SIZE, 150, 100, 50)
        self.shuffle_btn.setFont(QFont("Times New Roman", 20))
        self.shuffle_btn.clicked.connect(self.shuffle_btn_clicked)

        # Создание игрового поля и начальное определение количества полных линий
        self.field = GameField(FIELD_SIZE)
        self.rows = self.field.check_rows()
        self.counter = QLabel(f"Rows: {self.rows}", self)
        self.counter.setGeometry(150 + CELL_SIZE * FIELD_SIZE, 250, 200, 50)
        self.counter.setFont(QFont("Times New Roman", 20))

        # Метка, показывающая сообщение о победе
        self.win_label = QLabel("Вы выиграли!", self)
        self.win_label.setGeometry(100, CELL_SIZE * FIELD_SIZE + 100, 500, 200)
        self.win_label.setFont(QFont("Times New Roman", 36))
        self.win_label.setVisible(False)

        self.init_menu()

    def init_menu(self):
        main_menu = self.menuBar()
        # Добавление действия "Правила"
        rules_action = QAction('Rules', self)
        rules_action.triggered.connect(self.rules_click)
        main_menu.addAction(rules_action)
        # Добавление действия "Настройки"
        settings_action = QAction('Settings', self)
        settings_action.triggered.connect(self.settings_click)
        main_menu.addAction(settings_action)
        # Добавление действия "Выход"
        quit_action = QAction('Exit', self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        main_menu.addAction(quit_action)
        # Создание окон правил и настроек
        self.rules = Rules()
        self.settings = Settings(on_settings_change=self.handle_settings_change)

    def rules_click(self): # Отображение окна с правилами игры
        self.rules.show()

    def settings_click(self): # Отображение окна настроек
        self.settings.show()

    def handle_settings_change(self, new_size):  # Обработка изменения настроек размера поля
        try:
            global FIELD_SIZE
            FIELD_SIZE = int(new_size)
            print("Updating field size to:", FIELD_SIZE)

            self.field = GameField(FIELD_SIZE)
            self.steps = 0 # Обновление поля с новым размером
            self.win_label.setVisible(False)  # Скрываем сообщение о победе
            # Обновление размеров и позиций элементов интерфейса
            margin_horizontal = 300
            margin_vertical = 200
            new_width = 100 + CELL_SIZE * FIELD_SIZE + margin_horizontal
            new_height = 100 + CELL_SIZE * FIELD_SIZE + margin_vertical

            self.setGeometry(100, 100, new_width, new_height)

            offset_x = 150 + CELL_SIZE * FIELD_SIZE
            self.counter.setGeometry(offset_x, 250, 200, 50)
            self.step_counter.setGeometry(offset_x, 350, 200, 50)
            self.shuffle_btn.setGeometry(offset_x, 150, 100, 50)
            self.win_label.setGeometry(100, CELL_SIZE * FIELD_SIZE + 100, 500, 200)

            self.update_display()
        except Exception as e:
            print("Error in handle_settings_change:", e)

    def keyPressEvent(self, event):  # Обработка нажатий клавиш для управления игрой
        key = event.key()
        moved = False
        if key == Qt.Key_L:
            self.field.rotate()
            self.steps += 1
            moved = True
        elif key == Qt.Key_K:
            self.field.reverse_rotate()
            self.steps += 1
            moved = True
        if key in [Qt.Key_W, Qt.Key_S, Qt.Key_A, Qt.Key_D]: # Если нажата клавиша перемещения
            self.update_movement_keys(key) # Обновляем позицию рамки на поле
            moved = True
        if moved:
            self.update_display()

    def update_movement_keys(self, key): # Обновление позиции рамки на поле
        if self.rows == FIELD_SIZE:  # Если игрок выиграл, не обновляем позицию рамки
            return
        if key == Qt.Key_W and self.field.frame.i > 0:
            self.field.frame.i -= 1
        elif key == Qt.Key_S and self.field.frame.i < FIELD_SIZE - 3:
            self.field.frame.i += 1
        elif key == Qt.Key_A and self.field.frame.j > 0:
            self.field.frame.j -= 1
        elif key == Qt.Key_D and self.field.frame.j < FIELD_SIZE - 3:
            self.field.frame.j += 1

    def shuffle_btn_clicked(self): # Обработка нажатия кнопки перемешивания
        self.field.shuffle()
        self.update_display()

    def update_display(self): # Обновление отображения игрового поля
        self.rows = self.field.check_rows()
        self.counter.setText(f"Rows: {self.rows}")
        self.step_counter.setText(f"Steps: {self.steps}")
        if self.rows == FIELD_SIZE:
            self.win_label.setVisible(True)
        self.update()

    def paintEvent(self, event): # Отрисовка игрового поля
        try:
            painter = QPainter(self)
            self.draw_field(painter)
            self.draw_frame(painter)
            painter.end()
            print("Field painted successfully")
        except Exception as e:
            print("Error during painting:", e)

    def draw_frame(self, painter): # Отрисовка рамки на игровом поле
        pen = QPen(QColor(255, 255, 255))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        frame_i = self.field.frame.i
        frame_j = self.field.frame.j
        frame_x = 100 + CELL_SIZE // 2 + frame_j * CELL_SIZE
        frame_y = 100 + CELL_SIZE // 2 + frame_i * CELL_SIZE
        frame_width = CELL_SIZE * 2
        frame_height = CELL_SIZE * 2
        painter.drawRect(frame_x, frame_y, frame_width, frame_height)
        circle_radius = 5
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(frame_x - circle_radius, frame_y - circle_radius, circle_radius * 2, circle_radius * 2)
        painter.drawEllipse(frame_x + frame_width - circle_radius, frame_y - circle_radius, circle_radius * 2,
                            circle_radius * 2)
        painter.drawEllipse(frame_x - circle_radius, frame_y + frame_height - circle_radius, circle_radius * 2,
                            circle_radius * 2)
        painter.drawEllipse(frame_x + frame_width - circle_radius, frame_y + frame_height - circle_radius,
                            circle_radius * 2, circle_radius * 2)

    def draw_field(self, painter): # Отрисовка ячеек на игровом поле
        radius = 10
        shadow_offset = 5
        shadow_color = QColor(50, 50, 50, 100)

        for i in range(FIELD_SIZE):
            for j in range(FIELD_SIZE):
                cell = self.field.field[i][j]
                base_color = QColor(255, 0, 0) if cell.color == Color.RED else QColor(255, 255, 0)

                # Рисование тени
                painter.setBrush(shadow_color)
                painter.drawRoundedRect(
                    100 + j * CELL_SIZE + shadow_offset,
                    100 + i * CELL_SIZE + shadow_offset,
                    cell.size, cell.size,
                    radius, radius
                )

                # Рисование самой ячейки
                painter.setBrush(base_color)
                painter.drawRoundedRect(
                    100 + j * CELL_SIZE,
                    100 + i * CELL_SIZE,
                    cell.size, cell.size,
                    radius, radius
                )



if __name__ == '__main__':
    print("Starting application...")
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    print("Entering main loop...")
    sys.exit(app.exec_())