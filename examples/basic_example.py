#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import signal
import types
from PySide6 import QtCore, QtWidgets, QtGui

from NodeGraphQt import (
    BaseNode,
    NodeGraph,
    PropertiesBinWidget,
    NodesTreeWidget,
    NodesPaletteWidget,
)

# import example nodes from the "example_nodes" package
import PresetNotes
from createNodeDialog import CreateNodeDialog
import inspect


class FlowNodeGraph(QtWidgets.QMainWindow):
    graph = None
    nodesTree = None

    def __init__(self):
        super(FlowNodeGraph, self).__init__()
        self.setAcceptDrops(True)
        self.initUI()
        self.properties_bin = PropertiesBinWidget(node_graph=self.graph, mode="dock")
        self.properties_bin.setWindowFlags(QtCore.Qt.WindowType.Tool)
        self.dockWidgetProperties.setWidget(self.properties_bin)
        self.setupInitalGraphy()
        self.updateNodeExplorer()
        # self.graph.node_double_clicked.connect(self.display_properties_bin)
        # self.graph.node_selected.connect(self.display_properties_bin)

    def dragEnterEvent(self, e):
        # if the item being dragged is a node from the node explorer, and the item is top level, refuse the event.
        if (
            e.source() == self.nodesTree
            and e.source().selectedIndexes()[0].parent().data() is None
        ):
            e.ignore()
        else:
            e.accept()

    def dropEvent(self, e):
        super().dropEvent(e)
        position = e.position().toPoint()
        position = self.centralWidget().mapFromParent(position)
        position = self.graph._viewer.mapToScene(position)
        sender = e.source()
        nodeId = sender.selectedIndexes()[0].data()
        gp = sender.selectedIndexes()[0].parent().data()
        p = position.x() - 20, position.y() - 20
        self.graph.create_node(node_type=f"{gp}.{nodeId}", pos=p)
        e.accept()

    def initUI(self):
        # add status bar
        self.statusBar().showMessage("Ready")

        # create node graph.
        self.graph = NodeGraph()
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, False)
        self.graph._viewer.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, False
        )
        # set the context menu from a json file.
        self.graph.set_context_menu_from_file("hotkeys.json")
        self.setCentralWidget(self.graph.widget)

        # create dock widgets Nodes Explorer.
        self.dockWidgetNoteExplorer = QtWidgets.QDockWidget("Nodes Explorer")
        nodeWidget = QtWidgets.QWidget()
        nodeWidgetLayout = QtWidgets.QVBoxLayout(
            nodeWidget, spacing=0, contentsMargins=QtCore.QMargins(0, 0, 0, 0)
        )
        self.nodefilter = QtWidgets.QLineEdit(textChanged=self.onFilterChanged)
        self.nodefilter.setPlaceholderText("Filter nodes...")
        refreshButton = QtWidgets.QPushButton(
            text="", icon=QtGui.QIcon("icon/refresh.png")
        )

        refreshButton.clicked.connect(self.updateNodeExplorer)
        filterAndRefreshWidget = QtWidgets.QWidget()
        filterAndRefreshLayout = QtWidgets.QHBoxLayout(
            filterAndRefreshWidget,
            spacing=0,
            contentsMargins=QtCore.QMargins(0, 0, 0, 0),
        )
        filterAndRefreshLayout.addWidget(self.nodefilter)
        filterAndRefreshLayout.addWidget(refreshButton)
        nodeWidgetLayout.addWidget(filterAndRefreshWidget)
        createNewNodeButton = QtWidgets.QPushButton("Create New Node")

        createNewNodeButton.clicked.connect(self.onCreateNode)
        nodeWidgetLayout.addWidget(createNewNodeButton)
        self.dockWidgetNoteExplorer.setWidget(nodeWidget)
        self.nodesTree = QtWidgets.QTreeWidget()
        self.nodesTree.setDragEnabled(True)
        self.nodesTree.setHeaderHidden(True)
        nodeWidgetLayout.addWidget(self.nodesTree)
        self.addDockWidget(
            QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, self.dockWidgetNoteExplorer
        )

        # create dock widgets Properties. TODO: Add the properties widget.
        self.dockWidgetProperties = QtWidgets.QDockWidget("Properties")
        self.addDockWidget(
            QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.dockWidgetProperties
        )

    def updateNodeExplorer(self):
        self.nodesTree.clear()
        self.nodefilter.clear()
        nodeClasses = inspect.getmembers(PresetNotes, inspect.isclass)
        identifiers = [nodeClass[1].__identifier__ for nodeClass in nodeClasses]
        identifiers = list(set(identifiers))

        # add thoses identifiers to the tree as top level items, and add the classes name as children
        for identifier in identifiers:
            item = QtWidgets.QTreeWidgetItem()
            item.setBackground(0, QtGui.QColor(55, 55, 55, 80))
            item.setText(0, identifier)
            self.nodesTree.addTopLevelItem(item)
            for nodeClass in nodeClasses:
                if nodeClass[1].__identifier__ == identifier:
                    child = QtWidgets.QTreeWidgetItem()
                    child.setText(0, nodeClass[0])
                    item.addChild(child)
        self.nodesTree.expandAll()

    def setupInitalGraphy(self):

        nodeClasses = inspect.getmembers(PresetNotes, inspect.isclass)
        self.graph.register_nodes([nodeClass[1] for nodeClass in nodeClasses])

        # create node with custom text color and disable it.
        n_basic_a = self.graph.create_node(
            "nodes.basic.BasicNodeA", text_color="#feab20"
        )
        n_basic_a.set_disabled(True)

        # create node and set a custom icon.
        n_basic_b = self.graph.create_node("nodes.basic.BasicNodeB", name="custom icon")
        n_basic_b.set_icon(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "star.png")
        )

        # create node with the custom port shapes.
        n_custom_ports = self.graph.create_node(
            "nodes.custom.ports.CustomPortsNode", name="custom ports"
        )

        # create node with the embedded QLineEdit widget.
        n_text_input = self.graph.create_node(
            "nodes.widget.TextInputNode", name="text node", color="#0a1e20"
        )

        # create node with the embedded QCheckBox widgets.
        n_checkbox = self.graph.create_node(
            "nodes.widget.CheckboxNode", name="checkbox node"
        )

        # create node with the QComboBox widget.
        n_combo_menu = self.graph.create_node(
            "nodes.widget.DropdownMenuNode", name="combobox node"
        )

        # crete node with the circular design.
        n_circle = self.graph.create_node("nodes.basic.CircleNode", name="circle node")

        # create group node.
        n_group = self.graph.create_node("nodes.group.MyGroupNode")

        # make node connections.

        # (connect nodes using the .set_output method)
        n_text_input.set_output(0, n_custom_ports.input(0))
        n_text_input.set_output(0, n_checkbox.input(0))
        n_text_input.set_output(0, n_combo_menu.input(0))

        # (connect nodes using the .set_input method)
        n_group.set_input(0, n_custom_ports.output(1))
        n_basic_b.set_input(2, n_checkbox.output(0))
        n_basic_b.set_input(2, n_combo_menu.output(1))

        # (connect nodes using the .connect_to method from the port object)
        # n_basic_a.input(0).connect_to(n_basic_b.output(0))
        n_basic_b.output(0).connect_to(n_basic_a.input(0))

        # auto layout nodes.
        self.graph.auto_layout_nodes()

        # crate a backdrop node and wrap it around
        # "custom port node" and "group node".
        n_backdrop = self.graph.create_node("Backdrop")
        n_backdrop.wrap_nodes([n_custom_ports, n_combo_menu])

        # fit nodes to the viewer.
        self.graph.clear_selection()
        self.graph.fit_to_selection()

        # Custom builtin widgets from NodeGraphQt
        # ---------------------------------------

    # example show the node properties bin widget when a node is double-clicked.
    def display_properties_bin(self):
        if not self.properties_bin.isVisible():
            self.properties_bin.show()

    @QtCore.Slot()
    def onCreateNode(self):
        createNode = CreateNodeDialog(self)
        createNode.show()

    @QtCore.Slot(str)
    def onFilterChanged(self, text: str):
        # filter the node explorer tree items based on the text.
        # for i in range(self.nodesTree.topLevelItemCount()):
        #     item = self.nodesTree.topLevelItem(i)
        #     item.setHidden(text.lower() not in item.text(0).lower())

        # filter the node explorer tree items based on the text,hide the parent if no child is visible
        for i in range(self.nodesTree.topLevelItemCount()):
            item = self.nodesTree.topLevelItem(i)
            parentHidden = True
            for j in range(item.childCount()):
                child = item.child(j)
                child.setHidden(text.lower() not in child.text(0).lower())
                if not child.isHidden():
                    parentHidden = False
            item.setHidden(parentHidden)


if __name__ == "__main__":

    # handle SIGINT to make the app terminate on CTRL+C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QtWidgets.QApplication([])

    mainWin = FlowNodeGraph()
    mainWin.show()
    app.exec()
