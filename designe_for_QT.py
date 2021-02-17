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
        # верхний порог 90
        self.spn = 0.0005
        self.coeff = 2
        self.color = 'pm2blm'
        # сначала долгота, потом широта
        self.ll = [92.888506,56.009354]
        self.type_of_map = 'sat'
        uic.loadUi('main_design_Ui.ui', self)  # Загружаем дизайн
        self.initUi()

    def initUi(self):
        self.up_btn.clicked.connect(self.movement)
        self.down_btn.clicked.connect(self.movement)
        self.left_btn.clicked.connect(self.movement)
        self.right_btn.clicked.connect(self.movement)
        self.minus_btn.clicked.connect(lambda x: self.zoom(-1))
        self.plus_btn.clicked.connect(lambda x: self.zoom(1))
        self.hybrid.clicked.connect(lambda x: self.changing_type_of_map('skl'))
        self.scheme.clicked.connect(lambda x: self.changing_type_of_map('map'))
        self.sputnik.clicked.connect(lambda x: self.changing_type_of_map('sat'))
        self.find_address.clicked.connect(self.get_ll)
        self.show_map()

    def changing_type_of_map(self, type):
        self.type_of_map = type
        self.show_map()

    def get_ll(self):
        ll, spn = get_ll_span(self.address.text())
        if ll is None:
            return 0
        self.ll = list(map(float, ll.split(',')))
        self.spn = max(list(map(float, spn.split(','))))
        self.show_map()

    def show_map(self):
        open_image( f'{self.ll[0]},{self.ll[1]}', f'{self.spn},{self.spn}', self.png_map, mode=self.type_of_map, points=[f'{self.ll[0]},{self.ll[1]},{self.color}'])
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

    def zoom(self, x):
        if x == -1:
            self.spn = self.spn * self.coeff
        else:
            self.spn = self.spn / self.coeff
        self.show_map()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.movement()
        elif event.key() == Qt.Key_Down:
            self.movement()
        elif event.key() == Qt.Key_Left:
            self.movement()
        elif event.key() == Qt.Key_Right:
            self.movement()
        elif event.key() == Qt.Key_PageUp:
            self.zoom(1)
        elif event.key() == Qt.Key_PageDown:
            self.zoom(-1)
        elif event.key() == Qt.Key_Escape:
            sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())