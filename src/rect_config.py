from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSlider, QColorDialog, QMessageBox
)
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

class RectConfigWindow(QWidget):
    def __init__(self, overlay_instance):
        super().__init__()
        self.overlay = overlay_instance  # Reference to the RecordingOverlay instance
        self.setWindowTitle("Rectangle Configuration")
        self.setFixedSize(320, 250)  # Adjusted size for new layout

        # Copy current settings
        self._current_color = QColor(self.overlay.rect_color)
        self._current_margin = self.overlay.resize_margin

        self._init_ui()
        self._load_current_values()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)

        # --- Color Section ---
        color_group_layout = QVBoxLayout()
        color_group_layout.addWidget(QLabel("<b>Rectangle Color:</b>"))

        # Color picker button and preview
        color_layout = QHBoxLayout()
        self.color_preview = QLabel("   ")  # Placeholder for color
        self.color_preview.setFixedSize(60, 25)
        color_layout.addWidget(self.color_preview)

        self.color_button = QPushButton("Pick Color...")
        self.color_button.clicked.connect(self._pick_color)
        color_layout.addWidget(self.color_button)
        color_group_layout.addLayout(color_layout)

        # Alpha slider
        alpha_layout = QHBoxLayout()
        alpha_layout.addWidget(QLabel("Alpha:"))
        self.alpha_slider = QSlider(Qt.Horizontal)
        self.alpha_slider.setRange(0, 255)
        self.alpha_slider.valueChanged.connect(self._update_alpha_from_slider)
        alpha_layout.addWidget(self.alpha_slider)
        color_group_layout.addLayout(alpha_layout)

        main_layout.addLayout(color_group_layout)

        # --- Margin Section ---
        margin_layout = QHBoxLayout()
        margin_layout.addWidget(QLabel("<b>Resize Margin:</b>"))
        self.margin_spinbox = QSlider(Qt.Horizontal)
        self.margin_spinbox.setRange(1, 50)  # Reasonable range for margin size
        self.margin_spinbox.setFixedWidth(150)
        self.margin_spinbox.setValue(self._current_margin)
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
        # Set alpha slider and margin slider
        self.alpha_slider.setValue(self._current_color.alpha())
        self.margin_spinbox.setValue(self._current_margin)
        self._update_color_preview()

    def _pick_color(self):
        """Opens a color dialog to pick the base color."""
        color = QColorDialog.getColor(self._current_color, self, "Select Rectangle Color")
        if color.isValid():
            # Preserve alpha from slider
            alpha = self.alpha_slider.value()
            self._current_color = QColor(color.red(), color.green(), color.blue(), alpha)
            self._update_color_preview()

    def _update_alpha_from_slider(self, value):
        """Updates the alpha channel and preview from the slider."""
        self._current_color.setAlpha(value)
        self._update_color_preview()

    def _update_color_preview(self):
        """Updates the color preview label's background."""
        # Use HexArgb to include alpha in CSS string
        self.color_preview.setStyleSheet(
            f"background-color: {self._current_color.name(QColor.HexArgb)}; border: 1px solid gray;"
        )
        self.color_preview.update()

    def _apply_config(self):
        """Applies the configured values to the RecordingOverlay."""
        self.overlay.rect_color = self._current_color
        self.overlay.resize_margin = self.margin_spinbox.value()

        QMessageBox.information(
            self, "Configuration Applied", "Rectangle configuration updated successfully!"
        )
