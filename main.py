from PyQt6.QtWidgets import QApplication
import sys
from main_window import MainWindow
from database import init_db

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    
    try:
        with open("style.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("style.qss file not found. Using default styling.")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())