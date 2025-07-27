# main.py
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from rect import RecordingOverlay
from capture import capture_region

if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = RecordingOverlay()
    overlay.show()

    def grab_and_save():
        geom = overlay.geometry()
        x, y = geom.x(), geom.y()
        w, h = geom.width(), geom.height()
        capture_region(x, y, w, h, "now.png")

    # Call grab_and_save() every 1000 ms
    timer = QTimer()
    timer.timeout.connect(grab_and_save)
    timer.start(1000)

    sys.exit(app.exec())
