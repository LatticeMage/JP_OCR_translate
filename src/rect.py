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
    # RESIZE_MARGIN is now an instance attribute, not a class constant

    def __init__(self):
        super().__init__()

        # --- Configurable attributes with default values ---
        self._rect_color = QColor(255, 0, 0, 255) # Default Red, fully opaque (RGBA)
        self._resize_margin = 10 # Default margin for resize handle
        # --- End configurable attributes ---

        # Default geometry
        self._rect_x = 200
        self._rect_y = 200
        self._rect_width = 550
        self._rect_height = 400
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

    # --- Properties for rect_color and resize_margin ---
    @property
    def rect_color(self):
        return self._rect_color

    @rect_color.setter
    def rect_color(self, color: QColor):
        if isinstance(color, QColor) and self._rect_color != color:
            self._rect_color = color
            self.update() # Trigger a repaint

    @property
    def resize_margin(self):
        return self._resize_margin

    @resize_margin.setter
    def resize_margin(self, margin: int):
        if isinstance(margin, int) and margin > 0 and self._resize_margin != margin:
            self._resize_margin = margin
            # No update() needed here as margin affects mouse interaction, not direct drawing

    # --- End properties ---

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # Use the configurable rect_color
        pen = QPen(self._rect_color)
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
                # Use the configurable resize_margin
                self.width() - local.x() <= self.resize_margin and
                self.height() - local.y() <= self.resize_margin
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
                # Use the configurable resize_margin
                self.width() - local.x() <= self.resize_margin and
                self.height() - local.y() <= self.resize_margin
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