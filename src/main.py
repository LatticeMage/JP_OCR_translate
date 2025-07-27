# main.py
import sys
from PySide6.QtWidgets import QApplication
from rect import RecordingOverlay

if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = RecordingOverlay()
    overlay.show()
    sys.exit(app.exec())
