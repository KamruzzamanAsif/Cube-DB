from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
import ui_window
from Backend import apriori
import sys


class Home(QMainWindow):  # Home extends QMainWindow

    def __init__(self):
        super(QMainWindow, self).__init__()
        
        # store values in dictionary [BACKEND]
        self.inventory_items = []               # this will update when user add item into inventory from STOCK Tab
        self.transaction_list = []
        self.table_data = apriori.updated_stock_data()
        
        # initialization
        self.home = ui_window.Ui_MainWindow()
        self.home.setupUi(self) 
        self.stock_page()
        self.home.add_transaction_btn.clicked.connect(self.transaction_page)
        
    def stock_page(self):
        
        # set the current tab
        self.home.tabWidget.setCurrentIndex(0)
        
        # load the table with data
        self.loadStockTable()
        
        # navigate the update inventory button click
        self.home.update_inventory_btn.clicked.connect(self.update_inventory)
        
    def best_product_page(self):
        
        self.home.tabWidget.setCurrentIndex(1)
        
    def transaction_page(self):
        
        # set the current Tab
        self.home.tabWidget.setCurrentIndex(2)
        
        # get the text from the textboxes
        self.product_names = self.home.product_names_edit.text().split(', ')
        self.product_quantites = self.home.product_quant_edit.text().split(', ')
        print(self.product_names)
        print(self.product_quantites)
        
        # set the text into appriori algorithm
        self.tempdict = {}
        for name, quantity in zip(self.product_names, self.product_quantites):
            self.tempdict[name] = int(quantity)
            
        self.transaction_list.append(self.tempdict)
        
        # sending data to [BACKEND]
        apriori.addData(self.transaction_list)
        self.loadStockTable()
        
        
                
    def update_inventory(self):
        
        # first extract the selected row Id and then update the value
        currentrow = self.home.stockTable.currentRow()
        currentRowValue = self.table_data[currentrow]       # ('Apple', 5, '50%')
        self.inventory_items.append(currentRowValue)
        
        # now update the value of the selected row in table_data
        self.table_data[currentrow] = (currentRowValue[0], currentRowValue[1] + 1, currentRowValue[2])
        print(self.table_data,'\n')
        
        self.home.reload_btn.clicked.connect(self.loadStockTable)
        
    def loadStockTable(self):
        
        self.table_data = apriori.updated_stock_data()
        print(self.table_data)
        
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