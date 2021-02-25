import sys
from All_Functions import *
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
import time
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
        self.color2 = 'pm2grm'
        # сначала долгота, потом широта
        self.ll = list(self.DEF_LL)
        self.points = []
        self.type_of_map = 'sat'
        self.image = (50, 10, 450, 450)
        self.img_centre = (self.image[0] + self.image[2]) // 2, (self.image[1] + self.image[3]) // 2
        # print(self.img_centre)
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

        # self.task = TaskThread()
        #
        # #
        # self.find_address.clicked.connect(self.onStart)
        # self.progressBar.setRange(0, 1)
        # self.task = TaskThread(self)
        # # self.myLongTask = TaskThread()
        # self.task.taskFinished.connect(self.onFinished)
        # #

    def start_progress_bar(self):
        self.progressBar.setRange(0, 0)

    def finish_progress_bar(self):
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(100)

    def reset(self):
        self.points = []
        self.statusbar.showMessage('')
        self.show_map()

    def changing_type_of_map(self, type):
        self.type_of_map = type
        self.show_map()

    def get_ll(self):
        self.start_progress_bar()
        # self.task.start()
        ll, spn, address = get_ll_span(self.address.text())
        if ll is None:
            self.statusbar.showMessage('Адрес не найден')
            return 0

        # показываем карту
        self.ll = list(map(float, ll.split(',')))
        self.spn = max(list(map(float, spn.split(','))))
        self.points = [f'{self.ll[0]},{self.ll[1]},{self.color}']
        self.show_map(start=False)

        # выводим адресс
        # pprint.pprint(toponym)
        try:
            self.statusbar.showMessage(address['formatted'])
        except Exception:
            self.statusbar.showMessage(f'{self.ll[1]}широты,{self.ll[0]}долготы')
        # self.task.
        # QtCore.pyqtSignal().emit()
        # self.task.taskFinished.emit()

    def show_map(self, start=True):
        if start:
            self.start_progress_bar()
        open_image(f'{self.ll[0]},{self.ll[1]}', f'{self.spn},{self.spn}', self.png_map, mode=self.type_of_map,
                   points=self.points)
        pixmap = QPixmap(self.png_map)
        # print('size', pixmap.size())
        # print('xy', self.label.x(), self.label.y())
        # print('-' * 10)
        self.label.setPixmap(pixmap)

        # print(self.ll, self.obj_ll, sep='\n')
        # print('showing', self.ll)
        self.finish_progress_bar()

    def movement(self, dir):
        # 0 элемент - вправо, влево
        # 1 элемент - вверх, вниз
        # print(longtitude_offset(self.ll, self.spn * 2))
        self.ll[0] += dir[0] * self.spn * 2
        self.ll[1] += dir[1] * self.spn * 2
        # self.ll = longtitude_offset(self.ll, self.spn * 2)
        # print(self.ll)
        self.show_map()

    def zoom(self, x):
        if x == -1:
            self.spn = min(self.spn * self.coeff, 90)
        else:
            # todo: find max spn
            self.spn = max(self.spn / self.coeff, 0.000000001)
        self.show_map()

    def longlat_by_mousepos(self, x, y):
        degrees_per_pixel_x = (self.spn / self.image[2])
        degrees_per_pixel_y = (self.spn / self.image[3])
        # print('*' * 10)
        # print(degrees_per_pixel_x, degrees_per_pixel_y)
        # print(degrees_per_pixel)
        # print('mxmy', x, y)
        # print('m_x, m_y', x, y)
        # print('old')
        # print('x', (x - self.img_centre[0]))
        # print('y', -(y - self.img_centre[1]))
        # print('new')
        # print('x', x - self.image[0] - self.img_centre[0])
        # print('y', y - self.image[1] - self.img_centre[1])
        new_x, new_y = x - self.image[0] - self.img_centre[0], -(y - self.image[1] - self.img_centre[1])
        ll_offset = [new_x * degrees_per_pixel_x, new_y * degrees_per_pixel_y]
        # ll_offset[0] = 0
        # print(ll_offset)
        # print('spn', self.spn)
        #
        # print('*' * 10)
        # print(ll_offset)
        # ll_offset = longtitude_offset(self.ll, ll_offset[0])
        ##########
        # a_lat = self.ll[1]
        # b_lat = self.ll[1] + (self.image[2] // 2 * pixels_per_degree)
        # print('a and b', a_lat, b_lat)
        # radiance_lattitude = math.radians((a_lat + b_lat) / 2)
        # print(1)
        # lat_lon_factor = math.cos(radiance_lattitude)
        # print(2)
        # print(ll_offset[0])
        # print(lat_lon_factor)
        # ll_offset[0] = ll_offset[0] * lat_lon_factor
        # print(3)
        #
        # ##########
        # print(self.spn)
        # print(pixels_per_degree)
        # print(img_centre)
        # print('ll', self.ll)
        # print(ll_offset)
        #
        # 92.888549, 56.009220
        # 92.885234, 56.009190
        #
        return self.ll[0] + ll_offset[0], self.ll[1] + ll_offset[1]
        # return self.ll[0] + ll_offset[0], self.ll[1] + ll_offset[1]

    def mousePressEvent(self, event):
        left = event.button() == Qt.LeftButton
        right = event.button() == Qt.RightButton
        if left or right:
            x, y = event.x(), event.y()
            print('fasfasd', self.image[2] + self.image[0])
            if self.image[0] <= x <= self.image[2] + self.image[0] and self.image[1] <= y <= self.image[3] + self.image[
                1]:
                ll = self.longlat_by_mousepos(x, y)
                if left:
                    self.points = [f'{ll[0]},{ll[1]},{self.color}',
                                   f'{self.ll[0]},{self.ll[1]},{self.color2}']
                    # address = geocode(ll)
                    # print(address)
                    # self.statusbar.showMessage(address['formatted'])
                    self.show_map()
                elif right:
                    pass
        # if event.button() == Qt.LeftButton:
        #     x, y = event.x(), event.y()
        #     # print('first', x, y)
        #     if x in range(self.image[0], self.image[2] + self.image[0]) and y in range(self.image[1],
        #                                                                                self.image[3] + self.image[1]):
        #         # image_x = x - self.image[0]
        #         # image_y = y - self.image[1]
        #         ### delete
        #         # x = 10
        #         # y = 305
        #         ###
        #         # print('second', image_x, image_y)
        #         click_ll = self.longlat_by_mousepos(x, y)
        #         # print('click_ll:', click_ll)
        #         # print('self.ll:', self.ll)
        #         # print('-' * 25)
        #         self.points = [f'{click_ll[0]},{click_ll[1]},{self.color}', f'{self.ll[0]},{self.ll[1]},{self.color2}']
        #         self.show_map()
        # elif event.button() == Qt.RightButton():
        #     x, y = event.x(), event.y()
        #     if self.image[0] <= x <= self.image[2] + self.image[0] and self.image[1] <= y <= self.image[3] + self.image[1]:
        #         ll = self.longlat_by_mousepos(x, y)

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

    # def onStart(self):
    #     print(1)
    #     self.progressBar.setRange(0, 0)
    #     self.task.start()
    #     print(2)
    #
    # def onFinished(self):
    #     # Stop the pulsation
    #     self.progressBar.setRange(0, 100)
    #     self.progressBar.setValue(100)
    #     print(7)
    #     print()


# class TaskThread(QtCore.QThread):
#     taskFinished = QtCore.pyqtSignal()
#
#     def __init__(self, window):
#         super().__init__()
#         self.window = window
#
#     def run(self):
#         try:
#             print(4)
#             self.window.get_ll()
#             print(5)
#             self.taskFinished.emit()
#             print(6)
#         except Exception as e:
#             print(e)
#

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
