import tempfile

from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QApplication, QMainWindow

from translator.gui.widgets import RectController


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
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet('background-color: rgba(0, 0, 0, 0)')

        screen = QApplication.primaryScreen()
        width = screen.size().width()
        height = screen.size().height()
        self.move(screen.geometry().x(), screen.geometry().y())
        self.setFixedSize(width, height)
        self.showFullScreen()

        self.hole = RectController(width, height)
        self.setCentralWidget(self.hole)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key.Key_Escape:
            self.close()
            QApplication.restoreOverrideCursor()
            self.parent_window.show()
        if event.key() == QtCore.Qt.Key.Key_A:
            if self.hole.rectangle.is_valid():
                self.take_screenshot('test.jpg')
        if event.key() == QtCore.Qt.Key.Key_B:
            print(self.screen())
            print(QApplication.screens())

    def take_screenshot(self, outpath: str = '') -> str:
        screen = QApplication.primaryScreen()
        rect = self.hole.rectangle
        screenshot = screen.grabWindow(0, rect.tl.x, rect.tl.y, rect.width, rect.height)
        if outpath == '':
            filename = tempfile.mktemp(suffix='.jpg')
        else:
            filename = outpath
        screenshot.save(filename, 'jpg')
        return filename
