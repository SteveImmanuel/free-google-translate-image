from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import QKeyEvent, QMouseEvent, QPaintEvent, QRegion
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget

from translator.gui.widgets import CircleButton, RectController


class Screenshot(QMainWindow):

    def __init__(self, parent_window: QMainWindow) -> None:
        super().__init__()
        self.is_mouse_pressed = False
        self.parent_window = parent_window
        self._setup_ui()

    def show(self) -> None:
        QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CursorShape.CrossCursor))
        return super().show()

    def _setup_ui(self) -> None:
        self.setWindowFlags(QtCore.Qt.WindowType.Window | QtCore.Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet('background-color: white;')
        self.setWindowOpacity(0.1)

        width = QApplication.primaryScreen().size().width()
        height = QApplication.primaryScreen().size().height()
        self.setFixedSize(width, height)

        self.hole = RectController(width, height)
        self.setCentralWidget(self.hole)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key.Key_Escape:
            self.close()
            QApplication.restoreOverrideCursor()
            self.parent_window.show()
