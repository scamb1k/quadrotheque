from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QTextBrowser

class Rules(QMainWindow):
    """
            Здесь просто инициализация окна с правилами игры в виде html-страницы
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rules")
        self.setGeometry(200, 200, 700, 400)

        self.text_browser = QTextBrowser(self)
        self.text_browser.setGeometry(0, 0, 700, 400)
        self.text_browser.setFont(QFont("Times New Roman", 14))

        html_content = """
        <html>
        <head>
        <title>Game Rules</title>
        </head>
        <body>
        <h1>Game Rules</h1>
        <p>Kvadroteka - это головоломка, в которой необходимо собрать кубики одного цвета в одной линии</p>
        <p>Используйте  <b>W</b>, <b>A</b>, <b>S</b>, <b>D</b> клавиши для перемещения белой квадратной рамки</p>
        <p>Используйте <b>K</b> и <b>L</b> клавиши для вращения кубиков внутри рамки по часовой стрелке и против часовой стрелки</p>
        <p>Нажмите <b>Shuffle</b> чтобы перетасовать кубики</p>
        </body>
        </html>
        """

        self.text_browser.setHtml(html_content)
