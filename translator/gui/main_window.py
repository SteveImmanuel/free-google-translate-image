from multiprocessing import cpu_count
import typing
from PyQt6 import QtGui, QtCore

from PyQt6.QtCore import QThreadPool
from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QApplication, QWidget

from translator.gui.widgets import *
from translator.gui.screenshot_window import Screenshot


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        max_thread_count = max(1, min(cpu_count() - 1, 4))
        QThreadPool.globalInstance().setMaxThreadCount(max_thread_count)
        self.last_x = None
        self.last_y = None
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle('Instant Screen Translator')
        # self.setMinimumSize(500, 650)

        self._lang_selector = LangSelector()
        self._btn_ss = QPushButton('Take Screenshot', self)
        self._btn_ss.adjustSize()

        self._layout = QVBoxLayout()
        self._layout.addWidget(self._lang_selector)
        self._layout.addWidget(self._btn_ss)

        self._btn_ss.clicked.connect(self.show_ss_window)

        self._main_widget = QWidget()
        self._main_widget.setLayout(self._layout)
        self.setCentralWidget(self._main_widget)
        # self.setLayout(self._layout)
        # self.setCentralWidget(self._lang_selector)

    def show_ss_window(self, a):
        self.last_x = self.x()
        self.last_y = self.y()
        self.ss_window = Screenshot(self)
        self.ss_window.show()
        self.hide()

    def show(self) -> None:
        if self.last_x and self.last_y:
            self.move(self.last_x, self.last_y)
        QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        return super().show()
