import sys
from pprint import pprint

import requests

import mapstatic as ms
from scalmap import selection_scale

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QApplication, QMainWindow


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


class MyLineEdit(QLineEdit):
    def __init__(self, *a, **b):
        super(MyLineEdit, self).__init__(*a, **b)

    def keyPressEvent(self, event) -> None:
        keyPressEvent(ex, event)
        super(MyLineEdit, self).keyPressEvent(event)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(800, 600)
        MainWindow.setTabletTracking(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.search = QtWidgets.QPushButton(self.centralwidget)
        self.search.setObjectName("search")
        self.gridLayout.addWidget(self.search, 2, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.toponym_to_find = MyLineEdit(self.centralwidget)
        self.toponym_to_find.setEnabled(False)
        self.toponym_to_find.setMouseTracking(False)
        self.toponym_to_find.setTabletTracking(False)
        self.toponym_to_find.setToolTip("")
        self.toponym_to_find.setStatusTip("")
        self.toponym_to_find.setWhatsThis("")
        self.toponym_to_find.setAccessibleName("")
        self.toponym_to_find.setAutoFillBackground(False)
        self.toponym_to_find.setInputMethodHints(QtCore.Qt.ImhNone)
        self.toponym_to_find.setText("")
        self.toponym_to_find.setFrame(True)
        self.toponym_to_find.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.toponym_to_find.setDragEnabled(False)
        self.toponym_to_find.setReadOnly(False)
        self.toponym_to_find.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.toponym_to_find.setClearButtonEnabled(True)
        self.toponym_to_find.setObjectName("toponym_to_find")
        self.gridLayout.addWidget(self.toponym_to_find, 2, 1, 1, 1)
        self.ful_path = QtWidgets.QLabel(self.centralwidget)
        self.ful_path.setText("")
        self.ful_path.setObjectName("ful_path")
        self.gridLayout.addWidget(self.ful_path, 4, 1, 1, 2)
        self.img = QtWidgets.QLabel(self.centralwidget)
        self.img.setTabletTracking(False)
        self.img.setInputMethodHints(QtCore.Qt.ImhNone)
        self.img.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextEditable)
        self.img.setObjectName("img")
        self.gridLayout.addWidget(self.img, 0, 0, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 3, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.search.setText(_translate("MainWindow", "Искать"))
        self.img.setText(_translate("MainWindow", "TextLabel"))
        self.checkBox.setText(_translate("MainWindow", "Отображать почтовый индекс"))


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # uic.loadUi('main.ui', self)
        self.setupUi(self)

        self.z = 10
        self.x, self.y = .0, .0

        self.pt = None

        self.map_type = ['map', 'sat', 'sat,skl']

        self.update_img()

        self.toponym_to_find.setEnabled(True)

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
            try:
                # self.toponym_to_find.setEnabled(True)

                self.toponym_to_find.setText('')
                self.ful_path.setText('')

                self.search.setText(text_for_enabled)
                self.pt = None
            except Exception as e:
                print(e)
        else:
            try:
                response = requests.get(
                    "http://geocode-maps.yandex.ru/1.x/",
                    params={
                        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                        "geocode": self.toponym_to_find.text(),
                        "format": "json"
                    }
                ).json()

                postal_code = ''
                if self.checkBox.isChecked():
                    postal_code = '\nПочтовый индекс: ' + response['response']['GeoObjectCollection'
                    ]['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData'
                    ]['Address'].get('postal_code', '---')

                self.x, self.y = map(float, selection_scale(response))
                self.z = .001  # Чтобы было видно

                self.pt = ','.join(map(str, (self.x, self.y, 'flag')))

                self.ful_path.setText('Адрес: ' + response['response']['GeoObjectCollection'][
                    'featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['AddressDetails'][
                    'Country']['AddressLine'] + postal_code)
            except Exception as e:
                print(e, '----')
                self.pt = None

            # self.toponym_to_find.setEnabled(False)
            # self.search.setText('Сброс поискового результата')

        self.update_img()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
