import sys

import mapstatic as ms

from PIL import Image

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.z = 16

        self.update_img()

    def update_img(self):
        Image.open(ms.get_img({'ll': '20.0,20.0', 'z': self.z})).save('map.png')

        pixmap = QPixmap('map.png')

        self.img.setFixedSize(pixmap.width(), pixmap.height())
        self.img.setPixmap(pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.z = min(self.z + 1, 17)
        elif event.key() == Qt.Key_Down:
            self.z = max(self.z - 1, 0)

        self.update_img()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
