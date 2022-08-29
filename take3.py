import datetime
import re
from dataclasses import dataclass
from datetime import time
from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector
from PyQt5.QtWidgets import QMessageBox


@dataclass
class AssemblyRegex:
    """Holds product name of DUT"""
    pn_rx: str
    sn_rx: str
    station_name: str


@dataclass
class Operator:
    """Holds product name of DUT"""
    user_name: str


@dataclass
class StationReport:
    """Holds product name of DUT"""
    station_name: str
    operator_user_name: str
    dut_part_number: str
    dut_serial_number: str
    status: str
    started_at: time
    ended_at: time


@dataclass
class AssemblyReport:
    """Holds product name of DUT"""
    station_name: str
    part_name: str
    part_number: str
    serial_number: str
    installed: bool


class Ui_Dialog(object):

    def __init__(self):
        self.permission: str = ""
        self.rout_name: str = ""
        self.first_pass: bool = True
        self.rout_done: bool = False
        self.summary_status: bool = False
        self.started_at: datetime = None
        self.ended_at: datetime = None
        self.station_name: str = ""
        self.rout_position: int = 0
        self.dut_sn = None
        self.dut_pn = None
        self.enable_assembly = False
        self.assembly_list: list = []
        self.method_list = []
        self.counter = 0
        self.product_name: str = ""
        self.row = 0
        self.assembly_count = 0
        self.method_list = [self.verify_user, self.verify_pn_sn, self.verify_assembly_part]

    def start(self):
        self.cnx = mysql.connector.connect(user='root', password='123@Weezer', host='127.0.0.1',
                                           database='factory_mes')
        self.cursor = self.cnx.cursor()

    def end(self):
        self.cursor.close()
        self.cnx.close()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1167, 883)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(0, 70, 631, 811))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnWidth(0, 530)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.Start_button = QtWidgets.QPushButton(Dialog)
        self.Start_button.setGeometry(QtCore.QRect(650, 70, 89, 25))
        self.Start_button.setObjectName("Start_button")
        self.abort_button = QtWidgets.QPushButton(Dialog)
        self.abort_button.setGeometry(QtCore.QRect(650, 120, 89, 25))
        self.abort_button.setObjectName("abort_button")
        self.abort_button.clicked.connect(self.fail_test)
        self.title_label = QtWidgets.QLabel(Dialog)
        self.title_label.setGeometry(QtCore.QRect(10, 20, 181, 31))
        self.title_label.setObjectName("title_label")
        self.MPI_button = QtWidgets.QPushButton(Dialog)
        self.MPI_button.setGeometry(QtCore.QRect(650, 170, 89, 25))
        self.MPI_button.setObjectName("MPI_button")
        self.rout_position_label = QtWidgets.QLabel(Dialog)
        self.rout_position_label.setGeometry(QtCore.QRect(660, 280, 281, 17))
        self.rout_position_label.setObjectName("rout_position_label")
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(820, 840, 118, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.prog_bar_label = QtWidgets.QLabel(Dialog)
        self.prog_bar_label.setGeometry(QtCore.QRect(840, 810, 67, 17))
        self.prog_bar_label.setObjectName("prog_bar_label")
        self.factory_id_label = QtWidgets.QLabel(Dialog)
        self.factory_id_label.setGeometry(QtCore.QRect(660, 320, 281, 17))
        self.factory_id_label.setObjectName("factory_id_label")
        self.operator_label = QtWidgets.QLabel(Dialog)
        self.operator_label.setGeometry(QtCore.QRect(670, 540, 221, 16))
        self.operator_label.setObjectName("operator_label")
        self.rout_name_label = QtWidgets.QLabel(Dialog)
        self.rout_name_label.setGeometry(QtCore.QRect(660, 240, 281, 16))
        self.rout_name_label.setObjectName("rout_name_label")
        self.first_pass_label = QtWidgets.QLabel(Dialog)
        self.first_pass_label.setGeometry(QtCore.QRect(660, 360, 281, 17))
        self.first_pass_label.setObjectName("first_pass_label")
        self.su_checkBox = QtWidgets.QCheckBox(Dialog)
        self.su_checkBox.setGeometry(QtCore.QRect(670, 570, 101, 23))
        self.su_checkBox.setObjectName("su_checkBox")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.returnPressed.connect(self.control)
        self.lineEdit.setGeometry(QtCore.QRect(200, 20, 281, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.test_comboBox = QtWidgets.QComboBox(Dialog)
        self.test_comboBox.setGeometry(QtCore.QRect(950, 20, 171, 31))
        self.test_comboBox.setObjectName("test_comboBox")
        self.test_comboBox.activated.connect(self.change_test)
        # self.test_comboBox.addItems("")
        self.test_comboBox.addItem("")
        self.test_comboBox.hide()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.display_wo()



    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "part_name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Verified"))
        self.Start_button.setText(_translate("Dialog", "Start Test"))
        self.abort_button.setText(_translate("Dialog", "Abort Test"))
        self.title_label.setText(_translate("Dialog", "Test Title"))
        self.MPI_button.setText(_translate("Dialog", "MPI"))
        self.rout_position_label.setText(_translate("Dialog", "Position"))
        self.prog_bar_label.setText(_translate("Dialog", "TextLabel"))
        self.factory_id_label.setText(_translate("Dialog", "Factory ID"))
        self.operator_label.setText(_translate("Dialog", "User_Name"))
        self.rout_name_label.setText(_translate("Dialog", "Rout Name"))
        self.first_pass_label.setText(_translate("Dialog", "First Pass"))
        self.su_checkBox.setText(_translate("Dialog", "Super User"))

    def populate_combobox(self):
        self.start()
        query = (f"SELECT station_name FROM assembly_list WHERE product = '{self.product_name}';")
        self.cursor.execute(query)
        ret = set()
        for i in self.cursor.fetchall():
            ret.add(i[0])
        self.end()
        self.test_comboBox.addItems(ret)

    def change_test(self):
        self.station_name = self.test_comboBox.currentText()
        self.start()
        query = (f"SELECT rout_position FROM assembly_list WHERE station_name = '{self.station_name}';")
        self.cursor.execute(query)
        rout_position = self.cursor.fetchall()
        self.rout_position = rout_position[0][0]
        self.end()
        self.load_assembly()

    def display_wo(self):
        self.tableWidget.setRowCount(2)
        self.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem("Verify User Name"))
        self.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem("No"))
        self.tableWidget.setItem(1, 0, QtWidgets.QTableWidgetItem(
            "Work order part number and serial number ex 123123123123,45-00121212-12-12"))
        self.tableWidget.setItem(1, 1, QtWidgets.QTableWidgetItem("No"))

    def control(self):
        if self.method_list[self.counter] == self.verify_assembly_part and not self.enable_assembly:
            self.assembly()

        self.method_list[self.counter]()
        self.counter += 1
        if self.counter == len(self.method_list):
            self.complete_test_msg_box()
            self.assembly_count = 0
            self.counter = 0
            self.enable_assembly = False

    def assembly(self):
        count = 0
        while count < (self.row - 1):
            self.method_list.append(self.verify_assembly_part)
            count += 1
        self.enable_assembly = True

    def complete_test_msg_box(self):
        self.ended_at = datetime.datetime.now()
        self.summary_status = True
        self.upload_report()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Assembly Completed")
        msg.setWindowTitle("Information MessageBox")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()
        self.counter = 0
        self.method_list = [self.verify_user, self.verify_pn_sn, self.verify_assembly_part]
        self.display_wo()

    def fail_test(self):
        self.ended_at = datetime.datetime.now()
        self.summary_status = False
        self.upload_report()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Assembly Failed")
        msg.setWindowTitle("Information MessageBox")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()
        self.counter = 0
        self.method_list = [self.verify_user, self.verify_pn_sn, self.verify_assembly_part]
        self.display_wo()

    def verify_user(self):
        Operator.user_name = self.lineEdit.text()
        self.start()
        query = f"SELECT EXISTS(SELECT * from operator WHERE user_name='{Operator.user_name}');"
        self.cursor.execute(query)
        ret = self.cursor.fetchall()[0][0]
        self.end()
        if ret:
            self.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem("Yes"))
            self.tableWidget.item(0, 1).setBackground(QtGui.QColor(0, 255, 0))
            self.lineEdit.clear()
            self.operator_label.setText(f"User Name: {Operator.user_name}")
            # self.factory_id_label.setText(f"Factory ID: {}")
            self.get_user_info()

    def get_user_info(self):
        self.start()
        query = f"SELECT position from operator WHERE user_name='{Operator.user_name}';"
        self.cursor.execute(query)
        self.permission = self.cursor.fetchall()[0][0]
        self.end()

    def get_rout_info(self):
        self.start()
        query = f"SELECT rout_name, factory_id from routs WHERE station_name = '{self.station_name}';"
        self.cursor.execute(query)
        ret = self.cursor.fetchall()
        self.end()
        self.rout_name = ret[0][0]
        self.factory_id_label.setText(f"Factory ID: {ret[0][1]}")
        self.rout_name_label.setText(f"Rout Name: {self.rout_name}")

    def verify_pn_sn(self):
        self.start()
        self.dut_pn, self.dut_sn = self.lineEdit.text().split(",")
        query = f"SELECT EXISTS(SELECT * from WorkOrder WHERE part_number='{self.dut_pn}' and serial_number='{self.dut_sn}');"
        self.cursor.execute(query)
        ret = self.cursor.fetchall()[0][0]
        self.end()
        if ret:
            self.tableWidget.setItem(1, 1, QtWidgets.QTableWidgetItem("Yes"))
            self.tableWidget.item(1, 1).setBackground(QtGui.QColor(0, 255, 0))
            self.lineEdit.clear()
            self.start()
            query = f"SELECT product_name from WorkOrder WHERE part_number='{self.dut_pn}' and serial_number='{self.dut_sn}';"
            self.cursor.execute(query)
            self.product_name = self.cursor.fetchall()[0][0]
            self.end()
        if self.permission == "admin":
            self.su_checkBox.setChecked(True)
            self.test_comboBox.show()
            self.test_comboBox.setCurrentText("")

        self.check_rout()
        self.rout_position_label.setText(f"Rout Position: {self.rout_position}")
        self.get_rout_size()
        self.populate_combobox()
        if not self.rout_done:
            self.load_assembly()

    def get_rout_size(self):
        self.start()
        query = (f"SELECT complete_rout_size FROM assembly_list WHERE product = '{self.product_name}';")
        self.cursor.execute(query)
        rout_size = self.cursor.fetchall()
        self.rout_size = rout_size
        self.end()
        if self.rout_position > self.rout_size[0][0]:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("This Product has completed the rout")
            msg.setWindowTitle("Information MessageBox")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()
            self.assembly_count = 0
            self.counter = -1
            self.display_wo()
            self.rout_done = True
        else:
            self.rout_done = False

    def verify_assembly_part(self):
        self.started_at = datetime.datetime.now()
        pn, sn = self.lineEdit.text().split(",")
        if bool(re.fullmatch(self.assembly_list[self.assembly_count].pn_rx, pn)) and \
                bool(re.fullmatch(self.assembly_list[self.assembly_count].sn_rx, sn)):
            self.tableWidget.setItem(self.assembly_count, 1, QtWidgets.QTableWidgetItem("Yes"))
            self.tableWidget.item(self.assembly_count, 1).setBackground(QtGui.QColor(0, 255, 0))
            self.lineEdit.clear()
            self.assembly_count += 1
            if self.assembly_count == len(self.assembly_list):
                self.assembly_list = []
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Assembly Failed")
            msg.setWindowTitle("Failed at verify_assembly_part")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

    def check_rout(self):
        self.start()
        query = (f"SELECT max(rout_position), status FROM StationReport WHERE dut_serial_number = '{self.dut_sn}' group by status;")
        self.cursor.execute(query)
        position = self.cursor.fetchall()
        print(position)
        self.end()
        if not position:
            self.rout_position = 1
        else:
            if position[0][1]:
                self.rout_position = int(position[0][0]) + 1
            else:
                self.rout_position = int(position[0][0])

    def load_assembly(self):
        # TODO add try except
        self.start()
        query = (
            f"SELECT * FROM assembly_list WHERE product = '{self.product_name}' and rout_position = '{self.rout_position}';")
        self.cursor.execute(query)
        myresult = self.cursor.fetchall()
        self.row = 0
        self.tableWidget.setRowCount(len(myresult))
        self.station_name = myresult[0][5]
        for test in myresult:
            self.assembly_list.append(AssemblyRegex(test[2], test[3], test[5]))
            self.tableWidget.setItem(self.row, 0, QtWidgets.QTableWidgetItem(test[0]))
            self.tableWidget.setItem(self.row, 1, QtWidgets.QTableWidgetItem("No"))
            self.row += 1
        self.end()
        self.get_first_pass()
        self.get_rout_info()

    def get_first_pass(self):
        self.start()
        first_pass = f"select exists(select first_pass from StationReport where station_name = '{self.station_name}');"
        self.cursor.execute(first_pass)
        fp_res = self.cursor.fetchall()
        if not fp_res[0][0]:
            self.first_pass_label.setText("First Pass: True")
        else:
            self.first_pass_label.setText("First Pass: False")
            self.first_pass = False
        self.end()

    def upload_report(self):
        self.start()
        query = f"INSERT INTO StationReport (station_name, operator_user_name, dut_part_number, dut_serial_number, status, started_at, ended_at, rout_position, complete_rout_size, rout_name, first_pass) VALUES" \
                f" ('{self.station_name}', '{Operator.user_name}','{self.dut_pn}', '{self.dut_sn}', {self.summary_status}, '{self.started_at}', '{self.ended_at}', '{self.rout_position}' ,'{self.rout_position}', '{self.rout_name}', {self.first_pass});"
        self.cursor.execute(query)
        self.cnx.commit()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
