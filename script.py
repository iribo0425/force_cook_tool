# -*- coding: utf-8 -*-
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,QMetaObject, QObject, QPoint, QRect,QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,QFont, QFontDatabase, QGradient, QIcon,QImage, QKeySequence, QLinearGradient, QPainter,QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QLabel, QMainWindow,QMenuBar, QPushButton, QSizePolicy, QStatusBar,QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(300, 200)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.button_add_params = QPushButton(self.centralwidget)
        self.button_add_params.setObjectName(u"button_add_params")
        self.verticalLayout.addWidget(self.button_add_params)
        self.button_force_cook_display_node = QPushButton(self.centralwidget)
        self.button_force_cook_display_node.setObjectName(u"button_force_cook_display_node")
        self.verticalLayout.addWidget(self.button_force_cook_display_node)
        self.check_box_save_cache_files = QCheckBox(self.centralwidget)
        self.check_box_save_cache_files.setObjectName(u"check_box_save_cache_files")
        self.verticalLayout.addWidget(self.check_box_save_cache_files)
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
        self.button_force_cook_display_node.setText(QCoreApplication.translate("MainWindow", u"Force Cook Display Node", None))
        self.check_box_save_cache_files.setText(QCoreApplication.translate("MainWindow", u"Save Cache Files", None))
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

def b_is_filecache(node: hou.Node) -> bool:
    return node.type().name() == "filecache::2.0"

class NodeOpType(Enum):
    FORCE_COOK = auto()
    SAVE_CACHE_FILES = auto()

class NodeOp(object):
    def __init__(self, node: hou.Node, t: NodeOpType):
        super(NodeOp, self).__init__()

        self.node: hou.Node = node
        self.type: NodeOpType = t

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.__ui: Ui_MainWindow = Ui_MainWindow()
        self.__ui.setupUi(self)
        self.setWindowTitle("Force Cook Tool")

        self.__ui.button_add_params.clicked.connect(self.__button_add_params_clicked)
        self.__ui.button_force_cook_display_node.clicked.connect(self.__button_force_cook_display_node_clicked)

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

    def __button_force_cook_display_node_clicked(self) -> None:
        network_editor: hou.NetworkEditor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)

        if not network_editor:
            return

        network: hou.Node = network_editor.pwd()

        display_node: hou.Node = network_editor.pwd()

        for child in network.children():
            if not hasattr(child, "isDisplayFlagSet"):
                continue

            if child.isDisplayFlagSet():
                display_node = child
                break

        if not display_node:
            return

        b_save_cache_files = self.__ui.check_box_save_cache_files.isChecked()

        node_ops: list[NodeOp] = []
        stack: list[hou.Node] = []
        stack.append(display_node)
        discovered_nodes: list[hou.Node] = []

        while stack:
            current_node: hou.Node = stack.pop()
            discovered_nodes.append(current_node)

            b_can_add_node_op: bool = True

            for node_op in node_ops:
                if node_op.node == current_node:
                    b_can_add_node_op = False
                    break

            if b_can_add_node_op:
                if current_node.inputConnections():
                    if b_is_filecache(current_node):
                        if b_save_cache_files:
                            node_op: NodeOp = NodeOp(current_node, NodeOpType.SAVE_CACHE_FILES)
                            node_ops.append(node_op)
                        else:
                            node_op: NodeOp = NodeOp(current_node, NodeOpType.FORCE_COOK)
                            node_ops.append(node_op)
                            continue
                else:
                    node_op: NodeOp = NodeOp(current_node, NodeOpType.FORCE_COOK)
                    node_ops.append(node_op)

            for input_connection in current_node.inputConnections():
                if input_connection.inputNode().isNetwork():
                    if b_is_filecache(input_connection.inputNode()):
                        if not input_connection.inputNode() in discovered_nodes:
                            stack.append(input_connection.inputNode())
                    else:
                        if b_is_valid_index(input_connection.inputNode().subnetOutputs(), input_connection.outputIndex()):
                            input_node = input_connection.inputNode().subnetOutputs()[input_connection.outputIndex()]

                            if not input_node in discovered_nodes:
                                stack.append(input_node)
                        else:
                            if not input_connection.inputNode() in discovered_nodes:
                                stack.append(input_node)
                else:
                    if not input_connection.inputNode() in discovered_nodes:
                        stack.append(input_connection.inputNode())

        for node_op in reversed(node_ops):
            if node_op.type == NodeOpType.FORCE_COOK:
                node_op.node.cook(force=True)
            elif node_op.type == NodeOpType.SAVE_CACHE_FILES:
                node_op.node.parm("execute").pressButton()

def show_main_window() -> None:
    main_window: MainWindow = MainWindow(hou.qt.mainWindow())
    main_window.show()

show_main_window()
