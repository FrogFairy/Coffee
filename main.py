from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTableWidgetItem, QDialog, QLabel
from PyQt5.QtGui import QPixmap
import sqlite3
import sys


con = sqlite3.connect("coffee")
cur = con.cursor()


class MainWindow(QMainWindow):
   def __init__(self):
      super(MainWindow, self).__init__()
      uic.loadUi('main_window.ui', self)
      self.display()

   def display(self):
       result = cur.execute("""SELECT coffee.id, types.title, coffee.roasting, coffee.structure, coffee.taste, 
       coffee.price, coffee.volume
       FROM coffee INNER JOIN types on coffee.type = types.id""").fetchall()
       self.tableWidget.setRowCount(len(result))
       self.tableWidget.setColumnCount(len(result[0]))
       self.tableWidget.setHorizontalHeaderLabels(
           ['ИД', 'Название сорта', 'Степень обжарки', 'Молотый/в зернах', 'Описание вкуса', 'Цена', 'Объем упаковки'])
       for i, elem in enumerate(result):
           for j, val in enumerate(elem):
               self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())