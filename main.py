import sys

import requests

import mapstatic as ms
from scalmap import selection_scale

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

        self.pt = None

        self.map_type = ['map', 'sat', 'sat,skl']

        self.update_img()

        self.search.clicked.connect(self.search_fun)

    def update_img(self):
        pixmap = QPixmap()
        img = ms.get_img(
            {
                'll': ','.join(map(str, (self.x, self.y))),
                'spn': ','.join(map(str, [self.z] * 2)),
                'l': self.map_type[0]
            } | ({'pt': self.pt} if self.pt else {})
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

    def search_fun(self):
        text_for_enabled = 'Искать'
        if self.search.text() != text_for_enabled:
            self.toponym_to_find.setEnabled(True)
            self.toponym_to_find.setText('')
            self.search.setText(text_for_enabled)
            self.pt = None
        else:
            try:
                response = requests.get(
                    "http://geocode-maps.yandex.ru/1.x/",
                    params={
                        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                        "geocode": self.toponym_to_find.text(),
                        "format": "json"
                    }
                )

                self.x, self.y = map(float, selection_scale(response))
                self.z = .001  # Чтобы было видно

                self.pt = ','.join(map(str, (self.x, self.y, 'flag')))
            except Exception as e:
                print(e)
                self.pt = None

            self.toponym_to_find.setEnabled(False)
            self.search.setText('Сброс поискового результата')

        self.update_img()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
