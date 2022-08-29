import mysql.connector
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def __init__(self):
        self.cnx = mysql.connector.connect(user='root', password='123@Weezer', host='127.0.0.1',
                                      database='factory_mes')
        self.cursor = self.cnx.cursor()
        self.populate_combobox()


    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1167, 883)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(0, 70, 631, 811))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.setColumnWidth(0, 530)
        self.Start_button = QtWidgets.QPushButton(Dialog)
        self.Start_button.setGeometry(QtCore.QRect(650, 70, 89, 25))
        self.Start_button.setObjectName("Start_button")
        self.test_comboBox = QtWidgets.QComboBox(Dialog)
        self.test_comboBox.setGeometry(QtCore.QRect(950, 20, 171, 31))
        self.test_comboBox.setObjectName("test_comboBox")
        self.test_comboBox.addItems(self.populate_combobox())
        self.test_comboBox.addItem("")
        self.abort_button = QtWidgets.QPushButton(Dialog)
        self.abort_button.setGeometry(QtCore.QRect(650, 120, 89, 25))
        self.abort_button.setObjectName("abort_button")
        self.title_label = QtWidgets.QLabel(Dialog)
        self.title_label.setGeometry(QtCore.QRect(140, 20, 231, 31))
        self.title_label.setObjectName("title_label")
        self.MPI_button = QtWidgets.QPushButton(Dialog)
        self.MPI_button.setGeometry(QtCore.QRect(650, 170, 89, 25))
        self.MPI_button.setObjectName("MPI_button")
        self.rout_position_label = QtWidgets.QLabel(Dialog)
        self.rout_position_label.setGeometry(QtCore.QRect(660, 280, 67, 17))
        self.rout_position_label.setObjectName("rout_position_label")
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(820, 840, 118, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.prog_bar_label = QtWidgets.QLabel(Dialog)
        self.prog_bar_label.setGeometry(QtCore.QRect(840, 810, 67, 17))
        self.prog_bar_label.setObjectName("prog_bar_label")
        self.factory_id_label = QtWidgets.QLabel(Dialog)
        self.factory_id_label.setGeometry(QtCore.QRect(660, 320, 67, 17))
        self.factory_id_label.setObjectName("factory_id_label")
        self.operator_label = QtWidgets.QLabel(Dialog)
        self.operator_label.setGeometry(QtCore.QRect(670, 540, 221, 16))
        self.operator_label.setObjectName("operator_label")
        self.rout_name_label = QtWidgets.QLabel(Dialog)
        self.rout_name_label.setGeometry(QtCore.QRect(660, 240, 81, 16))
        self.rout_name_label.setObjectName("rout_name_label")
        self.first_pass_label = QtWidgets.QLabel(Dialog)
        self.first_pass_label.setGeometry(QtCore.QRect(660, 360, 67, 17))
        self.first_pass_label.setObjectName("first_pass_label")
        self.super_user_status_label = QtWidgets.QLabel(Dialog)
        self.super_user_status_label.setGeometry(QtCore.QRect(690, 570, 111, 16))
        self.super_user_status_label.setObjectName("super_user_status_label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.load_data()

    def populate_combobox(self) -> set:
        query = ("SELECT * FROM routs")
        self.cursor.execute(query)
        ret = set()
        for i in self.cursor.fetchall():
            ret.add(i[1])
        return ret


    def retranslateUi(self, Dialog):

        _translate = QtCore.QCoreApplication.translate
        # for i , v in enumerate(self.populate_combobox()):
        #     self.test_comboBox.setItemText(i, _translate("Dialog", v[1]))
        #     self.test_comboBox.setItemText(i, _translate("Dialog", v[1]))
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "part_name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Installed"))
        self.Start_button.setText(_translate("Dialog", "Start Test"))
        # self.test_comboBox.setItemText(0, _translate("Dialog", "Car Test"))
        # self.test_comboBox.setItemText(1, _translate("Dialog", "Truck Test"))
        self.abort_button.setText(_translate("Dialog", "Abort Test"))
        self.title_label.setText(_translate("Dialog", "Test Title"))
        self.MPI_button.setText(_translate("Dialog", "MPI"))
        self.rout_position_label.setText(_translate("Dialog", "Position"))
        self.prog_bar_label.setText(_translate("Dialog", "TextLabel"))
        self.factory_id_label.setText(_translate("Dialog", "Factory ID"))
        self.operator_label.setText(_translate("Dialog", "User_Name"))
        self.rout_name_label.setText(_translate("Dialog", "Rout Name"))
        self.first_pass_label.setText(_translate("Dialog", "First Pass"))
        self.super_user_status_label.setText(_translate("Dialog", "Super User Status"))

    def load_data(self):
        #TODO add try except
        query = ("SELECT * FROM assembly_list")

        self.cursor.execute(query)

        myresult = self.cursor.fetchall()
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
        self.cursor.close()
        self.cnx.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())