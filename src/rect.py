
# rect.py

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt, QRect, QPoint
from rect_config import RectConfig

class RecordingOverlay(QWidget):
    def __init__(self):
        super().__init__()
        
        self.config = RectConfig.default()
        
        # Setup window
        self.setGeometry(200, 200, 550, 400)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setMouseTracking(True)

        # Interaction state
        self._dragging = False
        self._resizing = False
        self._drag_start = QPoint()
        self._orig_geom = QRect()

    def update_config(self, new_config: RectConfig):
        """Single update method - replace entire config"""
        self.config = new_config
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(self.config.color)
        pen.setWidth(3)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.drawRect(QRect(0, 0, self.width() - 1, self.height() - 1))

    def focusInEvent(self, event):
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().focusOutEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start = event.globalPos()
            self._orig_geom = self.geometry()
            local = event.pos()
            if (
                self.width() - local.x() <= self.config.margin and
                self.height() - local.y() <= self.config.margin
            ):
                self._resizing = True
            else:
                self._dragging = True
            event.accept()

    def mouseMoveEvent(self, event):
        if not (self._dragging or self._resizing):
            local = event.pos()
            if (
                self.width() - local.x() <= self.config.margin and
                self.height() - local.y() <= self.config.margin
            ):
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            else:
                self.setCursor(Qt.CursorShape.SizeAllCursor)
        
        if event.buttons() & Qt.MouseButton.LeftButton:
            delta = event.globalPos() - self._drag_start
            if self._resizing:
                new_w = max(1, self._orig_geom.width() + delta.x())
                new_h = max(1, self._orig_geom.height() + delta.y())
                self.setGeometry(self._orig_geom.x(), self._orig_geom.y(), new_w, new_h)
            elif self._dragging:
                self.setGeometry(
                    self._orig_geom.x() + delta.x(),
                    self._orig_geom.y() + delta.y(),
                    self._orig_geom.width(),
                    self._orig_geom.height()
                )

    def mouseReleaseEvent(self, event):
        self._dragging = False
        self._resizing = False

    def keyPressEvent(self, event):
        from PySide6.QtWidgets import QApplication
        if event.key() == Qt.Key.Key_Escape:
            QApplication.instance().quit()