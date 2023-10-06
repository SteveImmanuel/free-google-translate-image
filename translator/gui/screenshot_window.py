import tempfile

from PyQt6 import QtCore, QtGui, QtTest
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
        screen = self.parent_window.screen()
        width = screen.size().width()
        height = screen.size().height()
        self.move(screen.geometry().x(), screen.geometry().y())
        self.setFixedSize(width, height)
        self.showFullScreen()
        QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CursorShape.CrossCursor))
        return super().show()

    def _setup_ui(self) -> None:
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet('background-color: rgba(0, 0, 0, 0)')

        self.hole = RectController(self.parent_window.screen().size().width(), self.parent_window.screen().size().height())
        self.setCentralWidget(self.hole)

    def close_window(self):
        self.close()
        QApplication.restoreOverrideCursor()
        self.parent_window.show()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key.Key_Escape:
            self.close_window()
        if event.key() == QtCore.Qt.Key.Key_Space:
            if self.hole.rectangle.is_valid():
                ss_path = self.take_screenshot()
                self.parent_window.on_translate_ss(ss_path)
                self.close_window()

    def take_screenshot(self, outpath: str = '') -> str:
        screen = self.screen()
        rect = self.hole.rectangle
        self.hole.hide_buttons()
        QtTest.QTest.qWait(100)  # wait for buttons to hide
        screenshot = screen.grabWindow(0, *rect.get_hole_geom())
        self.hole.show_buttons()

        if outpath == '':
            filename = tempfile.mktemp(suffix='.png')
        else:
            filename = outpath
        screenshot.save(filename, 'png')

        return filename
