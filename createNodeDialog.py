from PySide6 import QtWidgets, QtCore, QtGui
import inspect
import types
from NodeGraphQt import (
    BaseNode,
    NodeGraph,
    PropertiesBinWidget,
    NodesTreeWidget,
    NodesPaletteWidget,
)


class CreateNodeDialog(QtWidgets.QWidget):
    """a dialog for creating a new node."""

    def __init__(self, parent=None):
        super(CreateNodeDialog, self).__init__()
        self.node_name = ""
        self.inPorts = {
            "display_name": [],
            "name": [],
        }
        self.outPorts = {
            "display_name": [],
            "name": [],
        }
        self.properties = {"display_name": [], "name": [], "type": [], "value": []}
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
        self.resize(680, 600)
        self.layout = QtWidgets.QVBoxLayout(self)

        self.name_wgt = QtWidgets.QLineEdit(self)
        self.save_to_presets_btn = QtWidgets.QPushButton("Save to Presets", self, clicked=self.saveToPresets)
        self.create_btn = QtWidgets.QPushButton("Create", self, clicked=self.createNode)
        self.tab_properties = QtWidgets.QTabWidget(self)
        self.tab_node = QtWidgets.QTabWidget(self)
        self.tab_Ports = QtWidgets.QTabWidget(self)

        name_layout = QtWidgets.QHBoxLayout()
        name_layout.addWidget(QtWidgets.QLabel("Name:"))
        name_layout.addWidget(self.name_wgt)
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
            ["Display name", "Name", "Type", "Value", " "]
        )
        self.property_table.horizontalHeader().setStretchLastSection(True)
        self.property_table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch
        )
        add_btn = QtWidgets.QPushButton("Add", icon=QtGui.QIcon("icon/add.png"),parent=self, clicked=self.addProperties)
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
        self.inPorts_table.setColumnCount(3)
        self.inPorts_table.setHorizontalHeaderLabels(["Display name", "Name", ""])
        self.inPorts_table.horizontalHeader().setStretchLastSection(True)
        self.inPorts_table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch
        )
        inPorts_layout.addWidget(self.inPorts_table)
        add_inport_btn = QtWidgets.QPushButton("Add", icon=QtGui.QIcon("icon/add.png"),parent=self)
        add_inport_btn.clicked.connect(lambda: self.addPort("in"))
        inPorts_layout.addWidget(add_inport_btn)
        layout.addLayout(inPorts_layout)

        outPorts_layout = QtWidgets.QVBoxLayout()
        outPorts_layout.addWidget(QtWidgets.QLabel("Output Ports"))
        self.outPorts_table = QtWidgets.QTableWidget(self)
        self.outPorts_table.setColumnCount(3)
        self.outPorts_table.setHorizontalHeaderLabels(["Display name", "Name", ""])
        self.outPorts_table.horizontalHeader().setStretchLastSection(True)
        self.outPorts_table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch
        )
        outPorts_layout.addWidget(self.outPorts_table)
        add_oport_btn = QtWidgets.QPushButton("Add",icon=QtGui.QIcon("icon/add.png"),parent=self)
        add_oport_btn.clicked.connect(lambda: self.addPort("out"))
        outPorts_layout.addWidget(add_oport_btn)
        layout.addLayout(outPorts_layout)

        self.tab_Ports.addTab(self.widget_Ports, "Ports")

        # node tab
        self.widget_node = QtWidgets.QWidget(self)
        layout = QtWidgets.QVBoxLayout(
            self.widget_node, spacing=3, contentsMargins=QtCore.QMargins(0, 3, 3, 0)
        )

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
        self.node_color_r.textChanged.connect(lambda: {self.node_color_r.setText(str(min(255,self._to_int(self.node_color_r.text())))),
                                                        color_btn.setStyleSheet(f"background-color: rgb({self.node_color_r.text()}, {self.node_color_g.text()}, {self.node_color_b.text()})")})   
        self.node_color_g = QtWidgets.QLineEdit(self, text=f'{self.node["color"][1]}')
        self.node_color_g.setValidator(QtGui.QIntValidator(0, 255))
        self.node_color_g.textChanged.connect(lambda: {self.node_color_g.setText(str(min(255,self._to_int(self.node_color_g.text())))),
                                                        color_btn.setStyleSheet(f"background-color: rgb({self.node_color_r.text()}, {self.node_color_g.text()}, {self.node_color_b.text()})")} )
        self.node_color_b = QtWidgets.QLineEdit(self, text=f'{self.node["color"][2]}')
        self.node_color_b.setValidator(QtGui.QIntValidator(0, 255))
        self.node_color_b.textChanged.connect(lambda: {self.node_color_b.setText(str(min(255,self._to_int(self.node_color_b.text())))),
                                                        color_btn.setStyleSheet(f"background-color: rgb({self.node_color_r.text()}, {self.node_color_g.text()}, {self.node_color_b.text()})")} )
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
        self.text_node_color_r.textChanged.connect(lambda: {self.text_node_color_r.setText(str(min(255,self._to_int(self.text_node_color_r.text())))),
                                                            text_color_btn.setStyleSheet(f"background-color: rgb({self.text_node_color_r.text()}, {self.text_node_color_g.text()}, {self.text_node_color_b.text()})")})
        self.text_node_color_g = QtWidgets.QLineEdit(
            self, text=f'{self.node["text_color"][1]}'
        )
        self.text_node_color_g.setValidator(QtGui.QIntValidator(0, 255))
        self.text_node_color_g.textChanged.connect(lambda: {self.text_node_color_g.setText(str(min(255,self._to_int(self.text_node_color_g.text())))),
                                                            text_color_btn.setStyleSheet(f"background-color: rgb({self.text_node_color_g.text()}, {self.text_node_color_g.text()}, {self.text_node_color_b.text()})")})
        self.text_node_color_b = QtWidgets.QLineEdit(
            self, text=f'{self.node["text_color"][2]}'
        )
        self.text_node_color_b.setValidator(QtGui.QIntValidator(0, 255))
        self.text_node_color_b.textChanged.connect(lambda: {self.text_node_color_g.setText(str(min(255,self._to_int(self.text_node_color_g.text())))),
                                                            text_color_btn.setStyleSheet(f"background-color: rgb({self.text_node_color_b.text()}, {self.text_node_color_g.text()}, {self.text_node_color_b.text()})")})        
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
        self.border_node_color_r.textChanged.connect(lambda: {self.text_node_color_r.setText(str(min(255,self._to_int(self.text_node_color_r.text())))),
                                                              border_color_btn.setStyleSheet(f"background-color: rgb({self.border_node_color_r.text()}, {self.border_node_color_g.text()}, {self.border_node_color_b.text()})")} )  
        self.border_node_color_g = QtWidgets.QLineEdit(
            self, text=f'{self.node["border_color"][1]}'
        )
        self.border_node_color_g.setValidator(QtGui.QIntValidator(0, 255))
        self.border_node_color_g.textChanged.connect(lambda: {self.text_node_color_g.setText(str(min(255,self._to_int(self.text_node_color_g.text())))),
                                                              border_color_btn.setStyleSheet(f"background-color: rgb({self.border_node_color_g.text()}, {self.border_node_color_g.text()}, {self.border_node_color_b.text()})")} )  
        self.border_node_color_b = QtWidgets.QLineEdit(
            self, text=f'{self.node["border_color"][2]}'
        )
        self.border_node_color_b.setValidator(QtGui.QIntValidator(0, 255))
        self.border_node_color_b.textChanged.connect(lambda: {self.text_node_color_b.setText(str(min(255,self._to_int(self.text_node_color_b.text())))),
                                                              border_color_btn.setStyleSheet(f"background-color: rgb({self.border_node_color_b.text()}, {self.border_node_color_g.text()}, {self.border_node_color_b.text()})")} )  
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
    
    def createCustomNode(self, inputPorts: list, outputPorts: list, elementDict: list):
        # check if the node name is valid name for a class
        if not self.isidentifier():
            raise ValueError("Invalid node name, must be a valid python class name")
        code_str = "def __init__(self):\n\tsuper(" + self + ", self).__init__()\n"
        for inputPort in inputPorts:
            code_str = (
                f"{code_str}\tself.add_input(name='{inputPort['name']}',"
                + f"multi_input={inputPort['multi_input']},"
                + f"display_name={inputPort['display_name']},"
                + f"color={inputPort['color']}, "
                + f"locked={inputPort['locked']},"
                + f"painter_func={inputPort['painter_func']})\n"
            )

        for outputPort in outputPorts:
            code_str = (
                f"{code_str}\tself.add_output(name='{outputPort['name']}',"
                + f"multi_output={outputPort['multi_output']},"
                + f"display_name={outputPort['display_name']},"
                + f"color={outputPort['color']}, "
                + f"locked={outputPort['locked']},"
                + f"painter_func={outputPort['painter_func']})\n"
            )

        for element in elementDict:
            if element["type"] == "text_input":
                code_str = (
                    f"{code_str}\tself.add_text_input(name='{element['name']}',"
                    + f"label='{element['label']}',"
                    + f"placeholder_text='{element['placeholder_text']}',"
                    + f"tooltip='{element['tooltip']}',"
                    + f"tab='{element['tab']}')\n"
                )

            elif element["type"] == "combo_menu":
                code_str = (
                    f"{code_str}\tself.add_combo_menu(name='{element['name']}',"
                    + f"label='{element['label']}',"
                    + f"items={element['items']},"
                    + f"tooltip='{element['tooltip']}',"
                    + f"tab='{element['tab']}')\n"
                )

            elif element["type"] == "checkbox":
                code_str = (
                    f"{code_str}\tself.add_checkbox(name='{element['name']}',"
                    + f"label='{element['label']}',"
                    + f"text='{element['text']}',"
                    + f"state={element['state']},"
                    + f"tooltip='{element['tooltip']}',"
                    + f"tab='{element['tab']}')\n"
                )
        create_code = compile(
            code_str,
            "<string>",
            "exec",
        )
        func = types.FunctionType(create_code.co_consts[0], globals(), "func")

        return type(
            self,
            (BaseNode,),
            {
                "__identifier__": "nodes.custom.",
                "NODE_NAME": self,
                "__init__": func,
            },
        )

    def _updatePrpertyWidget(self):
        
        #clear the table items  
        self.property_table.clear()
        self.property_table.setRowCount(0)
        self.property_table.setHorizontalHeaderLabels(
            ["Display name", "Name", "Type", "Value", " "]
        )
        
        itemNum = len(self.properties["name"])
        self.property_table.setRowCount(itemNum)
        for i in range(itemNum):
            self.property_table.setItem(
                i, 0, QtWidgets.QTableWidgetItem(self.properties["display_name"][i])
            )
            self.property_table.setItem(
                i, 1, QtWidgets.QTableWidgetItem(self.properties["name"][i])
            )

            combo = QtWidgets.QComboBox()
            for t in self.propertyTypes:
                combo.addItem(t)
            combo.setCurrentText(self.properties["type"][i])
            self.property_table.setCellWidget(i, 2, combo)

            self.property_table.setItem(
                i, 3, QtWidgets.QTableWidgetItem(self.properties["value"][i])
            )
            # add a button to delete the current item, the clicked signal is connected to the deleteProperty method, and the index is passed as an argument
            btn = QtWidgets.QPushButton(
                "Delete", icon=QtGui.QIcon("icon/bin.png"),clicked=lambda checked, i=i: self.deleteProperty(i)
            )
            self.property_table.setCellWidget(i, 4, btn)
    @QtCore.Slot()
    def addProperties(self):
        # add items in to  self.properties, and update the properties widget
        self.properties["display_name"].append(
            f'text_{len(self.properties["display_name"])}'
        )
        self.properties["name"].append(f'property_{len(self.properties["name"])}')
        self.properties["type"].append("lineEdit")
        self.properties["value"].append("")
        self._updatePrpertyWidget()

    @QtCore.Slot()
    def addPort(self, portType: str):
        # add a port to the input or output ports
        if portType == "in":
            self.inPorts["display_name"].append(
                f'in_{len(self.inPorts["display_name"])}'
            )
            self.inPorts["name"].append(f'inport_{len(self.inPorts["name"])}')
        else:
            self.outPorts["display_name"].append(
                f'out_{len(self.outPorts["display_name"])}'
            )
            self.outPorts["name"].append(f'outport_{len(self.outPorts["name"])}')

        self._updatePortWidget(portType)

    
    def _updatePortWidget(self, portType="in"):
        if portType == "in":
            self.inPorts_table.clear()
            self.inPorts_table.setRowCount(0)
            self.inPorts_table.setHorizontalHeaderLabels(["Display name", "Name", ""])
            itemNum = len(self.inPorts["name"])
            self.inPorts_table.setRowCount(itemNum)
            for i in range(itemNum):
                self.inPorts_table.setItem(
                    i, 0, QtWidgets.QTableWidgetItem(self.inPorts["display_name"][i])
                )
                self.inPorts_table.setItem(
                    i, 1, QtWidgets.QTableWidgetItem(self.inPorts["name"][i])
                )
                btn = QtWidgets.QPushButton(
                    "Delete",icon=QtGui.QIcon("icon/bin.png"), clicked=lambda checked, i=i: self.deletePort(i, portType)
                )
                self.inPorts_table.setCellWidget(i, 2, btn)
        else:
            self.outPorts_table.clear()
            self.outPorts_table.setRowCount(0)
            self.outPorts_table.setHorizontalHeaderLabels(["Display name", "Name", ""])
            itemNum = len(self.outPorts["name"])
            self.outPorts_table.setRowCount(itemNum)
            for i in range(itemNum):
                self.outPorts_table.setItem(
                    i, 0, QtWidgets.QTableWidgetItem(self.outPorts["display_name"][i])
                )
                self.outPorts_table.setItem(
                    i, 1, QtWidgets.QTableWidgetItem(self.outPorts["name"][i])
                )
                btn = QtWidgets.QPushButton(
                    "Delete", icon=QtGui.QIcon("icon/bin.png"),clicked=lambda checked, i=i: self.deletePort(i, portType)
                )
                self.outPorts_table.setCellWidget(i, 2, btn)
    
    @QtCore.Slot()
    def updatePropertiesWidgetType(self):
        # update the properties widget based on the selected type in the dropdown menu
        pass

    @QtCore.Slot()
    def deleteProperty(self, index: int):       
        # delete the property at the index
        self.properties["display_name"].pop(index)
        self.properties["name"].pop(index)
        self.properties["type"].pop(index)
        self.properties["value"].pop(index)
        self._updatePrpertyWidget()

    @QtCore.Slot()
    def deletePort(self, index: int, portType: str):
        # delete the port at the index
        if portType == "in":
            self.inPorts["display_name"].pop(index)
            self.inPorts["name"].pop(index)
        else:
            self.outPorts["display_name"].pop(index)
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
        # save the current node to the presets
        pass
    
    @QtCore.Slot()
    def createNode(self):
        # create a new node based on the input data
        pass
        

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    dialog = CreateNodeDialog()
    dialog.show()
    sys.exit(app.exec())
