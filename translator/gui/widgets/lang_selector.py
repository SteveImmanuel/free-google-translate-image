import typing
from PyQt6 import QtCore
from PyQt6.QtWidgets import QComboBox, QWidget, QHBoxLayout
from translator.gui.const import LANG


class LangSelector(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self._setup_ui()

    def _setup_ui(self) -> None:
        self._source_lang = QComboBox()
        self._target_lang = QComboBox()

        lang_list = list(map(lambda x: x.name, LANG))
        self._source_lang.addItems(lang_list)
        self._target_lang.addItems(lang_list)
        self._target_lang.setCurrentIndex(1)

        self._layout = QHBoxLayout()
        self._layout.addWidget(self._source_lang)
        self._layout.addWidget(self._target_lang)

        self.setLayout(self._layout)
