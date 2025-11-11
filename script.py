# -*- coding: utf-8 -*-
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QGradient, QIcon, QImage, QKeySequence, QLinearGradient, QPainter, QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMenuBar, QPushButton, QSizePolicy, QSlider, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(300, 150)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.button_add_params = QPushButton(self.centralwidget)
        self.button_add_params.setObjectName(u"button_add_params")
        self.verticalLayout.addWidget(self.button_add_params)
        self.button_force_cook_displayed_node = QPushButton(self.centralwidget)
        self.button_force_cook_displayed_node.setObjectName(u"button_force_cook_displayed_node")
        self.verticalLayout.addWidget(self.button_force_cook_displayed_node)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.verticalLayout.addWidget(self.label)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 300, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.button_add_params.setText(QCoreApplication.translate("MainWindow", u"Add Button", None))
        self.button_force_cook_displayed_node.setText(QCoreApplication.translate("MainWindow", u"Force Cook Displayed Node", None))
        self.label.setText("")

import hou
from PySide6 import QtWidgets

PARAM_NAME_BUTTON: str = "button_force_cook"
PARAM_NAME_FOLDER: str = "folder_force_cook"

PARAM_NAMES: list[str] = [
    PARAM_NAME_BUTTON,
    PARAM_NAME_FOLDER,
]

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.__ui: Ui_MainWindow = Ui_MainWindow()
        self.__ui.setupUi(self)
        self.setWindowTitle("Force Cook Tool")

        self.__ui.button_add_params.clicked.connect(self.__button_add_params_clicked)
        self.__ui.button_force_cook_displayed_node.clicked.connect(self.__button_force_cook_displayed_node_clicked)

    def __button_add_params_clicked(self) -> None:
        for node_selected in hou.selectedNodes():
            ptg: hou.ParmTemplateGroup = node_selected.parmTemplateGroup()

            for param_name in PARAM_NAMES:
                param_template: hou.ParmTemplate = ptg.find(param_name)

                if param_template:
                    ptg.remove(param_template)

            param_template_button = hou.ButtonParmTemplate(
                PARAM_NAME_BUTTON,
                "Force Cook",
                script_callback="kwargs[\"node\"].cook(force=True)",
                script_callback_language=hou.scriptLanguage.Python)

            param_template_folder = hou.FolderParmTemplate(
                PARAM_NAME_FOLDER,
                "Force Cook",
                folder_type=hou.folderType.Collapsible)
            param_template_folder.addParmTemplate(param_template_button)
            ptg.append(param_template_folder)

            node_selected.setParmTemplateGroup(ptg)

    def __button_force_cook_displayed_node_clicked(self) -> None:
        network_editor: hou.NetworkEditor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)

        if not network_editor:
            return

        network: hou.Node = network_editor.pwd()

        displayed_node: hou.Node = None

        for child in network.children():
            if not hasattr(child, "isDisplayFlagSet"):
                continue

            if child.isDisplayFlagSet():
                displayed_node = child

                break

        if not displayed_node:
            return

        for input_ancestor in displayed_node.inputAncestors(follow_subnets=True):
            if not input_ancestor.inputs():
                input_ancestor.cook(force=True)

def show_main_window() -> None:
    main_window: MainWindow = MainWindow(hou.qt.mainWindow())
    main_window.show()

show_main_window()
