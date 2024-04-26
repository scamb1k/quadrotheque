from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout, QRadioButton


class Settings(QMainWindow):
    """
      Дефолт класс Settings - окно настроек. Оно позволяет пользователю выбрать размер игрового поля
      При выборе размера поля вызывается функция on_settings_change, которая обновляет размер поля в главном окне игры"""
    def __init__(self, on_settings_change=None):
        """
               Инициализация окна настроек. Принимает функцию обратного вызова, которая будет вызвана при изменении настроек
               :param on_settings_change: функция, которая будет вызвана при изменении настроек"""
        super().__init__()
        self.radio_buttons = None
        self.on_settings_change = on_settings_change
        self.init_ui()

    def init_ui(self):
        """
               Инициализирует пользовательский интерфейс окна настроек. Создает все необходимые элементы управления.
               Вызывает функцию on_changed при изменении размера поля"""
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 100, 200)

        widget = QWidget(self)
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)

        label = QLabel("Выберите размеры поля:", self)
        label.setFont(QFont("Times New Roman", 12))
        layout.addWidget(label)

        field_sizes = ["5", "6", "7", "8", "9", "10"]
        self.radio_buttons = []
        for size in field_sizes:
            radio_button = QRadioButton(f"{size}x{size}", self)
            radio_button.field_size = size
            radio_button.toggled.connect(self.on_changed)
            layout.addWidget(radio_button)
            self.radio_buttons.append(radio_button)

    def on_changed(self):
        # Обработчик события изменения выбранного размера поля. Вызывает функцию обратного вызова и закрывает окно настроек
        for radio_button in self.radio_buttons:
            if radio_button.isChecked():
                if self.on_settings_change:
                    self.on_settings_change(radio_button.field_size)
                self.close()
                break