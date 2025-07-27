# main.py
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QMessageBox, QTextEdit
)
from PySide6.QtCore import Qt
from rect import RecordingOverlay
from capture import capture_region
from ocr import ocr_image_to_text

class ControlWindow(QWidget):
    def __init__(self, overlay):
        super().__init__()
        self.overlay = overlay
        self.setWindowTitle("OCR Control")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout(self)

        # 1) Capture & OCR button
        self.btn = QPushButton("Capture & OCR", self)
        self.btn.clicked.connect(self.on_capture)
        layout.addWidget(self.btn)

        # 2) Text display (read-only)
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        # 3) Copy-to-clipboard button
        self.copy_btn = QPushButton("Copy Text", self)
        self.copy_btn.setEnabled(False)
        self.copy_btn.clicked.connect(self.copy_text)
        layout.addWidget(self.copy_btn)

        layout.addStretch()

    def on_capture(self):
        # grab overlay region
        geom = self.overlay.geometry()
        img = capture_region(geom.x(), geom.y(), geom.width(), geom.height())

        try:
            text = ocr_image_to_text(img)
        except Exception as e:
            QMessageBox.critical(self, "OCR Error", f"Failed to run OCR:\n{e}")
        else:
            # display in the text widget
            self.text_edit.setPlainText(text)
            self.copy_btn.setEnabled(bool(text))

    def copy_text(self):
        QApplication.clipboard().setText(self.text_edit.toPlainText())
        QMessageBox.information(self, "Copied", "Text copied to clipboard")

    def closeEvent(self, event):
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = RecordingOverlay()
    overlay.show()
    control = ControlWindow(overlay)
    control.show()
    sys.exit(app.exec())
