import sys
from All_Functions import *
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import pprint


class MyWidget(QMainWindow):
    DEF_LL = (92.888506, 56.009354)

    def __init__(self):
        super().__init__()
        self.png_map = 'image.jpeg'
        # верхний порог 90
        self.spn = 0.0005
        self.coeff = 2
        self.color = 'pm2blm'
        # сначала долгота, потом широта
        self.ll = list(self.DEF_LL)
        self.points = []
        self.type_of_map = 'sat'
        uic.loadUi('main_design_Ui.ui', self)  # Загружаем дизайн
        self.initUi()

    def initUi(self):
        self.up_btn.clicked.connect(lambda x: self.movement((0, 1)))
        self.down_btn.clicked.connect(lambda x: self.movement((0, -1)))
        self.right_btn.clicked.connect(lambda x: self.movement((1, 0)))
        self.left_btn.clicked.connect(lambda x: self.movement((-1, 0)))

        self.minus_btn.clicked.connect(lambda x: self.zoom(-1))
        self.plus_btn.clicked.connect(lambda x: self.zoom(1))
        self.reset_btn.clicked.connect(self.reset)

        self.hybrid.clicked.connect(lambda x: self.changing_type_of_map('skl'))
        self.scheme.clicked.connect(lambda x: self.changing_type_of_map('map'))
        self.sputnik.clicked.connect(lambda x: self.changing_type_of_map('sat'))

        self.find_address.clicked.connect(self.get_ll)

        self.show_map()

    def reset(self):
        self.points = []
        self.statusbar.showMessage('')
        self.show_map()

    def changing_type_of_map(self, type):
        self.type_of_map = type
        self.show_map()

    def get_ll(self):
        ll, spn, address = get_ll_span(self.address.text())
        if ll is None:
            self.statusbar.showMessage('Адрес не найден')
            return 0

        # показываем карту
        self.ll = list(map(float, ll.split(',')))
        self.spn = max(list(map(float, spn.split(','))))
        self.points = [f'{self.ll[0]},{self.ll[1]},{self.color}']
        self.show_map()

        # выводим адресс
        # pprint.pprint(toponym)
        try:
            self.statusbar.showMessage(address['formatted'])
        except Exception:
            self.statusbar.showMessage(f'{self.ll[1]}широты,{self.ll[0]}долготы')

    def show_map(self):

        open_image(f'{self.ll[0]},{self.ll[1]}', f'{self.spn},{self.spn}', self.png_map, mode=self.type_of_map,
                   points=self.points)
        pixmap = QPixmap(self.png_map)
        self.label.setPixmap(pixmap)
        # print(self.ll, self.obj_ll, sep='\n')
        # print('showing', self.ll)

    def movement(self, dir):
        # 0 элемент - вправо, влево
        # 1 элемент - вверх, вниз
        # print('before', self.ll)
        self.ll[0] += dir[0] * self.spn * 2
        self.ll[1] += dir[1] * self.spn * 2
        # print('after', self.ll)
        self.show_map()

    def zoom(self, x):
        if x == -1:
            self.spn = min(self.spn * self.coeff, 90)
        else:
            # todo: find max spn
            self.spn = max(self.spn / self.coeff, 0.000000001)
        self.show_map()

    def find(self):
        # self.obj_ll =
        pass

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            print('up')
            self.movement((0, 1))
        elif event.key() == Qt.Key_Down:
            print('down')
            self.movement((0, -1))
        elif event.key() == Qt.Key_Right:
            print('right')
            self.movement((1, 0))
        elif event.key() == Qt.Key_Left:
            print('left')
            self.movement((-1, 0))

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