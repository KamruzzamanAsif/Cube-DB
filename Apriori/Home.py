from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
import ui_window
import sys


class Home(QMainWindow):  # Home extends QMainWindow

    def __init__(self):
        super(QMainWindow, self).__init__()
        
        # store values in dictionary [BACKEND]
        self.inventory_items = []               # this will update when user add item into inventory from STOCK Tab
        self.table_data = [
            ('Apple', 5, '50%'), 
            ('Banana', 10, '20%'),
            ('Orange', 15, '10%'),
            ('Grapes', 20, '5%'),
            ('Mango', 25, '0%')
        ]
        

        self.home = ui_window.Ui_MainWindow()
        self.home.setupUi(self) 
                
        self.stock_page()
        
    def stock_page(self):
        
        # set the current tab
        self.home.tabWidget.setCurrentIndex(0)
        
        # load the table with data
        self.loadTable()
        
        # navigate the update inventory button click
        self.home.update_inventory_btn.clicked.connect(self.update_inventory)
        
    def best_product_page(self):
        
        self.home.tabWidget.setCurrentIndex(1)
        
    def transaction_page(self):
        
        self.home.tabWidget.setCurrentIndex(2)
                
    def update_inventory(self):
        
        # first extract the selected row Id and then update the value
        currentrow = self.home.stockTable.currentRow()
        currentRowValue = self.table_data[currentrow]       # ('Apple', 5, '50%')
        self.inventory_items.append(currentRowValue)
        
        # now update the value of the selected row in table_data
        self.table_data[currentrow] = (currentRowValue[0], currentRowValue[1] + 1, currentRowValue[2])
        print(self.table_data,'\n')
        
        self.home.reload_btn.clicked.connect(self.loadTable)
        
    def loadTable(self):
        
        # set value to the table
        columns = self.home.stockTable.columnCount()
        rows = len(self.table_data)
        self.home.stockTable.setRowCount(rows)
        
        # store the reloaded value into the PyQt_UI
        for row in range(rows):
            for col in range(columns):
                self.home.stockTable.setItem(
                    row, col, QTableWidgetItem(str(self.table_data[row][col])))
        
        
        
                
if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    window = Home()
    window.show()
    sys.exit(app.exec_())