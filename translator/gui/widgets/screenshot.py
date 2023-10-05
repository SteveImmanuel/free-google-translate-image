import typing
from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton
from PyQt6.QtGui import QMouseEvent, QKeyEvent, QPaintEvent, QRegion

from translator.gui.widgets.circle_button import CircleButton
from translator.gui.widgets.background import Background


class Screenshot(QWidget):

    def __init__(self, parent_window: QMainWindow) -> None:
        super().__init__()
        self.is_mouse_pressed = False
        self.parent_window = parent_window
        self.top_left = QtCore.QPoint()
        self.bottom_right = QtCore.QPoint()
        self.setMouseTracking(True)
        self._setup_ui()

    def show(self) -> None:
        QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CursorShape.CrossCursor))
        return super().show()

    def _setup_ui(self) -> None:
        self.setWindowFlags(QtCore.Qt.WindowType.Window | QtCore.Qt.WindowType.FramelessWindowHint)
        # self.setStyleSheet('background-color: black;')
        # self.setWindowOpacity(0.5)

        width = QApplication.primaryScreen().size().width()
        height = QApplication.primaryScreen().size().height()

        self.background = Background(width, height, self.top_left, self.bottom_right)

        self.btn_tl = CircleButton(QtCore.Qt.CursorShape.SizeFDiagCursor, self)
        self.btn_tr = CircleButton(QtCore.Qt.CursorShape.SizeBDiagCursor, self)
        self.btn_bl = CircleButton(QtCore.Qt.CursorShape.SizeBDiagCursor, self)
        self.btn_br = CircleButton(QtCore.Qt.CursorShape.SizeFDiagCursor, self)

    def _reposition_buttons(self):
        self.btn_tl.move(self.top_left.x() - self.btn_tl.width() // 2, self.top_left.y() - self.btn_tl.height() // 2)
        self.btn_tr.move(self.top_left.x() - self.btn_tr.width() // 2,
                         self.bottom_right.y() - self.btn_tr.height() // 2)
        self.btn_bl.move(self.bottom_right.x() - self.btn_bl.width() // 2,
                         self.top_left.y() - self.btn_bl.height() // 2)
        self.btn_br.move(self.bottom_right.x() - self.btn_br.width() // 2,
                         self.bottom_right.y() - self.btn_br.height() // 2)

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

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.is_mouse_pressed = True
        self.top_left = event.position().toPoint()
        self.bottom_right = event.position().toPoint()
        self.update()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.is_mouse_pressed:
            self.bottom_right = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.is_mouse_pressed = False
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        self._reposition_buttons()
        self._show_buttons()

        self.background.update_hole(self.top_left, self.bottom_right)

        qp = QtGui.QPainter(self)
        qp.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        br = QtGui.QBrush(QtGui.QColor(-255, -255, -255, 100))
        qp.setBrush(br)
        qp.drawRect(QtCore.QRect(self.top_left, self.bottom_right))

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key.Key_Escape:
            self.close()
            QApplication.restoreOverrideCursor()
            self.parent_window.show()

    def get_sqr_dist(self, p1: QtCore.QPoint, p2: QtCore.QPoint) -> int:
        return (p1.x() - p2.x())**2 + (p1.y() - p2.y())**2

    # def get_closest_
