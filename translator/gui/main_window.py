import logging
import typing

from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QThreadPool
from PyQt6.QtGui import QPixmap, QKeyEvent
from PyQt6.QtWidgets import (QApplication, QCheckBox, QLabel, QMainWindow, QProgressBar, QPushButton, QSizePolicy, QVBoxLayout,
                             QWidget, QComboBox)

from translator.engine import translate_emulate
from translator.gui.const import MAX_THREADS, INSTRUCTION
from translator.gui.screenshot_window import Screenshot
from translator.gui.widgets import *
from translator.gui.worker import TranslateWorker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
        self._lbl_img = QLabel(INSTRUCTION, self)
        self._lbl_img.setMinimumSize(320, 240)
        self._progress_bar = QProgressBar(self)
        self._progress_bar.setMinimum(0)
        self._progress_bar.setMaximum(0)
        self._progress_bar.setHidden(True)

        self._lbl_img.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._lbl_img.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._btn_ss.adjustSize()
        # self._check_always_on_top = QCheckBox('Always on top', self)

        self._layout = QVBoxLayout()
        self._layout.addWidget(self._lang_selector)
        # self._layout.addWidget(self._check_always_on_top)
        self._layout.addWidget(self._lbl_img)
        self._layout.addWidget(self._progress_bar)
        self._layout.addWidget(self._btn_ss)
        self._layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self._btn_ss.clicked.connect(self.show_ss_window)
        # self._check_always_on_top.toggled.connect(self._on_check_always_on_top)

        self._main_widget = QWidget()
        self._main_widget.setLayout(self._layout)
        self.setCentralWidget(self._main_widget)
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)

    def _on_translate_complete(self, translated_path: str, translated_text: str):
        logger.info(f'Translation complete: {translated_path}')
        pixmap = QPixmap(translated_path)
        self._lbl_img.setPixmap(pixmap)
        self._lbl_img.setHidden(False)
        self._progress_bar.setHidden(True)
        self._btn_ss.setDisabled(False)

    def _on_translate_error(self, error: str):
        logger.error('Translation error: {error}')
        self._lbl_img.setPixmap(QPixmap())
        self._lbl_img.setText(error)
        self._lbl_img.setHidden(False)
        self._progress_bar.setHidden(True)
        self._btn_ss.setDisabled(False)

    # def _on_check_always_on_top(self, checked: bool):
    #     self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)

    def on_translate_ss(self, input_path: str):
        self._progress_bar.setHidden(False)
        self._lbl_img.setHidden(True)
        self._btn_ss.setDisabled(True)

        worker = TranslateWorker(lambda: translate_emulate(
            input_path,
            source_lang=self._lang_selector.source_lang,
            target_lang=self._lang_selector.target_lang,
        ))
        worker.signal.success.connect(self._on_translate_complete)
        worker.signal.error.connect(self._on_translate_error)
        logger.info('Starting translation worker')

        QThreadPool.globalInstance().start(worker)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key.Key_X and event.modifiers() == QtCore.Qt.KeyboardModifier.ShiftModifier:
            self.show_ss_window()

    def show_ss_window(self):
        self.last_x = self.x()
        self.last_y = self.y()
        if self.ss_window is None:
            self.ss_window = Screenshot(self)
        self.ss_window.show()
        self.hide()

    def show(self) -> None:
        self.setFocus()
        if self.last_x and self.last_y:
            self.move(self.last_x, self.last_y)
        QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        return super().show()
