import typing
from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPixmap, QWheelEvent, QEnterEvent, QBrush, QColor
from PyQt6.QtWidgets import (QApplication, QSizePolicy, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView, QVBoxLayout, QWidget)

from translator.gui.const import ZOOM_FACTOR


class CustomGraphicsView(QGraphicsView):

    def __init__(self):
        super().__init__()

    def wheelEvent(self, event: QWheelEvent) -> None:
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            event.ignore()
        else:
            super().wheelEvent(event)


class ImageViewer(QWidget):

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        self._view = CustomGraphicsView()
        self._scene = QGraphicsScene()
        self._view.setScene(self._scene)

        self._image_item = QGraphicsPixmapItem()
        self._scene.addItem(self._image_item)
        self._scene.setBackgroundBrush(QBrush(QColor(0, 0, 0, 20)))
        self._view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self._layout = QVBoxLayout()
        self._layout.addWidget(self._view)
        self.setLayout(self._layout)

    def load_image(self, image_path: str):
        self.pixmap = QPixmap(image_path)
        self._image_item.setPixmap(self.pixmap)

        self._view.setSceneRect(0, 0, self.pixmap.width(), self.pixmap.height())
        self._image_item.resetTransform()
        self._view.resetTransform()
        self._view.centerOn(self._image_item)

    def get_img_width(self) -> int:
        if self.pixmap is None:
            return 0
        return self.pixmap.width()

    def get_img_height(self) -> int:
        if self.pixmap is None:
            return 0
        return self.pixmap.height()

    def _zoom_in(self):
        self._view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._view.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self._view.scale(ZOOM_FACTOR, ZOOM_FACTOR)

    def _zoom_out(self):
        self._view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._view.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self._view.scale(1 / ZOOM_FACTOR, 1 / ZOOM_FACTOR)

    def wheelEvent(self, event: QWheelEvent) -> None:
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.angleDelta().y() > 0:
                self._zoom_in()
            else:
                self._zoom_out()

    # def enterEvent(self, event: QEnterEvent) -> None:
    #     QApplication.setOverrideCursor(QtGui.QCursor(Qt.CursorShape.OpenHandCursor))

    # def enterEvent(self, event: QEnterEvent) -> None:
    #     QApplication.restoreOverrideCursor()
