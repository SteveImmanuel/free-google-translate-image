from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QPoint, QRect
from PyQt6.QtGui import QKeyEvent, QMouseEvent, QPaintEvent, QRegion
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget

from translator.gui.widgets.circle_button import CircleButton


class RectPoint(QPoint):

    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def connect(self, affect_x: 'RectPoint', affect_y: 'RectPoint'):
        self.affect_x = affect_x
        self.affect_y = affect_y

    @property
    def x(self):
        return super().x()

    @property
    def y(self):
        return super().y()

    @x.setter
    def x(self, x: int):
        self.setX(x)

    @y.setter
    def y(self, y: int):
        self.setY(y)

    def set_point(self, p: QPoint):
        self.setX(p.x())
        self.setY(p.y())
        self.affect_x.setX(p.x())
        self.affect_y.setY(p.y())


class Rectangle:

    def __init__(self, tl: QPoint, br: QPoint):
        self.tl = RectPoint(tl.x(), tl.y())
        self.tr = RectPoint(br.x(), tl.y())
        self.br = RectPoint(br.x(), br.y())
        self.bl = RectPoint(tl.x(), br.y())

        self.tl.connect(self.bl, self.tr)
        self.tr.connect(self.br, self.tl)
        self.br.connect(self.tr, self.bl)
        self.bl.connect(self.tl, self.br)

    def update(self):
        if self.tl.x > self.tr.x or self.bl.x > self.br.x:  # left-right swap
            self.tl, self.tr = self.tr, self.tl
            self.bl, self.br = self.br, self.bl
        if self.tl.y > self.bl.y or self.tr.y > self.br.y:  # top-bottom swap
            self.tl, self.bl = self.bl, self.tl
            self.tr, self.br = self.br, self.tr


class RectController(QWidget):

    def __init__(self, width: int, height: int):
        super().__init__()
        self.setMouseTracking(True)
        self.mouse_on_hold = False
        self.pos1 = QtCore.QPoint()
        self.pos2 = QtCore.QPoint()

        self.rectangle = Rectangle(self.pos1, self.pos2)

        self.w = width
        self.h = height

        self._setup_ui()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.mouse_on_hold = True
        self.pos1 = event.position().toPoint()
        self.pos2 = event.position().toPoint()
        self.update()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.mouse_on_hold:
            self.pos2 = event.position().toPoint()

            self.rectangle.tl.set_point(self.pos1)
            self.rectangle.br.set_point(self.pos2)
            self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        self.rectangle.update()
        self._reposition_buttons()
        self._show_buttons()
        self._paint_hole()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.mouse_on_hold = False
        self.update()

    def _paint_hole(self):
        qp = QtGui.QPainter(self)
        color = QtGui.QColor(0, 0, 0, 100)

        rect_top = QRect(QPoint(0, 0), QPoint(self.w, self.rectangle.tl.y))
        rect_bottom = QRect(QPoint(0, self.rectangle.br.y), QPoint(self.w, self.h))
        rect_left = QRect(QPoint(0, self.rectangle.tl.y + 1), QPoint(self.rectangle.bl.x, self.rectangle.br.y - 1))
        rect_right = QRect(QPoint(self.rectangle.tr.x, self.rectangle.tr.y + 1), QPoint(self.w, self.rectangle.br.y - 1))

        qp.fillRect(rect_top, color)
        qp.fillRect(rect_bottom, color)
        qp.fillRect(rect_left, color)
        qp.fillRect(rect_right, color)

    def _setup_ui(self):
        self.btn_tl = CircleButton(QtCore.Qt.CursorShape.SizeFDiagCursor, self)
        self.btn_tr = CircleButton(QtCore.Qt.CursorShape.SizeBDiagCursor, self)
        self.btn_bl = CircleButton(QtCore.Qt.CursorShape.SizeBDiagCursor, self)
        self.btn_br = CircleButton(QtCore.Qt.CursorShape.SizeFDiagCursor, self)

    def _reposition_buttons(self):
        self.btn_tl.move(self.rectangle.tl.x, self.rectangle.tl.y)
        self.btn_tr.move(self.rectangle.tr.x, self.rectangle.tr.y)
        self.btn_bl.move(self.rectangle.bl.x, self.rectangle.bl.y)
        self.btn_br.move(self.rectangle.br.x, self.rectangle.br.y)

    def _show_buttons(self):
        self.btn_tl.setHidden(False)
        self.btn_tr.setHidden(False)
        self.btn_bl.setHidden(False)
        self.btn_br.setHidden(False)

    def _hide_buttons(self):
        self.btn_tl.setHidden(True)
        self.btn_tr.setHidden(True)
        self.btn_bl.setHidden(True)
        self.btn_br.setHidden(True)

    def _get_sqr_dist(self, p1: QtCore.QPoint, p2: QtCore.QPoint) -> int:
        return (p1.x() - p2.x())**2 + (p1.y() - p2.y())**2
