import sys
from PyQt5.QtWidgets import QApplication
from gui.game_window import GameWindow

if __name__ == '__main__':
    """
            Тут просто запуск главного окна игры 
    """
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec_())