# -*- coding: utf-8 -*-
import subprocess
import sys

def run(ui_file_path: str, py_file_path: str) -> None:
    temp_file_path: str = py_file_path.replace(".py", "_temp.py")
    subprocess.run(["pyside6-uic", ui_file_path, "-o", temp_file_path], check=True)

    with open(temp_file_path, "r", encoding="utf-8") as temp_file,\
        open(py_file_path, "w", encoding="utf-8") as py_file:
        py_file.write("from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)\n")
        py_file.write("from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QGradient, QIcon, QImage, QKeySequence, QLinearGradient, QPainter, QPalette, QPixmap, QRadialGradient, QTransform)\n")
        py_file.write("from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMenuBar, QPushButton, QSizePolicy, QSlider, QStatusBar, QVBoxLayout, QWidget)\n")
        py_file.write("\n")

        while True:
            line: str = temp_file.readline()

            if "class" in line:
                break

        while line:
            py_file.write(line)

            if "# setupUi" in line:
                py_file.write("\n")

            while line:
                line = temp_file.readline()

                if "#" in line:
                    line = "\n"

                    break

                if "\n" != line:
                    break

if __name__ == "__main__":
    ui_file_path = sys.argv[1]
    py_file_path = sys.argv[2]
    run(ui_file_path, py_file_path)
