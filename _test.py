from PySide6 import QtWidgets, QtCore, QtGui
    
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self,parent)
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(3)
        self.setCentralWidget(self.table)
        data1 = ['row1','row2','row3','row4']
        data2 = ['1','2.0','3.00000001','3.9999999']
        combo_box_options = ["Option 1","Option 2","Option 3"]

        self.table.setRowCount(4)

        for index in range(4):
            item1 = QtWidgets.QTableWidgetItem(data1[index])
            self.table.setItem(index,0,item1)
            item2 = QtWidgets.QTableWidgetItem(data2[index])
            self.table.setItem(index,1,item2)
            combo = QtWidgets.QComboBox()
            for t in combo_box_options:
                combo.addItem(t)
            self.table.setCellWidget(index,2,combo)
            
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec()