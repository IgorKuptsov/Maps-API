import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_design_Ui.ui', self)  # Загружаем дизайн
        self.up_btn.clicked.connect(self.up)
        self.down_btn.clicked.connect(self.down)
        self.left_btn.clicked.connect(self.left)
        self.right_btn.clicked.connect(self.right)
        self.minus_btn.clicked.connect(self.minus)
        self.plus_btn.clicked.connect(self.plus)

    def up(self):
        self.label.setText("up")

    def down(self):
        self.label.setText("down")

    def left(self):
        self.label.setText("left")

    def right(self):
        self.label.setText("right")

    def plus(self):
        self.label.setText("plus")

    def minus(self):
        self.label.setText("minus")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())