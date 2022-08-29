from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector
from mysql.connector import errorcode


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1065, 540)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(20, 40, 581, 291))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)
        # self.tableWidget.setColumnWidth(0, 477)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.load_data()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "part_name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "part_number"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "serial_number"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "product"))

    def load_data(self):
        #TODO add try except
        cnx = mysql.connector.connect(user='root', password='123@Weezer', host='127.0.0.1',
                                      database='factory_mes')
        cursor = cnx.cursor()
        query = ("SELECT * FROM assembly_list")

        cursor.execute(query)

        myresult = cursor.fetchall()
        print(myresult)

        # for x in myresult:
        #     print(x[0])

        # tests = [{"part": "wheel", "installed": "yes"}, {"part": "windows", "installed": "no"}]
        row = 0
        self.tableWidget.setRowCount(len(myresult))
        for test in myresult:
            print("hi",test[0])
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(test[0]))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(test[1]))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(test[2]))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(test[3]))
            row += 1
        cursor.close()
        cnx.close()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
