# rect_config.py

from dataclasses import dataclass
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSlider, QColorDialog, QSpinBox
)
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

@dataclass
class RectConfig:
    color: QColor
    margin: int
    
    @classmethod
    def default(cls):
        return cls(color=QColor(255, 0, 0, 255), margin=10)

class RectConfigWindow(QWidget):
    def __init__(self, overlay_instance):
        super().__init__()
        self.overlay = overlay_instance
        self.setWindowTitle("Rectangle Configuration")
        self.setFixedSize(320, 200)
        
        # Work with a copy of current config
        self.config = RectConfig(
            color=QColor(self.overlay.config.color),
            margin=self.overlay.config.margin
        )
        
        self._init_ui()
        self._load_values()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        # Color section
        color_layout = QHBoxLayout()
        self.color_preview = QLabel("   ")
        self.color_preview.setFixedSize(60, 25)
        color_layout.addWidget(self.color_preview)
        
        self.color_button = QPushButton("Pick Color")
        self.color_button.clicked.connect(self._pick_color)
        color_layout.addWidget(self.color_button)
        layout.addLayout(color_layout)
        
        # Alpha slider
        alpha_layout = QHBoxLayout()
        alpha_layout.addWidget(QLabel("Alpha:"))
        self.alpha_slider = QSlider(Qt.Horizontal)
        self.alpha_slider.setRange(0, 255)
        self.alpha_slider.valueChanged.connect(self._update_alpha)
        alpha_layout.addWidget(self.alpha_slider)
        layout.addLayout(alpha_layout)
        
        # Margin
        margin_layout = QHBoxLayout()
        margin_layout.addWidget(QLabel("Margin:"))
        self.margin_spinbox = QSpinBox()
        self.margin_spinbox.setRange(1, 50)
        self.margin_spinbox.valueChanged.connect(self._update_margin)
        margin_layout.addWidget(self.margin_spinbox)
        layout.addLayout(margin_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self._apply)
        button_layout.addWidget(apply_btn)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)

    def _load_values(self):
        self.alpha_slider.setValue(self.config.color.alpha())
        self.margin_spinbox.setValue(self.config.margin)
        self._update_preview()

    def _pick_color(self):
        color = QColorDialog.getColor(self.config.color, self)
        if color.isValid():
            color.setAlpha(self.alpha_slider.value())
            self.config.color = color
            self._update_preview()

    def _update_alpha(self, value):
        self.config.color.setAlpha(value)
        self._update_preview()

    def _update_margin(self, value):
        self.config.margin = value

    def _update_preview(self):
        self.color_preview.setStyleSheet(
            f"background-color: {self.config.color.name(QColor.HexArgb)}; border: 1px solid gray;"
        )

    def _apply(self):
        self.overlay.update_config(self.config)
        self.close()

