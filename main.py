# main_app.py
import sys
from PyQt6.QtWidgets import QApplication
from app.main_window import QuizApp

def set_dark_theme(app):
    from PyQt6.QtGui import QPalette, QColor
    from PyQt6.QtCore import Qt
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53)); dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white); dark_palette.setColor(QPalette.ColorRole.Base, QColor(42, 42, 42)); dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53)); dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white); dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white); dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white); dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53)); dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white); dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red); dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218)); dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218)); dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
    app.setPalette(dark_palette)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    set_dark_theme(app)
    main_window = QuizApp()
    main_window.show()
    sys.exit(app.exec())