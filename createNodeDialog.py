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
    """a dialog for creating a new node.
    
    """
    
    def __init__(self, parent=None):
        super(CreateNodeDialog, self).__init__()
        self.node_name = ""
        self.inPorts = []
        self.outPorts = []
        self.properties = {'name':[], 'type':[], 'value':[]}
        self.node= {}
        self.propertyTypes = ['lineEdit', 'comboBox', 'checkBox']
        self._setupUi()
    def _setupUi(self):
        self.setWindowTitle("Create Node")
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.resize(500, 400)
        self.layout = QtWidgets.QVBoxLayout(self)
        
        self.name_wgt = QtWidgets.QLineEdit(self)
        self.tab_properties = QtWidgets.QTabWidget(self)
        self.tab_node = QtWidgets.QTabWidget(self)
        self.tab_ports = QtWidgets.QTabWidget(self)
        
        name_layout = QtWidgets.QHBoxLayout()
        name_layout.addWidget(QtWidgets.QLabel('Name:'))
        name_layout.addWidget(self.name_wgt)
    
        self.layout.setSpacing(4)
        self.layout.addLayout(name_layout)
        self.layout.addWidget(self.tab_properties)
        self.layout.addWidget(self.tab_node)
        self.layout.addWidget(self.tab_ports)

        self.widget_properties = QtWidgets.QWidget(self)
        self.property_table = QtWidgets.QTableWidget(self)
        self.property_table.setColumnCount(4)
        self.property_table.setHorizontalHeaderLabels(['Name', 'Type', 'Value'])
        self.property_table.horizontalHeader().setStretchLastSection(True)
        self.property_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        
        add_btn = QtWidgets.QPushButton('Add', self, clicked=self.addProperties)
        
        # add button to widget properties
        layout = QtWidgets.QVBoxLayout(self.widget_properties)
        layout.addWidget(self.property_table)
        layout.addWidget(add_btn)
        layout.addStretch()
        self.tab_properties.addTab(self.widget_properties, 'Properties')
        

    
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

    @QtCore.Slot()
    def addProperties(self):
        # add items in to  self.properties, and update the properties widget
        
        self.properties['name'].append(f'property_{len(self.properties["name"])}')
        self.properties['type'].append('lineEdit')
        self.properties['value'].append('')
        
        itemNum = len(self.properties['name'])
        self.property_table.setRowCount(itemNum)
        for i in range(itemNum):
            self.property_table.setItem(i, 0, QtWidgets.QTableWidgetItem(self.properties['name'][i]))
            
            combo = QtWidgets.QComboBox()
            for t in self.propertyTypes:
                combo.addItem(t)
            combo.setCurrentText(self.properties['type'][i])
            self.property_table.setCellWidget(i, 1, combo)
            
            self.property_table.setItem(i, 2, QtWidgets.QTableWidgetItem(self.properties['value'][i]))
            # add a button to delete the current item
            btn = QtWidgets.QPushButton('Delete', clicked= lambda: self.deleteProperty(i))
            self.property_table.setCellWidget(i, 3, btn)
        
        
    @QtCore.Slot() 
    def updatePropertiesWidgetType(self):
        # update the properties widget based on the selected type in the dropdown menu
        pass      
    
    @QtCore.Slot()
    def deleteProperty(self, index: int):
        # delete the property at the index
        self.properties['name'].pop(index)
        self.properties['type'].pop(index)
        self.properties['value'].pop(index)
        self.property_table.removeRow(index)
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = CreateNodeDialog()
    dialog.show()
    sys.exit(app.exec_())