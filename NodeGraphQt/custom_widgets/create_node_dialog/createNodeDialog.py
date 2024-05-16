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

    def setupUi(self):
        self.setWindowTitle("Create Node")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.resize(500, 400)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.tab_widget = QtWidgets.QTabWidget()
        self.layout.addWidget(self.tab_widget)
        self.properties_bin = PropertiesBinWidget()
        self.nodes_tree = NodesTreeWidget()
        self.nodes_palette = NodesPaletteWidget()
        self.tab_widget.addTab(self.properties_bin, "Properties")
        self.tab_widget.addTab(self.nodes_tree, "Nodes")
        self.tab_widget.addTab(self.nodes_palette, "Palette")
        self.nodes_tree.node_double_clicked.connect(self.create_node)
        self.nodes_palette.node_double_clicked.connect(self.create_node)
    
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

