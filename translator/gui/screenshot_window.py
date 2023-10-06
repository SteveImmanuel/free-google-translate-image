import tempfile

from PyQt6 import QtCore, QtGui, QtTest
from PyQt6.QtCore import QThreadPool
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QApplication, QMainWindow

from translator.engine import translate_emulate
from translator.gui.widgets import RectController
from translator.gui.worker import TranslateWorker


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

        screen = self.parent_window.screen()
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
                self.take_screenshot('test2.png')
        if event.key() == QtCore.Qt.Key.Key_B:
            print(self.screen())
            print(QApplication.screens())
        if event.key() == QtCore.Qt.Key.Key_C:
            self.hole.hide_buttons()
        if event.key() == QtCore.Qt.Key.Key_D:
            self.hole.show_buttons()

    def take_screenshot(self, outpath: str = '') -> str:

        screen = self.screen()
        rect = self.hole.rectangle
        self.hole.hide_buttons()
        QtTest.QTest.qWait(100)
        screenshot = screen.grabWindow(0, *rect.get_hole_geom())
        self.hole.show_buttons()

        if outpath == '':
            filename = tempfile.mktemp(suffix='.png')
        else:
            filename = outpath
        screenshot.save(filename, 'png')

        worker = TranslateWorker(lambda: translate_emulate(filename, 'out.png'))
        worker.signal.success.connect(self.on_translate_complete)
        worker.signal.error.connect(self.on_translate_error)
        print('starting worker')
        QThreadPool.globalInstance().start(worker)

        return filename

    def on_translate_complete(self, translated_path: str, translated_text: str):
        print(translated_path, translated_text)

    def on_translate_error(self, error: str):
        print(error)
