from all_functions import *
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class MyWidget(QMainWindow):
    DEF_LL = (92.888506, 56.009354)

    def __init__(self):
        super().__init__()
        self.png_map = 'image.jpeg'
        # верхний порог 90
        self.spn = 0.0005
        self.coeff = 2
        self.color = 'pm2blm'
        self.color2 = 'pm2grm'
        # сначала долгота, потом широта
        self.ll = list(self.DEF_LL)
        self.points = []
        self.type_of_map = 'sat'
        self.image = (50, 10, 450, 450)
        self.img_centre = (self.image[0] + self.image[2]) // 2, (self.image[1] + self.image[3]) // 2
        uic.loadUi('main_design.ui', self)  # Загружаем дизайн
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

    def start_progress_bar(self):
        self.progressBar.setRange(0, 0)

    def finish_progress_bar(self):
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(100)

    def reset(self):
        self.points = []
        self.statusbar.showMessage('')
        self.index_chb.setChecked(False)

    def changing_type_of_map(self, type):
        self.type_of_map = type
        self.show_map()

    def get_ll(self):
        self.start_progress_bar()
        # self.task.start()
        ll, spn, address = get_ll_span(self.address.text())
        if ll is None:
            self.statusbar.showMessage('Адрес не найден')
            self.finish_progress_bar()
            return 0

        # показываем карту
        self.ll = list(map(float, ll.split(',')))
        self.spn = max(list(map(float, spn.split(','))))
        self.points = [f'{self.ll[0]},{self.ll[1]},{self.color}']
        self.show_map(start=False)

        # выводим адрес
        try:
            message = address['formatted']
        except Exception:
            message = f'Данный адрес не найден, {self.ll[1]}широта,{self.ll[0]}долгота'
        if self.index_chb.isChecked():
            try:
                index = address['postal_code']
                message += f', индеск {index}'
            except Exception:
                message += ', индекс не найден'
        self.statusBar().showMessage(message)

    def show_map(self, start=True):
        if start:
            self.start_progress_bar()
        open_image(f'{self.ll[0]},{self.ll[1]}', f'{self.spn},{self.spn}', self.png_map, mode=self.type_of_map,
                   points=self.points)
        pixmap = QPixmap(self.png_map)
        self.label.setPixmap(pixmap)
        self.finish_progress_bar()

    def movement(self, dir):
        # 0 элемент - вправо, влево
        # 1 элемент - вверх, вниз
        self.ll[0] += dir[0] * self.spn * 2
        self.ll[1] += dir[1] * self.spn * 2
        self.show_map()

    def zoom(self, x):
        if x == -1:
            self.spn = min(self.spn * self.coeff, 90)
        else:
            self.spn = max(self.spn / self.coeff, 0.000000001)
        self.show_map()

    def longlat_by_mousepos(self, x, y):
        degrees_per_pixel_x = (self.spn / self.image[2])
        degrees_per_pixel_y = (self.spn / self.image[3])
        new_x, new_y = x - self.image[0] - self.img_centre[0], -(y - self.image[1] - self.img_centre[1])
        ll_offset = [new_x * degrees_per_pixel_x, new_y * degrees_per_pixel_y]
        return self.ll[0] + ll_offset[0], self.ll[1] + ll_offset[1]

    def mousePressEvent(self, event):
        left = event.button() == Qt.LeftButton
        right = event.button() == Qt.RightButton
        if left or right:
            x, y = event.x(), event.y()
            if self.image[0] <= x <= self.image[2] + self.image[0] and self.image[1] <= y <= self.image[3] + self.image[
                1]:
                self.start_progress_bar()
                self.reset()
                ll = self.longlat_by_mousepos(x, y)
                address = geocode(f'{ll[0]},{ll[1]}')
                if left:
                    self.points = [f'{ll[0]},{ll[1]},{self.color}']
                    if address:
                        address = address['metaDataProperty']['GeocoderMetaData']['Address']['formatted']
                    else:
                        address = 'Адрес объекта не найден'
                    self.statusbar.showMessage(address)
                elif right:
                    if address:
                        address = address['metaDataProperty']['GeocoderMetaData']['Address']['formatted']
                    try:
                        businesses = find_businesses(address, f'{ll[0]},{ll[1]}', '0.0015,0.0015')
                        closest = in_50_metres_range(ll, businesses)
                        if closest:
                            self.statusbar.showMessage(closest[0])
                            self.points = [f'{ll[0]},{ll[1]},{self.color}',
                                           f'{closest[1][0]},{closest[1][1]},{self.color2}']
                        else:
                            self.statusbar.showMessage('Организация в диапазоне 50 метров не найдена')
                    except Exception as e:
                        self.statusbar.showMessage('Организация не найдена')
            self.show_map(start=False)

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


# class TaskThread(QtCore.QThread):
#     taskFinished = QtCore.pyqtSignal()
#
#     def run(self):
#         time.sleep(3)
#         self.taskFinished.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
