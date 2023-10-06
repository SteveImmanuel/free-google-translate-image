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
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet('background-color: rgba(0, 0, 0, 0)')

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
        if event.key() == QtCore.Qt.Key.Key_A:
            self.take_screenshot()

    def take_screenshot(self):
        print('taking screenshot')
        screen = QApplication.primaryScreen()
        print(self.hole.rectangle.tl.x, self.hole.rectangle.tl.y, self.hole.rectangle.br.x - self.hole.rectangle.tl.x,
              self.hole.rectangle.br.y - self.hole.rectangle.tl.y)
        # screenshot = screen.grabWindow(0, self.hole.rectangle.tl.x, self.hole.rectangle.tl.y,
        #                                self.hole.rectangle.br.x - self.hole.rectangle.tl.x,
        #                                self.hole.rectangle.br.y - self.hole.rectangle.tl.y)
        screenshot = screen.grabWindow()
        print(screenshot, screenshot.isNull(), screenshot.size())
        screenshot.save('screenshot.png', 'png')
