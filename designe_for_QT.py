import sys
from All_Functions import *
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.png_map = 'image.jpeg'
        self.z = 15
        self.ll = '92.888506,56.009354'
        uic.loadUi('main_design_Ui.ui', self)  # Загружаем дизайн
        self.initUi()

    def initUi(self):
        self.up_btn.clicked.connect(self.up)
        self.down_btn.clicked.connect(self.down)
        self.left_btn.clicked.connect(self.left)
        self.right_btn.clicked.connect(self.right)
        self.minus_btn.clicked.connect(self.zoom_out)
        self.plus_btn.clicked.connect(self.zoom_in)
        self.show_map()


    def show_map(self):
        open_image(self.ll, str(self.z), self.png_map)
        pixmap = QPixmap(self.png_map)
        self.label.setPixmap(pixmap)

    def movement(self):
        if self.sender() == self.up_btn or event.key() == Qt.Key_Up:
            pass
        elif self.sender() == self.down_btn or event.key() == Qt.Key_Down:
            pass
        elif self.sender() == self.right_btn or event.key() == Qt.Key_Left:
            pass
        elif self.sender() == self.left_btn or event.key() == Qt.Key_Right:
            pass

    def zoom(self):
        if self.sender() == self.minus_btn or event.key() == Qt.Key_PageDown:
            if self.z - 1 < 0:
                return None
            self.z -= 1
        else:
            if self.z + 1 > 17:
                return None
            self.z += 1
        self.show_map()

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
            self.zoom()
        elif event.key() == Qt.Key_PageDown:
            self.zoom()
        elif event.key() == Qt.Key_Escape:
            sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())