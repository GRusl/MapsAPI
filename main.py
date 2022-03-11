import sys

import mapstatic as ms

from PIL import Image

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        Image.open(ms.get_img({'ll': '0.0,0.0', 'z': '16'})).save('map.png')

        pixmap = QPixmap('map.png')

        self.img.setFixedSize(pixmap.width(), pixmap.height())
        self.img.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
