import typing

from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QThreadPool
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget)

from translator.engine import translate_emulate
from translator.gui.const import MAX_THREADS
from translator.gui.screenshot_window import Screenshot
from translator.gui.widgets import *
from translator.gui.worker import TranslateWorker


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        QThreadPool.globalInstance().setMaxThreadCount(MAX_THREADS)
        self.last_x = None
        self.last_y = None
        self.ss_window = None
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle('Instant Screen Translator')

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

    def on_translate_ss(self, input_path: str):
        worker = TranslateWorker(lambda: translate_emulate(
            input_path,
            'out.png',
            self._lang_selector.source_lang,
            self._lang_selector.target_lang,
        ))
        worker.signal.success.connect(self.on_translate_complete)
        worker.signal.error.connect(self.on_translate_error)
        print('starting worker')

        QThreadPool.globalInstance().start(worker)

    def on_translate_complete(self, translated_path: str, translated_text: str):
        print(translated_path, translated_text)

    def on_translate_error(self, error: str):
        print(error)

    def show_ss_window(self, a):
        self.last_x = self.x()
        self.last_y = self.y()
        if self.ss_window is None:
            self.ss_window = Screenshot(self)
        self.ss_window.show()
        self.hide()

    def show(self) -> None:
        if self.last_x and self.last_y:
            self.move(self.last_x, self.last_y)
        QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        return super().show()
