import typing
from PyQt6.QtWidgets import QPushButton, QWidget, QApplication
from PyQt6.QtGui import QEnterEvent
from PyQt6 import QtCore, QtGui


class CircleButton(QPushButton):

    def __init__(
        self,
        cursor_type: QtCore.Qt.CursorShape,
        parent: QWidget,
        size: int = 20,
        x: int = 0,
        y: int = 0,
        hidden: bool = True,
    ):
        super().__init__(parent)

        self.setStyleSheet(f"""
            background-color: lightgray;
            border-radius:{size//2}px;
            border-color: red;
            max-width:{size}px;
            max-height:{size}px;
            min-width:{size}px;
            min-height:{size}px;
        """)
        self.cursor_type = cursor_type
        self.x = x
        self.y = y

        self.move(x, y)
        self.setHidden(hidden)

    def move(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        super().move(x - self.width() // 2, y - self.height() // 2)

    def enterEvent(self, event: QEnterEvent) -> None:
        QApplication.setOverrideCursor(QtGui.QCursor(self.cursor_type))
        return super().enterEvent(event)

    def leaveEvent(self, event: QEnterEvent) -> None:
        QApplication.restoreOverrideCursor()
        return super().leaveEvent(event)
