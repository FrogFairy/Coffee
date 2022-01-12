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
      uic.loadUi('main.ui', self)
      self.display()
      self.add.clicked.connect(self.add_object)
      self.edit.clicked.connect(self.edit_object)

   def add_object(self):
       self.dialog = Dialog(self, 'add')
       self.dialog.show()

   def edit_object(self):
       try:
           id = self.tableWidget.item(self.tableWidget.currentRow(), 0)
           if not id:
               self.statusBar().showMessage("Не выделен элемент таблицы")
           else:
               self.statusBar().clearMessage()
               self.dialog = Dialog(self, 'edit', int(id.text()))
               self.dialog.show()
       except Exception as e:
           print(e)

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


class Dialog(QDialog):
    def __init__(self, parent, *arg):
        super().__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.types = cur.execute("""SELECT id, title FROM types""").fetchall()
        self.structures = ['молотый', 'в зернах']
        for i in self.types:
            self.comboBox.addItem(i[1])
        self.comboBox.activated.connect(self.handleActivated)
        self.comboBox_2.activated.connect(self.handleActivated)
        if arg[0] == 'add':
            self.pushButton.clicked.connect(self.add)
            self.id = cur.execute("SELECT max(id) FROM coffee").fetchone()[0] + 1
            self.comboBox.setCurrentIndex(0)
            self.type = (1, 'арабика')
        else:
            self.id = arg[1]
            type, roasting, structure, type_id, taste, price, volume = cur.execute(f"SELECT types.title, coffee.roasting, "
                                                                 f"coffee.structure, types.id, coffee.taste, "
                                                                 f"coffee.price, coffee.volume"
                                                                 f" FROM coffee INNER JOIN types on "
                                                                 f"coffee.type = types.id "
                                                                 f"WHERE coffee.id = {self.id}").fetchone()
            self.comboBox.setCurrentIndex(self.types.index((type_id, type)))
            self.type = (type_id, type)
            self.lineEdit.setText(taste)
            self.lineEdit_2.setText(roasting)
            self.lineEdit_3.setText(str(price))
            self.lineEdit_4.setText(str(volume))
            self.comboBox_2.setCurrentIndex(self.structures.index(structure))
            self.structure = structure
            self.pushButton.clicked.connect(self.edit)
        self.label_7 = QLabel(self)
        self.label_7.setGeometry(10, 260, 150, 30)
        self.label_7.setText('')

    def handleActivated(self, index):
        if self.sender() == self.comboBox:
            self.type = self.types[index]
        else:
            self.structure = self.structures[index]

    def add(self):
        if not (self.lineEdit.text() and self.lineEdit_2.text() and self.lineEdit_3.text() and self.lineEdit_4.text()):
            self.label_7.setText('Неправильный запрос')
            return
        else:
            self.label_7.setText("")
            cur.execute(f"INSERT INTO coffee (id, type, roasting, structure, taste, price, volume)"
                        f" VALUES ({self.id}, {self.type[0]}, '{self.lineEdit_2.text()}', '{self.structure}', "
                        f"'{self.lineEdit.text()}', "
                        f"'{self.lineEdit_3.text()}', '{self.lineEdit_4.text()}')")
            con.commit()
            self.parent().display()

    def edit(self):
        if not (self.lineEdit.text() and self.lineEdit_2.text() and self.lineEdit_3.text() and self.lineEdit_4.text()):
            self.label_7.setText('Неправильный запрос')
            return
        else:
            self.label_7.setText('')
            cur.execute("""UPDATE coffee SET type = ?, roasting = ?, structure = ?, taste = ?, price = ?, volume = ? 
            WHERE id = ?""",
                        (self.type[0], self.lineEdit_2.text(), self.structure, self.lineEdit.text(),
                         self.lineEdit_3.text(), self.lineEdit_4.text(), self.id))
            con.commit()
            self.parent().display()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())