from all_functions import *
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class MyWidget(QMainWindow):
    DEF_LL = (92.888506, 56.009354)
    LAT_STEP = 0.008  # Шаги при движении карты по широте и долготе
    LON_STEP = 0.02
    MOVE_Z = 15
    COORD_TO_GEO_X = 0.0000428  # Пропорции пиксельных и географических координат.
    COORD_TO_GEO_Y = 0.0000428
    Z_MAX = 17
    Z_MIN = 2
    # spn = 50(метров) / degree_to_meters_factor
    # degree_to_meters_factor = 111 * 1000
    BUSINESS_SEARCH_SPN = '0.00045,0.00045'

    def __init__(self):
        super().__init__()
        self.png_map = 'image.jpeg'
        # верхний порог 90
        self.z = 15
        # self.spn = 0.0005
        # self.coeff = 2
        self.color = 'pm2blm'
        self.color2 = 'pm2grm'
        # сначала долгота, потом широта
        self.ll = list(self.DEF_LL)
        self.points = []
        self.type_of_map = 'sat'
        self.image = (50, 10, 450, 450)
        self.img_centre = self.image[0] + (self.image[2]) // 2, self.image[1] + (self.image[3]) // 2
        uic.loadUi('main_design.ui', self)  # Загружаем дизайн
        self.initUi()

    def initUi(self):
        self.up_btn.clicked.connect(lambda x: self.movement((0, 1)))
        self.down_btn.clicked.connect(lambda x: self.movement((0, -1)))
        self.right_btn.clicked.connect(lambda x: self.movement((1, 0)))
        self.left_btn.clicked.connect(lambda x: self.movement((-1, 0)))

        self.minus_btn.clicked.connect(lambda x: self.zoom(-1))
        self.plus_btn.clicked.connect(lambda x: self.zoom(1))
        self.reset_btn.clicked.connect(self.reset_button)

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

    def reset_button(self):
        self.points = []
        self.address.setText('')
        self.statusbar.showMessage('')
        self.show_map()

    def reset(self):
        self.points = []
        self.statusbar.showMessage('')
        self.index_chb.setChecked(False)

    def changing_type_of_map(self, type):
        self.type_of_map = type
        self.show_map()

    def get_ll(self):
        if not self.address.text():
            return -1
        self.start_progress_bar()
        if not any(filter(str.isalpha, self.address.text())):
            self.statusbar.showMessage('Пожалуйста, попробуйте ввести адерс, содержащий буквы,' +
                                       'и нажмите на кнопку "Найти адрес"')
            self.finish_progress_bar()
            return -1
        try:
            ll, address = get_longlat(self.address.text())
            if ll is None:
                self.statusbar.showMessage('Адрес не найден')
                self.finish_progress_bar()
                return -1
        except Exception:
            self.statusbar.showMessage('Адрес не найден')
            self.finish_progress_bar()
            return -1

        # показываем карту
        self.ll = list(map(float, ll.split(',')))
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
        # 83.618125, -32.856152
        img_opened = open_image(f'{self.ll[0]},{self.ll[1]}', self.z, self.png_map, points=self.points,
                                mode=self.type_of_map)
        self.z = self.z if not img_opened else img_opened
        # open_image(f'{self.ll[0]},{self.ll[1]}', self.z, self.png_map, points=self.points, mode=self.type_of_map)
        pixmap = QPixmap(self.png_map)
        self.label.setPixmap(pixmap)
        self.finish_progress_bar()

    def movement(self, dirr):
        # TODO: работает тольок для больших z
        delta_z = self.MOVE_Z - self.z
        multiplier = pow(2, delta_z)
        # print(multiplier, 'multiplier')
        long_offset = self.LON_STEP * multiplier
        lat_offset = self.LAT_STEP * multiplier
        self.ll[0] += dirr[0] * long_offset
        self.ll[1] += dirr[1] * lat_offset
        if dirr[0] < 0:
            self.ll[0] = max(-180, self.ll[0])
        elif dirr[0] > 0:
            self.ll[0] = min(180, self.ll[0])
        if dirr[1] < 0:
            self.ll[1] = max(-80, self.ll[1])
        elif dirr[1] > 0:
            self.ll[1] = min(80, self.ll[1])
        self.show_map()

    def zoom(self, x):
        if x == 1:
            new_z = min(self.z + x, self.Z_MAX)
        else:
            new_z = max(self.z + x, self.Z_MIN)
        if new_z != self.z:
            self.z = new_z
            self.show_map()
        # if self.Z_MIN < self.z < self.Z_MAX:
        #     self.z += x
        # if x == -1:
        #     self.z = min(self.spn * self.coeff, 90)
        # else:
        #     self.spn = max(self.spn / self.coeff, 0.000000001)

    def screen_to_geo(self, x, y):
        delta_x, delta_y = x - self.img_centre[0], -(y - self.img_centre[1])
        lx = self.ll[0] + delta_x * self.COORD_TO_GEO_X * math.pow(2, 15 - self.z)
        ly = self.ll[1] + delta_y * self.COORD_TO_GEO_Y * math.cos(math.radians(self.ll[1])) * math.pow(2, 15 - self.z)
        return lx, ly

    def mousePressEvent(self, event):
        left = event.button() == Qt.LeftButton
        right = event.button() == Qt.RightButton
        if left or right:
            x, y = event.x(), event.y()
            if self.image[0] <= x <= self.image[2] + self.image[0] and self.image[1] <= y <= self.image[3] + self.image[
                1]:
                self.start_progress_bar()
                self.reset()
                ll = self.screen_to_geo(x, y)
                address = geocode(f'{ll[0]},{ll[1]}')
                self.points = [f'{ll[0]},{ll[1]},{self.color}']
                message = ''
                if left:
                    if address:
                        message = address['metaDataProperty']['GeocoderMetaData']['Address']['formatted']
                    else:
                        message = 'Адрес объекта не найден'
                elif right:
                    if address:
                        address = address['metaDataProperty']['GeocoderMetaData']['Address']['formatted']
                    try:
                        businesses = find_businesses(address, f'{ll[0]},{ll[1]}', self.BUSINESS_SEARCH_SPN)
                        closest = in_50_metres_range(ll, businesses)
                        if closest:
                            message = f'"{closest[0]}", организация обозначена серой меткой'
                            self.points = [f'{ll[0]},{ll[1]},{self.color}',
                                           f'{closest[1][0]},{closest[1][1]},{self.color2}']
                        else:
                            message = 'Организация в диапазоне 50 метров не найдена'
                    except Exception:
                        message = 'Организация не найдена'
                self.statusbar.showMessage(message)
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
