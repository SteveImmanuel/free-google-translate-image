from multiprocessing import cpu_count
import typing
from PyQt6 import QtGui, QtCore

from PyQt6.QtCore import QThreadPool
from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QApplication

from translator.gui.widgets import *
from translator.gui.screenshot_window import Screenshot


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        max_thread_count = max(1, min(cpu_count() - 1, 4))
        QThreadPool.globalInstance().setMaxThreadCount(max_thread_count)
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle('Instant Screen Translator')
        # self.setMinimumSize(500, 650)

        self._lang_selector = LangSelector()

        self._btn_ss = QPushButton('Take Screenshot', self)
        self._btn_ss.adjustSize()

        # self._layout = QVBoxLayout()
        # self._layout.addWidget(self._lang_selector)
        # self._layout.addWidget(self.btn_ss)

        self._btn_ss.clicked.connect(self.show_ss_window)

        # self.setLayout(self._layout)
        # self.setCentralWidget(self._lang_selector)

    def show_ss_window(self, a):
        self.ss_window = Screenshot(self)
        self.ss_window.show()
        self.hide()

    def show(self) -> None:
        QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        return super().show()
