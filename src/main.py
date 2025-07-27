# main.py

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QMessageBox, QTextEdit
)
from PySide6.QtCore import Qt
from rect import RecordingOverlay
from rect_config import RectConfigWindow # NEW: Import the config window
from capture import capture_region
from ocr import ocr_image_to_text
from google_trans import translate_text


class ControlWindow(QWidget):
    def __init__(self, overlay):
        super().__init__()
        self.overlay = overlay
        self.setWindowTitle("OCR & Translate Control")
        self.setFixedSize(300, 500)

        layout = QVBoxLayout(self)

        # 1) Translate button
        self.btn = QPushButton("Translate", self)
        self.btn.clicked.connect(self.on_translate)
        layout.addWidget(self.btn)

        # 2) Original Japanese text (read-only)
        self.jp_text_edit = QTextEdit(self)
        self.jp_text_edit.setReadOnly(True)
        self.jp_text_edit.setPlaceholderText("Captured Japanese text will appear here...")
        layout.addWidget(self.jp_text_edit)

        # 3) Translated Traditional Chinese text (read-only)
        self.zh_text_edit = QTextEdit(self)
        self.zh_text_edit.setReadOnly(True)
        self.zh_text_edit.setPlaceholderText("Google Translate result will appear here...")
        layout.addWidget(self.zh_text_edit)

        layout.addStretch()

        # 4) Rect Config button
        self.rect_config_btn = QPushButton("Rect Config", self)
        self.rect_config_btn.clicked.connect(self.on_rect_config)
        layout.addWidget(self.rect_config_btn)

        # Keep a reference to the config window to prevent it from being garbage collected
        self.rect_config_window = None

    def on_translate(self):
        # grab overlay region
        geom = self.overlay.geometry()
        try:
            img = capture_region(geom.x(), geom.y(), geom.width(), geom.height())
        except Exception as e:
            QMessageBox.critical(self, "Capture Error", f"Failed to grab the screen:\n{e}")
            return

        try:
            # OCR → Japanese text
            jp_text = ocr_image_to_text(img).strip()
            if not jp_text:
                raise RuntimeError("No text detected in the selected region.")
            # translate → Traditional Chinese
            zh_text = translate_text(jp_text)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed during OCR/Translation:\n{e}")
            return

        # display results
        self.jp_text_edit.setPlainText(jp_text)
        self.zh_text_edit.setPlainText(zh_text)

    # NEW: Method to open the Rect Config window
    def on_rect_config(self):
        if self.rect_config_window is None:
            self.rect_config_window = RectConfigWindow(self.overlay)
        self.rect_config_window.show()
        # Bring the window to the front if it's already open
        self.rect_config_window.activateWindow()
        self.rect_config_window.raise_()
    # END NEW

    def closeEvent(self, event):
        # Ensure the config window is also closed if it's open
        if self.rect_config_window:
            self.rect_config_window.close()
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = RecordingOverlay()
    overlay.show()
    control = ControlWindow(overlay)
    control.show()
    sys.exit(app.exec())