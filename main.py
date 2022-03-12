import sys

import mapstatic as ms

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.z = 10
        self.x, self.y = .0, .0

        self.map_type = ['map', 'sat', 'sat,skl']

        self.update_img()

    def update_img(self):
        pixmap = QPixmap()
        img = ms.get_img(
            {
                'll': ','.join(map(str, (self.x, self.y))),
                'spn': ','.join(map(str, [self.z] * 2)),
                'l': self.map_type[0]
            }
        ).getvalue()

        if img:
            pixmap.loadFromData(img)

        self.img.setFixedSize(pixmap.width(), pixmap.height())
        self.img.setPixmap(pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Z:
            self.z = min((self.z + 5) // 5 * 5, 20)
        elif event.key() == Qt.Key_X:
            self.z = max(self.z - 5, 1)

        elif event.key() == Qt.Key_Q:
            self.map_type = self.map_type[1:] + [self.map_type[0]]

        elif event.key() == Qt.Key_Right:
            self.x = min(self.x + self.z * 2, 90 - self.z)
        elif event.key() == Qt.Key_Left:
            self.x = max(self.x - self.z * 2, -90 + self.z)

        elif event.key() == Qt.Key_Up:
            self.y = min(self.y + self.z * 2, 90 - self.z)
        elif event.key() == Qt.Key_Down:
            self.y = max(self.y - self.z * 2, -90 + self.z)

        print(self.x, self.y, self.z)

        self.update_img()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
