import sys
import All_Functions
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_design_Ui.ui', self)  # Загружаем дизайн
        self.initUi()

    def initUi(self):
        self.up_btn.clicked.connect(self.up)
        self.down_btn.clicked.connect(self.down)
        self.left_btn.clicked.connect(self.left)
        self.right_btn.clicked.connect(self.right)
        self.minus_btn.clicked.connect(self.zoom_out)
        self.plus_btn.clicked.connect(self.zoom_in)
        pixmap = QPixmap('image.jpeg')
        image.setPixmap(pixmap)

    def up(self):
        All_Functions.up()

    def down(self):
        All_Functions.down()

    def left(self):
        All_Functions.left()

    def right(self):
        All_Functions.right()

    def zoom_in(self):
        All_Functions.zoom_in(self.z)
        self.z += 1

    def zoom_out(self):
        All_Functions.zoom_out(self.z)
        self.z -= 1

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.up()
        elif event.key() == Qt.Key_Down:
            self.down()
        elif event.key() == Qt.Key_Left:
            self.left()
        elif event.key() == Qt.Key_Right:
            self.right()
        elif event.key() == Qt.Key_PageUp:
            self.zoom_in()
        elif event.key() == Qt.Key_PageDown:
            self.zoom_out()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())