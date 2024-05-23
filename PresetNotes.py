import NodeGraphQt
from PySide6 import QtCore, QtGui


class BasicImageNode(NodeGraphQt.BaseNode):
    __identifier__ = "nodes.image"
    NODE_NAME = "image node"

    def __init__(self):
        super(BasicImageNode, self).__init__()
        self.add_image_show("image", "", QtGui.QPixmap("star.png"))


class BasicNodeA(NodeGraphQt.BaseNode):
    """
    A node class with 2 inputs and 2 outputs.
    """

    # unique node identifier.
    __identifier__ = "nodes.basic"

    # initial default node name.
    NODE_NAME = "node A"

    def __init__(self):
        super(BasicNodeA, self).__init__()

        # create node inputs.
        self.add_input("in A")
        self.add_input("in B")

        # create node outputs.
        self.add_output("out A")
        self.add_output("out B")


class BasicNodeB(NodeGraphQt.BaseNode):
    """
    A node class with 3 inputs and 3 outputs.
    The last input and last output can take in multiple pipes.
    """

    # unique node identifier.
    __identifier__ = "nodes.basic"

    # initial default node name.
    NODE_NAME = "node B"

    def __init__(self):
        super(BasicNodeB, self).__init__()

        # create node inputs
        self.add_input("single 1")
        self.add_input("single 2")
        self.add_input("multi in", multi_input=True)

        # create node outputs
        self.add_output("single 1", multi_output=False)
        self.add_output("single 2", multi_output=False)
        self.add_output("multi out")


class CircleNode(NodeGraphQt.BaseNodeCircle):
    """
    A node class with 3 inputs and 3 outputs.
    This node is a circular design.
    """

    # unique node identifier.
    __identifier__ = "nodes.basic"

    # initial default node name.
    NODE_NAME = "Circle Node"

    def __init__(self):
        super(CircleNode, self).__init__()
        self.set_color(10, 24, 38)

        # create node inputs
        p = self.add_input("in 1")
        p.add_accept_port_type(
            port_name="single 1", port_type="out", node_type="nodes.basic.BasicNodeB"
        )

        self.add_input("in 2")
        self.add_input("in 3", multi_input=True)
        self.add_input("in 4", display_name=False)
        self.add_input("in 5", display_name=False)

        # create node outputs
        self.add_output("out 1")
        self.add_output("out 2", multi_output=False)
        self.add_output("out 3", multi_output=True, display_name=False)
        self.add_output("out 4", multi_output=True, display_name=False)


def draw_triangle_port(painter, rect, info):
    """
    Custom paint function for drawing a Triangle shaped port.

    Args:
        painter (QtGui.QPainter): painter object.
        rect (QtCore.QRectF): port rect used to describe parameters
                              needed to draw.
        info (dict): information describing the ports current state.
            {
                'port_type': 'in',
                'color': (0, 0, 0),
                'border_color': (255, 255, 255),
                'multi_connection': False,
                'connected': False,
                'hovered': False,
            }
    """
    painter.save()

    size = int(rect.height() / 2)
    triangle = QtGui.QPolygonF()
    triangle.append(QtCore.QPointF(-size, size))
    triangle.append(QtCore.QPointF(0.0, -size))
    triangle.append(QtCore.QPointF(size, size))

    transform = QtGui.QTransform()
    transform.translate(rect.center().x(), rect.center().y())
    port_poly = transform.map(triangle)

    # mouse over port color.
    if info["hovered"]:
        color = QtGui.QColor(14, 45, 59)
        border_color = QtGui.QColor(136, 255, 35)
    # port connected color.
    elif info["connected"]:
        color = QtGui.QColor(195, 60, 60)
        border_color = QtGui.QColor(200, 130, 70)
    # default port color
    else:
        color = QtGui.QColor(*info["color"])
        border_color = QtGui.QColor(*info["border_color"])

    pen = QtGui.QPen(border_color, 1.8)
    pen.setJoinStyle(QtCore.Qt.MiterJoin)

    painter.setPen(pen)
    painter.setBrush(color)
    painter.drawPolygon(port_poly)

    painter.restore()


def draw_square_port(painter, rect, info):
    """
    Custom paint function for drawing a Square shaped port.

    Args:
        painter (QtGui.QPainter): painter object.
        rect (QtCore.QRectF): port rect used to describe parameters
                              needed to draw.
        info (dict): information describing the ports current state.
            {
                'port_type': 'in',
                'color': (0, 0, 0),
                'border_color': (255, 255, 255),
                'multi_connection': False,
                'connected': False,
                'hovered': False,
            }
    """
    painter.save()

    # mouse over port color.
    if info["hovered"]:
        color = QtGui.QColor(14, 45, 59)
        border_color = QtGui.QColor(136, 255, 35, 255)
    # port connected color.
    elif info["connected"]:
        color = QtGui.QColor(195, 60, 60)
        border_color = QtGui.QColor(200, 130, 70)
    # default port color
    else:
        color = QtGui.QColor(*info["color"])
        border_color = QtGui.QColor(*info["border_color"])

    pen = QtGui.QPen(border_color, 1.8)
    pen.setJoinStyle(QtCore.Qt.MiterJoin)

    painter.setPen(pen)
    painter.setBrush(color)
    painter.drawRect(rect)

    painter.restore()


class CustomPortsNode(NodeGraphQt.BaseNode):
    """
    example test node with custom shaped ports.
    """

    # set a unique node identifier.
    __identifier__ = "nodes.custom.ports"

    # set the initial default node name.
    NODE_NAME = "node"

    def __init__(self):
        super(CustomPortsNode, self).__init__()

        # create input and output port.
        self.add_input("in", color=(200, 10, 0))
        self.add_output("default")
        self.add_output("square", painter_func=draw_square_port)
        self.add_output("triangle", painter_func=draw_triangle_port)


class MyGroupNode(NodeGraphQt.GroupNode):
    """
    example test group node with a in port and out port.
    """

    # set a unique node identifier.
    __identifier__ = "nodes.group"

    # set the initial default node name.
    NODE_NAME = "group node"

    def __init__(self):
        super(MyGroupNode, self).__init__()
        self.set_color(50, 8, 25)

        # create input and output port.
        self.add_input("in")
        self.add_output("out")
        self.add_output("out1")


class DropdownMenuNode(NodeGraphQt.BaseNode):
    """
    An example node with a embedded added QCombobox menu.
    """

    # unique node identifier.
    __identifier__ = "nodes.widget"

    # initial default node name.
    NODE_NAME = "menu"

    def __init__(self):
        super(DropdownMenuNode, self).__init__()

        # create input & output ports
        self.add_input("in 1")
        self.add_output("out 1")
        self.add_output("out 2")

        # create the QComboBox menu.
        items = ["item 1", "item 2", "item 3"]
        self.add_combo_menu(
            "my_menu", "Menu Test", items=items, tooltip="example custom tooltip"
        )


class TextInputNode(NodeGraphQt.BaseNode):
    """
    An example of a node with a embedded QLineEdit.
    """

    # unique node identifier.
    __identifier__ = "nodes.widget"

    # initial default node name.
    NODE_NAME = "text"

    def __init__(self):
        super(TextInputNode, self).__init__()

        # create input & output ports
        self.add_input("in")
        self.add_output("out")

        # create QLineEdit text input widget.
        self.add_text_input("my_input", "Text Input", tab="widgets")


class CheckboxNode(NodeGraphQt.BaseNode):
    """
    An example of a node with 2 embedded QCheckBox widgets.
    """

    # set a unique node identifier.
    __identifier__ = "nodes.widget"

    # set the initial default node name.
    NODE_NAME = "checkbox"

    def __init__(self):
        super(CheckboxNode, self).__init__()

        # create the checkboxes.
        self.add_checkbox("cb_1", "", "Checkbox 1", True)
        self.add_checkbox("cb_2", "", "Checkbox 2", False)

        # create input and output port.
        self.add_input("in", color=(200, 100, 0))
        self.add_output("out", color=(0, 100, 200))