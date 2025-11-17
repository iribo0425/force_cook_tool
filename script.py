# -*- coding: utf-8 -*-
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,QMetaObject, QObject, QPoint, QRect,QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,QFont, QFontDatabase, QGradient, QIcon,QImage, QKeySequence, QLinearGradient, QPainter,QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QLabel,QMainWindow, QMenuBar, QPushButton, QSizePolicy,QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(300, 226)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.button_add_params = QPushButton(self.centralwidget)
        self.button_add_params.setObjectName(u"button_add_params")
        self.verticalLayout.addWidget(self.button_add_params)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QSize(0, 2))
        self.frame.setMaximumSize(QSize(16777215, 2))
        self.frame.setFrameShape(QFrame.Shape.HLine)
        self.frame.setFrameShadow(QFrame.Shadow.Sunken)
        self.verticalLayout.addWidget(self.frame)
        self.button_force_cook_nodes = QPushButton(self.centralwidget)
        self.button_force_cook_nodes.setObjectName(u"button_force_cook_nodes")
        self.verticalLayout.addWidget(self.button_force_cook_nodes)
        self.check_box_save_cache_files = QCheckBox(self.centralwidget)
        self.check_box_save_cache_files.setObjectName(u"check_box_save_cache_files")
        self.verticalLayout.addWidget(self.check_box_save_cache_files)
        self.check_box_force_cook_referenced_nodes = QCheckBox(self.centralwidget)
        self.check_box_force_cook_referenced_nodes.setObjectName(u"check_box_force_cook_referenced_nodes")
        self.verticalLayout.addWidget(self.check_box_force_cook_referenced_nodes)
        self.check_box_log_messages = QCheckBox(self.centralwidget)
        self.check_box_log_messages.setObjectName(u"check_box_log_messages")
        self.verticalLayout.addWidget(self.check_box_log_messages)
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
        self.button_force_cook_nodes.setText(QCoreApplication.translate("MainWindow", u"Force Cook Display Node && Upstream Nodes", None))
        self.check_box_save_cache_files.setText(QCoreApplication.translate("MainWindow", u"Save Cache Files", None))
        self.check_box_force_cook_referenced_nodes.setText(QCoreApplication.translate("MainWindow", u"Force Cook Nodes Referenced By Object Merge", None))
        self.check_box_log_messages.setText(QCoreApplication.translate("MainWindow", u"Log Messages", None))
        self.label.setText("")

import hou
from enum import auto, Enum
from collections.abc import Sequence
from PySide6 import QtWidgets

PARAM_NAME_BUTTON: str = "button_force_cook"
PARAM_NAME_FOLDER: str = "folder_force_cook"

PARAM_NAMES: list[str] = [
    PARAM_NAME_BUTTON,
    PARAM_NAME_FOLDER,
]

def b_is_valid_index(sequence: Sequence, index: int) -> bool:
    try:
        sequence[index]
    except:
        return False

    return True

def b_is_object_merge(node: hou.Node) -> bool:
    return node.type().name() == "object_merge"

def b_is_file_cache(node: hou.Node) -> bool:
    return node.type().name() == "filecache::2.0"

def get_display_node(network: hou.Node) -> hou.Node:
    display_node: hou.Node = None

    for child in network.children():
        if hasattr(child, "isDisplayFlagSet")\
            and child.isDisplayFlagSet():
            display_node = child
            break

    return display_node

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.__ui: Ui_MainWindow = Ui_MainWindow()
        self.__ui.setupUi(self)
        self.setWindowTitle("Force Cook Tool")

        self.__ui.button_add_params.clicked.connect(self.__button_add_params_clicked)
        self.__ui.button_force_cook_nodes.clicked.connect(self.__button_force_cook_nodes_clicked)

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

    def __button_force_cook_nodes_clicked(self) -> None:
        network_editor: hou.NetworkEditor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)

        if not network_editor:
            return

        start_node: hou.Node = None
        network: hou.Node = network_editor.pwd()
        display_node: hou.Node = get_display_node(network)

        if b_is_file_cache(display_node):
            start_node = display_node
        elif display_node.isNetwork():
            start_node = get_display_node(display_node)

            if not start_node:
                start_node = display_node
        else:
            start_node = display_node

        self.__log_message(f"Start Node: {start_node.path()}")

        if not start_node:
            return

        self.__log_message("########## Get Children & Inputs ##########")

        b_save_cache_files: bool = self.__ui.check_box_save_cache_files.isChecked()
        b_force_cook_referenced_nodes: bool = self.__ui.check_box_force_cook_referenced_nodes.isChecked()

        discovered_nodes: list[hou.Node] = []
        stack: list[hou.Node] = []
        stack.append(start_node)

        while stack:
            current_node: hou.Node = stack.pop()
            self.__log_message(f"Current Node: {current_node.path()}")

            if current_node in discovered_nodes:
                continue

            discovered_nodes.append(current_node)
            self.__log_message(f"Appended {current_node.path()} to discovered nodes.")

            if b_is_file_cache(current_node)\
                and (not b_save_cache_files):
                continue

            if b_is_object_merge(current_node):
                if b_force_cook_referenced_nodes:
                    object_count: int = current_node.parm("numobj").eval()

                    for i in range(object_count):
                        b_is_enabled: bool = current_node.parm(f"enable{i + 1}").eval() == 1

                        if not b_is_enabled:
                            continue

                        object_path: str = current_node.parm(f"objpath{i + 1}").eval()
                        input_node: hou.Node = hou.node(object_path)

                        if b_is_file_cache(input_node):
                            stack.append(input_node)
                        elif input_node.isNetwork():
                            display_node_: hou.Node = get_display_node(input_node)

                            if display_node_:
                                stack.append(display_node_)
                            else:
                                stack.append(input_node)
                        else:
                            stack.append(input_node)
            else:
                for input_connection in current_node.inputConnections():
                    if b_is_file_cache(input_connection.inputNode()):
                        stack.append(input_connection.inputNode())
                    elif input_connection.inputNode().isNetwork():
                        if b_is_valid_index(input_connection.inputNode().subnetOutputs(), input_connection.outputIndex()):
                            input_node: hou.Node = input_connection.inputNode().subnetOutputs()[input_connection.outputIndex()]
                            stack.append(input_node)
                        else:
                            stack.append(input_connection.inputNode())
                    else:
                        stack.append(input_connection.inputNode())

        self.__log_message("##############################")
        self.__log_message("########## Force Cook & Save ##########")

        for discovered_node in reversed(discovered_nodes):
            if b_is_object_merge(discovered_node):
                if not b_force_cook_referenced_nodes:
                    discovered_node.cook(force=True)
                    self.__log_message(f"Force cooked {discovered_node.path()}.")
            elif b_is_file_cache(discovered_node):
                if b_save_cache_files:
                    discovered_node.parm("execute").pressButton()
                    self.__log_message(f"Saveed cache files at {discovered_node.path()}.")
                else:
                    discovered_node.cook(force=True)
                    self.__log_message(f"Force cooked {discovered_node.path()}.")
            else:
                if not discovered_node.inputConnections():
                    discovered_node.cook(force=True)
                    self.__log_message(f"Force cooked {discovered_node.path()}.")

        self.__log_message("##############################")

    def __log_message(self, *args, **kwargs) -> None:
        if self.__ui.check_box_log_messages.isChecked():
            print(*args, **kwargs)

def show_main_window() -> None:
    main_window: MainWindow = MainWindow(hou.qt.mainWindow())
    main_window.show()

show_main_window()
