# rect_config.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QPushButton,
    QColorDialog, QMessageBox
)
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

class RectConfigWindow(QWidget):
    def __init__(self, overlay_instance):
        super().__init__()
        self.overlay = overlay_instance # Reference to the RecordingOverlay instance
        self.setWindowTitle("Rectangle Configuration")
        self.setFixedSize(320, 270) # Adjust size as needed

        self._current_color = QColor(self.overlay.rect_color) # Make a copy to modify
        self._current_margin = self.overlay.resize_margin

        self._init_ui()
        self._load_current_values()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)

        # --- Color Section ---
        color_group_layout = QVBoxLayout()
        color_group_layout.addWidget(QLabel("<b>Rectangle Color:</b>"))

        # Color picker button and preview
        color_layout_top = QHBoxLayout()
        self.color_preview = QLabel("   ") # Placeholder for color
        self.color_preview.setFixedSize(60, 25)
        self.color_preview.setStyleSheet(f"background-color: {self._current_color.name(QColor.HexArgb)}; border: 1px solid gray;")
        color_layout_top.addWidget(self.color_preview)

        self.color_button = QPushButton("Pick Color...")
        self.color_button.clicked.connect(self._pick_color)
        color_layout_top.addWidget(self.color_button)
        color_group_layout.addLayout(color_layout_top)


        # RGBA Spinboxes
        rgba_layout = QHBoxLayout()
        rgba_layout.addWidget(QLabel("R:"))
        self.red_spinbox = QSpinBox()
        self.red_spinbox.setRange(0, 255)
        self.red_spinbox.valueChanged.connect(self._update_color_from_spinboxes)
        rgba_layout.addWidget(self.red_spinbox)

        rgba_layout.addWidget(QLabel("G:"))
        self.green_spinbox = QSpinBox()
        self.green_spinbox.setRange(0, 255)
        self.green_spinbox.valueChanged.connect(self._update_color_from_spinboxes)
        rgba_layout.addWidget(self.green_spinbox)

        rgba_layout.addWidget(QLabel("B:"))
        self.blue_spinbox = QSpinBox()
        self.blue_spinbox.setRange(0, 255)
        self.blue_spinbox.valueChanged.connect(self._update_color_from_spinboxes)
        rgba_layout.addWidget(self.blue_spinbox)

        rgba_layout.addWidget(QLabel("A:"))
        self.alpha_spinbox = QSpinBox()
        self.alpha_spinbox.setRange(0, 255)
        self.alpha_spinbox.valueChanged.connect(self._update_color_from_spinboxes)
        rgba_layout.addWidget(self.alpha_spinbox)

        color_group_layout.addLayout(rgba_layout)
        main_layout.addLayout(color_group_layout)


        # --- Margin Section ---
        margin_layout = QHBoxLayout()
        margin_layout.addWidget(QLabel("<b>Resize Margin:</b>"))
        self.margin_spinbox = QSpinBox()
        self.margin_spinbox.setRange(1, 50) # Reasonable range for margin size
        margin_layout.addWidget(self.margin_spinbox)
        main_layout.addLayout(margin_layout)

        main_layout.addStretch()

        # --- Action Buttons ---
        button_layout = QHBoxLayout()
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self._apply_config)
        button_layout.addWidget(self.apply_button)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        button_layout.addWidget(self.close_button)
        main_layout.addLayout(button_layout)

    def _load_current_values(self):
        """Loads current values from the overlay into the UI elements."""
        self.red_spinbox.setValue(self._current_color.red())
        self.green_spinbox.setValue(self._current_color.green())
        self.blue_spinbox.setValue(self._current_color.blue())
        self.alpha_spinbox.setValue(self._current_color.alpha())
        self.margin_spinbox.setValue(self._current_margin)
        self._update_color_preview()

    def _pick_color(self):
        """Opens a color dialog to pick the base color."""
        # QColorDialog allows picking color, but typically returns an opaque color.
        # We'll preserve the current alpha from our spinbox.
        color = QColorDialog.getColor(self._current_color, self, "Select Rectangle Color")
        if color.isValid():
            # Update the RGB components, keep the alpha from the spinbox
            self._current_color = QColor(color.red(), color.green(), color.blue(), self.alpha_spinbox.value())
            self._update_spinboxes_from_color()
            self._update_color_preview()

    def _update_spinboxes_from_color(self):
        """Updates RGB spinboxes based on the _current_color."""
        self.red_spinbox.blockSignals(True)
        self.green_spinbox.blockSignals(True)
        self.blue_spinbox.blockSignals(True)
        # Alpha is handled separately by its own spinbox
        # self.alpha_spinbox.blockSignals(True)

        self.red_spinbox.setValue(self._current_color.red())
        self.green_spinbox.setValue(self._current_color.green())
        self.blue_spinbox.setValue(self._current_color.blue())
        # self.alpha_spinbox.setValue(self._current_color.alpha()) # Managed by user input

        self.red_spinbox.blockSignals(False)
        self.green_spinbox.blockSignals(False)
        self.blue_spinbox.blockSignals(False)
        # self.alpha_spinbox.blockSignals(False)

    def _update_color_from_spinboxes(self):
        """Updates _current_color and preview from spinbox values."""
        r = self.red_spinbox.value()
        g = self.green_spinbox.value()
        b = self.blue_spinbox.value()
        a = self.alpha_spinbox.value()
        self._current_color = QColor(r, g, b, a)
        self._update_color_preview()

    def _update_color_preview(self):
        """Updates the color preview label's background."""
        # Use QColor.HexArgb to include alpha in the CSS color string
        self.color_preview.setStyleSheet(f"background-color: {self._current_color.name(QColor.HexArgb)}; border: 1px solid gray;")
        self.color_preview.update()

    def _apply_config(self):
        """Applies the configured values to the RecordingOverlay."""
        # Update overlay properties using their setters
        self.overlay.rect_color = self._current_color
        self.overlay.resize_margin = self.margin_spinbox.value()

        QMessageBox.information(self, "Configuration Applied", "Rectangle configuration updated successfully!")