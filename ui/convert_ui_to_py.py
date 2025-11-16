# -*- coding: utf-8 -*-
import subprocess
import sys

def run(ui_file_path: str, py_file_path: str) -> None:
    temp_file_path: str = py_file_path.replace(".py", "_temp.py")
    subprocess.run(["pyside6-uic", ui_file_path, "-o", temp_file_path], check=True)

    with open(temp_file_path, "r", encoding="utf-8") as temp_file,\
        open(py_file_path, "w", encoding="utf-8") as py_file:

        import_statement0 = ""

        while True:
            line: str = temp_file.readline()

            if "from PySide6.QtCore" in line:
                while True:
                    import_statement0 += line.lstrip().replace("\n", "")

                    line: str = temp_file.readline()

                    if ")" in line:
                        import_statement0 += line.lstrip()

                        break
            
            if import_statement0:
                break

        py_file.write(import_statement0)

        import_statement1 = ""

        while True:
            line: str = temp_file.readline()

            if "from PySide6.QtGui" in line:
                while True:
                    import_statement1 += line.lstrip().replace("\n", "")

                    line: str = temp_file.readline()

                    if ")" in line:
                        import_statement1 += line.lstrip()

                        break
            
            if import_statement1:
                break

        py_file.write(import_statement1)

        import_statement2 = ""

        while True:
            line: str = temp_file.readline()

            if "from PySide6.QtWidgets" in line:
                while True:
                    import_statement2 += line.lstrip().replace("\n", "")

                    line: str = temp_file.readline()

                    if ")" in line:
                        import_statement2 += line.lstrip()

                        break
            
            if import_statement2:
                break

        py_file.write(import_statement2)
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
