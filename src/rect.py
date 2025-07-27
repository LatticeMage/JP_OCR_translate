# rect.py
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt, QRect, QPoint

class RecordingOverlay(QWidget):
    """
    A transparent, frameless, always-on-top window that draws a red rectangle.
    Allows click-through by default, but becomes interactive when focused:
    - Drag the interior to move
    - Drag the bottom-right corner to resize
    - Press Esc to quit
    """
    RESIZE_MARGIN = 10

    def __init__(self):
        super().__init__()

        # Default geometry
        self._rect_x = 200
        self._rect_y = 200
        self._rect_width = 800
        self._rect_height = 600
        self.setGeometry(self._rect_x, self._rect_y, self._rect_width, self._rect_height)

        # Window flags
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        # Transparent background
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # Accept focus for interaction
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        # Initially click-through
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        # Enable mouse tracking for hover cursor
        self.setMouseTracking(True)

        # State
        self._dragging = False
        self._resizing = False
        self._drag_start = QPoint()
        self._orig_geom = QRect()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(QColor(255, 0, 0))
        pen.setWidth(3)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.drawRect(QRect(0, 0, self.width() - 1, self.height() - 1))

    def focusInEvent(self, event):
        # Become interactive
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        # Go back to click-through
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().focusOutEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start = event.globalPos()
            self._orig_geom = self.geometry()
            local = event.pos()
            if (
                self.width() - local.x() <= self.RESIZE_MARGIN and
                self.height() - local.y() <= self.RESIZE_MARGIN
            ):
                self._resizing = True
            else:
                self._dragging = True
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # Update cursor on hover
        if not (self._dragging or self._resizing):
            local = event.pos()
            if (
                self.width() - local.x() <= self.RESIZE_MARGIN and
                self.height() - local.y() <= self.RESIZE_MARGIN
            ):
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            else:
                self.setCursor(Qt.CursorShape.SizeAllCursor)
        # Handle drag or resize
        if event.buttons() & Qt.MouseButton.LeftButton:
            delta = event.globalPos() - self._drag_start
            if self._resizing:
                new_w = max(1, self._orig_geom.width() + delta.x())
                new_h = max(1, self._orig_geom.height() + delta.y())
                self.setGeometry(
                    self._orig_geom.x(), self._orig_geom.y(), new_w, new_h
                )
                self.update()
            elif self._dragging:
                self.setGeometry(
                    self._orig_geom.x() + delta.x(),
                    self._orig_geom.y() + delta.y(),
                    self._orig_geom.width(),
                    self._orig_geom.height()
                )
                self.update()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._dragging = False
        self._resizing = False
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        from PySide6.QtWidgets import QApplication
        if event.key() == Qt.Key.Key_Escape:
            QApplication.instance().quit()
        else:
            super().keyPressEvent(event)
