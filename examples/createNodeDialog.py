from PySide6 import QtWidgets, QtCore, QtGui

import types
from NodeGraphQt import (
    BaseNode,
)

class CreateNodeDialog(QtWidgets.QWidget):
    """a dialog for creating a new node."""

    def __init__(self, parent=None):
        super(CreateNodeDialog, self).__init__()
        self.parent = parent
        self.node_name = ""
        self.inPorts = {
            "name": [],
        }
        self.outPorts = {
            "name": [],
        }
        self.properties = {"name": [], "type": [], "default_value": [], "items": []}
        self.node = {
            "color": [13, 18, 23],
            "text_color": [255, 255, 255],
            "border_color": [74, 84, 86],
        }
        self.propertyTypes = ["lineEdit", "comboBox", "checkBox"]
        self._setupUi()

    def _setupUi(self):
        self.setWindowTitle("Create Node")
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.resize(600, 400)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setSpacing(0)

        self.type_wgt = QtWidgets.QLineEdit(self, text="node.custom")
        self.type_wgt.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.name_wgt = QtWidgets.QLineEdit(self, text="newNodeName")

        self.save_to_presets_btn = QtWidgets.QPushButton(
            "Save to Presets", self, clicked=self.saveToPresets
        )
        self.create_btn = QtWidgets.QPushButton("Create", self, clicked=self.createNode)
        self.tab_properties = QtWidgets.QTabWidget(self)
        self.tab_node = QtWidgets.QTabWidget(self)
        self.tab_node.setVisible(False)
        self.tab_Ports = QtWidgets.QTabWidget(self)

        name_layout = QtWidgets.QHBoxLayout()
        name_layout.addWidget(QtWidgets.QLabel("Node ID:"))
        name_layout.addWidget(self.type_wgt)
        name_layout.addWidget(QtWidgets.QLabel("."))
        name_layout.addWidget(self.name_wgt)
        name_layout.addStretch()
        name_layout.addWidget(self.save_to_presets_btn)
        name_layout.addWidget(self.create_btn)

        self.layout.setSpacing(4)
        self.layout.addLayout(name_layout)
        self.layout.addWidget(self.tab_Ports)
        self.layout.addWidget(self.tab_properties)
        self.layout.addWidget(self.tab_node)

        # properties tab
        self.widget_properties = QtWidgets.QWidget(self)
        self.property_table = QtWidgets.QTableWidget(self)
        self.property_table.setColumnCount(5)
        self.property_table.setHorizontalHeaderLabels(
            ["Name", "Type", "Default Value", "Possiable Values", " "]
        )
        self.property_table.horizontalHeader().setStretchLastSection(True)
        self.property_table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch
        )
        add_btn = QtWidgets.QPushButton(
            "Add",
            icon=QtGui.QIcon("icon/add.png"),
            parent=self,
            clicked=self.addProperties,
        )
        add_btn.setFixedWidth(200)

        # add button to widget properties
        layout = QtWidgets.QVBoxLayout(self.widget_properties)
        layout.addWidget(add_btn)
        layout.addWidget(self.property_table)

        layout.addStretch()
        self.tab_properties.addTab(self.widget_properties, "Properties")

        # ports tab
        self.widget_Ports = QtWidgets.QWidget(self)
        layout = QtWidgets.QHBoxLayout(self.widget_Ports)

        inPorts_layout = QtWidgets.QVBoxLayout()
        inPorts_layout.addWidget(QtWidgets.QLabel("Input Ports"))
        self.inPorts_table = QtWidgets.QTableWidget(self)
        self.inPorts_table.setColumnCount(2)
        self.inPorts_table.setHorizontalHeaderLabels(["Name", ""])
        self.inPorts_table.horizontalHeader().setStretchLastSection(True)
        self.inPorts_table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch
        )
        inPorts_layout.addWidget(self.inPorts_table)
        add_inport_btn = QtWidgets.QPushButton(
            "Add", icon=QtGui.QIcon("icon/add.png"), parent=self
        )
        add_inport_btn.clicked.connect(lambda: self.addPort("in"))
        inPorts_layout.addWidget(add_inport_btn)
        layout.addLayout(inPorts_layout)

        outPorts_layout = QtWidgets.QVBoxLayout()
        outPorts_layout.addWidget(QtWidgets.QLabel("Output Ports"))
        self.outPorts_table = QtWidgets.QTableWidget(self)
        self.outPorts_table.setColumnCount(2)
        self.outPorts_table.setHorizontalHeaderLabels(["Name", ""])
        self.outPorts_table.horizontalHeader().setStretchLastSection(True)
        self.outPorts_table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch
        )
        outPorts_layout.addWidget(self.outPorts_table)
        add_oport_btn = QtWidgets.QPushButton(
            "Add", icon=QtGui.QIcon("icon/add.png"), parent=self
        )
        add_oport_btn.clicked.connect(lambda: self.addPort("out"))
        outPorts_layout.addWidget(add_oport_btn)
        layout.addLayout(outPorts_layout)

        self.tab_Ports.addTab(self.widget_Ports, "Ports")

        # node tab
        self.widget_node = QtWidgets.QWidget(self)
        layout = QtWidgets.QVBoxLayout(
            self.widget_node, spacing=3, contentsMargins=QtCore.QMargins(0, 3, 3, 0)
        )
        self.widget_node.setVisible(False)

        color_layout = QtWidgets.QHBoxLayout()
        color_label = QtWidgets.QLabel("Color:")
        color_label.setFixedWidth(80)
        color_layout.addWidget(color_label)
        color_btn = QtWidgets.QPushButton("", self)
        color_btn.setFixedSize(50, 30)
        color_btn.setStyleSheet(
            f"background-color: rgb({self.node['color'][0]}, {self.node['color'][1]}, {self.node['color'][2]})"
        )
        color_btn.clicked.connect(lambda: self.pickColor("node_color"))
        color_layout.addWidget(color_btn)
        self.node_color_r = QtWidgets.QLineEdit(self, text=f'{self.node["color"][0]}')
        self.node_color_r.setValidator(QtGui.QIntValidator(0, 255))
        self.node_color_r.textChanged.connect(
            lambda: {
                self.node_color_r.setText(
                    str(min(255, self._to_int(self.node_color_r.text())))
                ),
                color_btn.setStyleSheet(
                    f"background-color: rgb({self.node_color_r.text()}, {self.node_color_g.text()}, {self.node_color_b.text()})"
                ),
            }
        )
        self.node_color_g = QtWidgets.QLineEdit(self, text=f'{self.node["color"][1]}')
        self.node_color_g.setValidator(QtGui.QIntValidator(0, 255))
        self.node_color_g.textChanged.connect(
            lambda: {
                self.node_color_g.setText(
                    str(min(255, self._to_int(self.node_color_g.text())))
                ),
                color_btn.setStyleSheet(
                    f"background-color: rgb({self.node_color_r.text()}, {self.node_color_g.text()}, {self.node_color_b.text()})"
                ),
            }
        )
        self.node_color_b = QtWidgets.QLineEdit(self, text=f'{self.node["color"][2]}')
        self.node_color_b.setValidator(QtGui.QIntValidator(0, 255))
        self.node_color_b.textChanged.connect(
            lambda: {
                self.node_color_b.setText(
                    str(min(255, self._to_int(self.node_color_b.text())))
                ),
                color_btn.setStyleSheet(
                    f"background-color: rgb({self.node_color_r.text()}, {self.node_color_g.text()}, {self.node_color_b.text()})"
                ),
            }
        )
        color_layout.addWidget(self.node_color_r)
        color_layout.addWidget(self.node_color_g)
        color_layout.addWidget(self.node_color_b)
        layout.addLayout(color_layout)

        text_color_layout = QtWidgets.QHBoxLayout()
        text_color_label = QtWidgets.QLabel("Text Color:")
        text_color_label.setFixedWidth(80)
        text_color_layout.addWidget(text_color_label)
        text_color_btn = QtWidgets.QPushButton("", self)
        text_color_btn.setFixedSize(50, 30)
        text_color_btn.setStyleSheet(
            f"background-color: rgb({self.node['text_color'][0]}, {self.node['text_color'][1]}, {self.node['text_color'][2]})"
        )
        text_color_btn.clicked.connect(lambda: self.pickColor("text_color"))
        text_color_layout.addWidget(text_color_btn)
        self.text_node_color_r = QtWidgets.QLineEdit(
            self, text=f'{self.node["text_color"][0]}'
        )
        self.text_node_color_r.setValidator(QtGui.QIntValidator(0, 255))
        # connect the textChanged signal to the setText method and change the text_color_btn background color
        self.text_node_color_r.textChanged.connect(
            lambda: {
                self.text_node_color_r.setText(
                    str(min(255, self._to_int(self.text_node_color_r.text())))
                ),
                text_color_btn.setStyleSheet(
                    f"background-color: rgb({self.text_node_color_r.text()}, {self.text_node_color_g.text()}, {self.text_node_color_b.text()})"
                ),
            }
        )
        self.text_node_color_g = QtWidgets.QLineEdit(
            self, text=f'{self.node["text_color"][1]}'
        )
        self.text_node_color_g.setValidator(QtGui.QIntValidator(0, 255))
        self.text_node_color_g.textChanged.connect(
            lambda: {
                self.text_node_color_g.setText(
                    str(min(255, self._to_int(self.text_node_color_g.text())))
                ),
                text_color_btn.setStyleSheet(
                    f"background-color: rgb({self.text_node_color_g.text()}, {self.text_node_color_g.text()}, {self.text_node_color_b.text()})"
                ),
            }
        )
        self.text_node_color_b = QtWidgets.QLineEdit(
            self, text=f'{self.node["text_color"][2]}'
        )
        self.text_node_color_b.setValidator(QtGui.QIntValidator(0, 255))
        self.text_node_color_b.textChanged.connect(
            lambda: {
                self.text_node_color_g.setText(
                    str(min(255, self._to_int(self.text_node_color_g.text())))
                ),
                text_color_btn.setStyleSheet(
                    f"background-color: rgb({self.text_node_color_b.text()}, {self.text_node_color_g.text()}, {self.text_node_color_b.text()})"
                ),
            }
        )
        text_color_layout.addWidget(self.text_node_color_r)
        text_color_layout.addWidget(self.text_node_color_g)
        text_color_layout.addWidget(self.text_node_color_b)
        layout.addLayout(text_color_layout)

        border_color_layout = QtWidgets.QHBoxLayout()
        border_color_label = QtWidgets.QLabel("border Color:")
        border_color_label.setFixedWidth(80)
        border_color_layout.addWidget(border_color_label)
        border_color_btn = QtWidgets.QPushButton("", self)
        border_color_btn.setFixedSize(50, 30)
        border_color_btn.setStyleSheet(
            f"background-color: rgb({self.node['border_color'][0]}, {self.node['border_color'][1]}, {self.node['border_color'][2]})"
        )
        border_color_btn.clicked.connect(lambda: self.pickColor("border_color"))
        border_color_layout.addWidget(border_color_btn)
        self.border_node_color_r = QtWidgets.QLineEdit(
            self, text=f'{self.node["border_color"][0]}'
        )
        self.border_node_color_r.setValidator(QtGui.QIntValidator(0, 255))
        self.border_node_color_r.textChanged.connect(
            lambda: {
                self.text_node_color_r.setText(
                    str(min(255, self._to_int(self.text_node_color_r.text())))
                ),
                border_color_btn.setStyleSheet(
                    f"background-color: rgb({self.border_node_color_r.text()}, {self.border_node_color_g.text()}, {self.border_node_color_b.text()})"
                ),
            }
        )
        self.border_node_color_g = QtWidgets.QLineEdit(
            self, text=f'{self.node["border_color"][1]}'
        )
        self.border_node_color_g.setValidator(QtGui.QIntValidator(0, 255))
        self.border_node_color_g.textChanged.connect(
            lambda: {
                self.text_node_color_g.setText(
                    str(min(255, self._to_int(self.text_node_color_g.text())))
                ),
                border_color_btn.setStyleSheet(
                    f"background-color: rgb({self.border_node_color_g.text()}, {self.border_node_color_g.text()}, {self.border_node_color_b.text()})"
                ),
            }
        )
        self.border_node_color_b = QtWidgets.QLineEdit(
            self, text=f'{self.node["border_color"][2]}'
        )
        self.border_node_color_b.setValidator(QtGui.QIntValidator(0, 255))
        self.border_node_color_b.textChanged.connect(
            lambda: {
                self.text_node_color_b.setText(
                    str(min(255, self._to_int(self.text_node_color_b.text())))
                ),
                border_color_btn.setStyleSheet(
                    f"background-color: rgb({self.border_node_color_b.text()}, {self.border_node_color_g.text()}, {self.border_node_color_b.text()})"
                ),
            }
        )
        border_color_layout.addWidget(self.border_node_color_r)
        border_color_layout.addWidget(self.border_node_color_g)
        border_color_layout.addWidget(self.border_node_color_b)
        layout.addLayout(border_color_layout)

        self.tab_node.addTab(self.widget_node, "Node")

    def _to_int(self, s):
        try:
            return int(s)
        except ValueError:
            return 0

    def isidentifier(self):
        return self.node_name.isidentifier()

    def _createCustomNode(
        self,
        nodeType: str,
        nodeName: str,
        inputPorts: any,
        outputPorts: any,
        elementDict: any,
        colors: any,
    ):
        # check if the node name is valid name for a class
        if not nodeName.isidentifier():
            raise ValueError("Invalid node name, must be a valid python class name")
        code_str = "def __init__(self):\n\t\tsuper(type(self), self).__init__()\n"
        for inputPort in inputPorts["name"]:
            code_str = f"{code_str}\t\tself.add_input(name='{inputPort}')\n"

        for outputPort in outputPorts["name"]:
            code_str = f"{code_str}\t\tself.add_output(name='{outputPort}')\n"

        for e in zip(
            elementDict["name"],
            elementDict["type"],
            elementDict["default_value"],
            elementDict["items"],
        ):
            if e[1] == "lineEdit":
                code_str = (
                    f"{code_str}\t\tself.add_text_input(name='{e[0]}',"
                    + f"label='{e[0]}',"
                    + f"text='{e[2]}',"
                    + f"tooltip=None,"
                    + f"tab=None)\n"
                )
            elif e[1] == "comboBox":
                code_str = (
                    f"{code_str}\t\tself.add_combo_menu(name='{e[0]}',"
                    + f"label='{e[0]}',"
                    + f"items={e[3]},"
                    + f"tooltip=None,"
                    + f"tab=None)\n"
                )
            elif e[1] == "checkBox":
                code_str = (
                    f"{code_str}\t\tself.add_checkbox(name='{e[0]}',"
                    + f"label='',"
                    + f"text='{e[0]}',"
                    + f"state={e[2]},"
                    + f"tooltip=None,"
                    + f"tab=None)\n"
                )

        create_code = compile(
            code_str,
            "<string>",
            "exec",
        )
        func = types.FunctionType(create_code.co_consts[0], globals(), "func")
        newNodeClass = type(
            nodeName,
            (BaseNode,),
            {
                "__identifier__": nodeType,
                "NODE_NAME": nodeName,
                "__init__": func,
            },
        )
        return newNodeClass

    def _generateCreateNodeCode(
        self,
        nodeType: str,
        nodeName: str,
        inputPorts: any,
        outputPorts: any,
        elementDict: any,
        colors: any,
    ):
        code_str = "def __init__(self):\n\t\tsuper(" + nodeName + ", self).__init__()\n"
        for inputPort in inputPorts["name"]:
            code_str = f"{code_str}\t\tself.add_input(name='{inputPort}')\n"

        for outputPort in outputPorts["name"]:
            code_str = f"{code_str}\t\tself.add_output(name='{outputPort}')\n"

        for e in zip(
            elementDict["name"],
            elementDict["type"],
            elementDict["default_value"],
            elementDict["items"],
        ):
            if e[1] == "lineEdit":
                code_str = (
                    f"{code_str}\t\tself.add_text_input(name='{e[0]}',"
                    + f"label='{e[0]}',"
                    + f"text='{e[2]}',"
                    + f"tooltip=None,"
                    + f"tab=None)\n"
                )
            elif e[1] == "comboBox":
                code_str = (
                    f"{code_str}\t\tself.add_combo_menu(name='{e[0]}',"
                    + f"label='{e[0]}',"
                    + f"items={e[3]},"
                    + f"tooltip=None,"
                    + f"tab=None)\n"
                )
            elif e[1] == "checkBox":
                code_str = (
                    f"{code_str}\t\tself.add_checkbox(name='{e[0]}',"
                    + f"label='',"
                    + f"text='{e[0]}',"
                    + f"state={e[2]},"
                    + f"tooltip=None,"
                    + f"tab=None)\n"
                )

        return f"class {nodeName}(BaseNode):\n\t__identifier__ = '{nodeType}'\n\tNODE_NAME = '{nodeName}'\n\t{code_str}"

    def _updatePrpertyWidget(self):

        # clear the table items
        self.property_table.clear()
        self.property_table.setRowCount(0)
        self.property_table.setHorizontalHeaderLabels(
            ["Name", "Type", "Default Value", "Possiable Values", " "]
        )

        itemNum = len(self.properties["name"])
        self.property_table.setRowCount(itemNum)
        for i in range(itemNum):
            # self.property_table.setItem(
            #     i, 0, QtWidgets.QTableWidgetItem(self.properties["display_name"][i])
            # )
            self.property_table.setItem(
                i, 0, QtWidgets.QTableWidgetItem(self.properties["name"][i])
            )

            combo = QtWidgets.QComboBox()
            for t in self.propertyTypes:
                combo.addItem(t)
            combo.setCurrentText(self.properties["type"][i])
            self.property_table.setCellWidget(i, 1, combo)

            self.property_table.setItem(
                i, 2, QtWidgets.QTableWidgetItem(self.properties["default_value"][i])
            )
            self.property_table.setItem(
                i, 3, QtWidgets.QTableWidgetItem(self.properties["items"][i])
            )
            # add a button to delete the current item, the clicked signal is connected to the deleteProperty method, and the index is passed as an argument
            btn = QtWidgets.QPushButton(
                "Delete",
                icon=QtGui.QIcon("icon/bin.png"),
                clicked=lambda checked, i=i: self.deleteProperty(i),
            )
            self.property_table.setCellWidget(i, 4, btn)

    @QtCore.Slot()
    def addProperties(self):
        # add items in to  self.properties, and update the properties widget
        # self.properties["display_name"].append(
        #     f'text_{len(self.properties["display_name"])}'
        # )
        self.properties["name"].append(f'property_{len(self.properties["name"])}')
        self.properties["type"].append("lineEdit")
        self.properties["default_value"].append("")
        self.properties["items"].append("")
        self._updatePrpertyWidget()

    @QtCore.Slot()
    def addPort(self, portType: str):
        # add a port to the input or output ports
        if portType == "in":
            # self.inPorts["display_name"].append(
            #     f'in_{len(self.inPorts["display_name"])}'
            # )
            self.inPorts["name"].append(f'in_{len(self.inPorts["name"])}')
        else:
            # self.outPorts["display_name"].append(
            #     f'out_{len(self.outPorts["display_name"])}'
            # )
            self.outPorts["name"].append(f'out_{len(self.outPorts["name"])}')

        self._updatePortWidget(portType)

    def _updatePortWidget(self, portType="in"):
        if portType == "in":
            self.inPorts_table.clear()
            self.inPorts_table.setRowCount(0)
            self.inPorts_table.setHorizontalHeaderLabels(["Name", ""])
            itemNum = len(self.inPorts["name"])
            self.inPorts_table.setRowCount(itemNum)
            for i in range(itemNum):
                # self.inPorts_table.setItem(
                #     i, 0, QtWidgets.QTableWidgetItem(self.inPorts["display_name"][i])
                # )
                self.inPorts_table.setItem(
                    i, 0, QtWidgets.QTableWidgetItem(self.inPorts["name"][i])
                )
                btn = QtWidgets.QPushButton(
                    "Delete",
                    icon=QtGui.QIcon("icon/bin.png"),
                    clicked=lambda checked, i=i: self.deletePort(i, portType),
                )
                self.inPorts_table.setCellWidget(i, 1, btn)
        else:
            self.outPorts_table.clear()
            self.outPorts_table.setRowCount(0)
            self.outPorts_table.setHorizontalHeaderLabels(["Name", ""])
            itemNum = len(self.outPorts["name"])
            self.outPorts_table.setRowCount(itemNum)
            for i in range(itemNum):
                # self.outPorts_table.setItem(
                #     i, 0, QtWidgets.QTableWidgetItem(self.outPorts["display_name"][i])
                # )
                self.outPorts_table.setItem(
                    i, 0, QtWidgets.QTableWidgetItem(self.outPorts["name"][i])
                )
                btn = QtWidgets.QPushButton(
                    "Delete",
                    icon=QtGui.QIcon("icon/bin.png"),
                    clicked=lambda checked, i=i: self.deletePort(i, portType),
                )
                self.outPorts_table.setCellWidget(i, 1, btn)

    @QtCore.Slot()
    def updatePropertiesWidgetType(self):
        # update the properties widget based on the selected type in the dropdown menu
        pass

    @QtCore.Slot()
    def deleteProperty(self, index: int):
        # delete the property at the index
        # self.properties["display_name"].pop(index)
        self.properties["name"].pop(index)
        self.properties["type"].pop(index)
        self.properties["default_value"].pop(index)
        self.properties["items"].pop(index)

        self._updatePrpertyWidget()

    @QtCore.Slot()
    def deletePort(self, index: int, portType: str):
        # delete the port at the index
        if portType == "in":
            # self.inPorts["display_name"].pop(index)
            self.inPorts["name"].pop(index)
        else:
            # self.outPorts["display_name"].pop(index)
            self.outPorts["name"].pop(index)
        self._updatePortWidget(portType)

    @QtCore.Slot()
    def pickColor(self, colorType: str):
        # open a color picker dialog, and set the color to the selected color
        color_picker = QtWidgets.QColorDialog()
        color = color_picker.getColor()
        if color.isValid():
            if colorType == "node_color":
                self.node["color"] = [color.red(), color.green(), color.blue()]
                self.node_color_r.setText(str(color.red()))
                self.node_color_g.setText(str(color.green()))
                self.node_color_b.setText(str(color.blue()))
            elif colorType == "text_color":
                self.node["text_color"] = [color.red(), color.green(), color.blue()]
                self.text_node_color_r.setText(str(color.red()))
                self.text_node_color_g.setText(str(color.green()))
                self.text_node_color_b.setText(str(color.blue()))
            else:
                self.node["border_color"] = [color.red(), color.green(), color.blue()]
                self.border_node_color_r.setText(str(color.red()))
                self.border_node_color_g.setText(str(color.green()))
                self.border_node_color_b.setText(str(color.blue()))

    @QtCore.Slot()
    def saveToPresets(self):
        nodeCode = self._generateCreateNodeCode(
            self.type_wgt.text(),
            self.name_wgt.text(),
            self.inPorts,
            self.outPorts,
            self.properties,
            self.node,
        )
        print(nodeCode)

    @QtCore.Slot()
    def createNode(self):
        nodeClass = self._createCustomNode(
            self.type_wgt.text(),
            self.name_wgt.text(),
            self.inPorts,
            self.outPorts,
            self.properties,
            self.node,
        )
        nodeID = f"{self.type_wgt.text()}.{self.name_wgt.text()}"
        # check if the node is already registered
        if nodeID in self.parent.graph.registered_nodes():
            # show a message box that the node is already registered
            QtWidgets.QMessageBox.warning(
                self,
                "Node Already Registered",
                f"The node {nodeID} is already registered",
            )
            return
        # register the node
        self.parent.graph.register_node(nodeClass)
        # create node with custom text color and disable it.
        self.parent.graph.create_node(
            f"{self.type_wgt.text()}.{self.name_wgt.text()}", name=self.name_wgt.text()
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    dialog = CreateNodeDialog()
    dialog.show()
    sys.exit(app.exec())
