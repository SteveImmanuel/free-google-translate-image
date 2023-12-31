import typing

from PyQt6 import QtCore
from PyQt6.QtWidgets import QComboBox, QHBoxLayout, QWidget

from translator.gui.const import LANG


class LangSelector(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self._setup_ui()

    def _setup_ui(self) -> None:
        self._source_lang = QComboBox()
        self._target_lang = QComboBox()
        self._source_lang.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self._target_lang.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        lang_list = list(LANG.keys())
        self._source_lang.addItems(lang_list)
        self._target_lang.addItems(lang_list[1:])
        self._target_lang.setCurrentIndex(0)

        self._layout = QHBoxLayout()
        self._layout.addWidget(self._source_lang)
        self._layout.addWidget(self._target_lang)

        self.setLayout(self._layout)

    @property
    def source_lang(self) -> str:
        return LANG[self._source_lang.currentText()]

    @property
    def target_lang(self) -> str:
        return LANG[self._target_lang.currentText()]
