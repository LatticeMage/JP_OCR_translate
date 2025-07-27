import sys
from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout,
                                QHBoxLayout, QLineEdit, QLabel, QMessageBox)
from PySide6.QtGui import QPainter, QPen, QColor, QIntValidator
from PySide6.QtCore import Qt, QRect

class RecordingOverlay(QWidget):
    """
    A transparent, frameless, always-on-top window that draws a red rectangle.
    It's designed to be click-through, allowing interaction with windows beneath it.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        # Default geometry for the red rectangle (screen coordinates)
        self._rect_x = 200
        self._rect_y = 200
        self._rect_width = 800
        self._rect_height = 600

        # Set initial window geometry based on the rectangle
        # The window itself will be exactly the size and position of the rectangle
        self.setGeometry(self._rect_x, self._rect_y, self._rect_width, self._rect_height)

        # Set window flags for overlay behavior
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |       # No title bar or border
            Qt.WindowType.WindowStaysOnTopHint |      # Always on top
            Qt.WindowType.WindowTransparentForInput   # Crucial: Allows clicks to pass through
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) # Make background transparent

        # Set an initial window title for identification (not visible due to FramelessHint)
        self.setWindowTitle("Recording Overlay")

    def paintEvent(self, event):
        """
        Draws the red rectangle on the widget.
        The rectangle is drawn at (0,0) relative to the widget's top-left corner,
        and fills the entire widget, which is sized to the desired recording area.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Set pen for the red boundary
        pen = QPen(QColor(255, 0, 0)) # Red color
        pen.setWidth(3)              # 3 pixels thick
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin) # Makes corners rounder
        painter.setPen(pen)

        # Draw the rectangle. It fills the entire widget's area.
        # We draw slightly inside to ensure the full pen width is visible.
        # QRect(left, top, width, height)
        painter.drawRect(
            QRect(0, 0, self.width() - 1, self.height() - 1)
        )
        # Note: painter.drawRect(0, 0, self.width(), self.height()) also works fine
        # for a simple border, the -1 is often used for filled shapes where the border
        # might be drawn slightly outside the specified pixel boundary.

    def set_rect_geometry(self, x, y, width, height):
        """
        Updates the rectangle's position and size.
        This effectively moves and resizes the entire overlay window.
        """
        self._rect_x = x
        self._rect_y = y
        self._rect_width = width
        self._rect_height = height

        # Update the window's geometry
        self.setGeometry(self._rect_x, self._rect_y, self._rect_width, self._rect_height)

        # Request a repaint to update the drawn rectangle
        self.update()

    def get_rect_geometry(self):
        """Returns the current rectangle geometry as (x, y, width, height)."""
        return (self._rect_x, self._rect_y, self._rect_width, self._rect_height)


class ControlWindow(QWidget):
    """
    A separate window to control the RecordingOverlay's position and size.
    """
    def __init__(self, overlay: RecordingOverlay):
        super().__init__()
        self.overlay = overlay
        self.setWindowTitle("Overlay Control")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint) # Keep control on top too

        self.init_ui()
        self.update_fields_from_overlay()

    def init_ui(self):
        layout = QVBoxLayout()

        # Input fields for X, Y, Width, Height
        grid_layout = QHBoxLayout()
        self.x_input = self._create_input_field("X:", grid_layout)
        self.y_input = self._create_input_field("Y:", grid_layout)
        self.width_input = self._create_input_field("Width:", grid_layout)
        self.height_input = self._create_input_field("Height:", grid_layout)

        layout.addLayout(grid_layout)

        # Apply Button
        apply_button = QPushButton("Apply New Geometry")
        apply_button.clicked.connect(self.apply_geometry)
        layout.addWidget(apply_button)

        # Update Fields Button (in case overlay is moved programmatically elsewhere)
        refresh_button = QPushButton("Refresh Fields from Overlay")
        refresh_button.clicked.connect(self.update_fields_from_overlay)
        layout.addWidget(refresh_button)

        # Quit Button
        quit_button = QPushButton("Quit Application")
        quit_button.clicked.connect(QApplication.instance().quit)
        layout.addWidget(quit_button)

        self.setLayout(layout)

        # Set validators for integer input
        validator = QIntValidator()
        self.x_input.setValidator(validator)
        self.y_input.setValidator(validator)
        self.width_input.setValidator(validator)
        self.height_input.setValidator(validator)

    def _create_input_field(self, label_text, layout):
        hbox = QVBoxLayout()
        label = QLabel(label_text)
        line_edit = QLineEdit()
        line_edit.setFixedWidth(80) # Make inputs compact
        hbox.addWidget(label)
        hbox.addWidget(line_edit)
        layout.addLayout(hbox)
        return line_edit

    def update_fields_from_overlay(self):
        x, y, w, h = self.overlay.get_rect_geometry()
        self.x_input.setText(str(x))
        self.y_input.setText(str(y))
        self.width_input.setText(str(w))
        self.height_input.setText(str(h))

    def apply_geometry(self):
        try:
            x = int(self.x_input.text())
            y = int(self.y_input.text())
            width = int(self.width_input.text())
            height = int(self.height_input.text())

            if width <= 0 or height <= 0:
                QMessageBox.warning(self, "Invalid Input", "Width and Height must be positive integers.")
                return

            self.overlay.set_rect_geometry(x, y, width, height)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid integer values for all fields.")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create the overlay window
    overlay_window = RecordingOverlay()
    overlay_window.show()

    # Create the control window
    control_window = ControlWindow(overlay_window)
    control_window.show()

    # Position the control window next to the overlay for convenience
    overlay_geo = overlay_window.geometry()
    control_window.move(overlay_geo.right() + 20, overlay_geo.top())


    sys.exit(app.exec())