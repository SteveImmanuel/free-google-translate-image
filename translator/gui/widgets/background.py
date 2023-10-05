import typing
from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton
from PyQt6.QtGui import QMouseEvent, QKeyEvent, QPaintEvent, QRegion


class Background(QWidget):

    def __init__(self, width: int, height: int, tl: QtCore.QPoint, br: QtCore.QPoint):
        super().__init__()
        self.width = width
        self.height = height
        self.tl = tl
        self.br = br
        self._setup_ui()

    def _setup_ui(self):
        self.setFixedSize(self.width, self.height)

        self.r1 = QWidget(self)
        self.r2 = QWidget(self)
        self.r3 = QWidget(self)
        self.r4 = QWidget(self)
        self.r1.setStyleSheet('background-color: red;')
        self.r2.setStyleSheet('background-color: red;')
        self.r3.setStyleSheet('background-color: red;')
        self.r4.setStyleSheet('background-color: red;')

    def update_hole(self, tl: QtCore.QPoint, br: QtCore.QPoint):
        self.r1.setGeometry(0, 0, tl.x(), self.height)
        self.r2.setGeometry(tl.x(), 0, br.x() - tl.x(), tl.y())
        self.r3.setGeometry(br.x(), 0, self.width - br.x(), self.height)
        self.r4.setGeometry(tl.x(), br.y(), br.x() - tl.x(), self.height - br.y())
