# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_connect.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import cx_Oracle
class Ui_qt_connect(object):
    def setupUi(self, qt_connect):
        self.qt_connect=qt_connect
        qt_connect.setObjectName("qt_connect")
        qt_connect.resize(400, 300)
        self.Connect = QtWidgets.QDialogButtonBox(qt_connect)
        self.Connect.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.Connect.setOrientation(QtCore.Qt.Horizontal)
        self.Connect.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.Connect.setObjectName("Connect")
        self.uname = QtWidgets.QLineEdit(qt_connect)
        self.uname.setGeometry(QtCore.QRect(210, 20, 113, 21))
        self.uname.setObjectName("uname")
        self.uname.setText("system")
        self.password = QtWidgets.QLineEdit(qt_connect)
        self.password.setGeometry(QtCore.QRect(210, 70, 113, 21))
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.password.setText("welcome1")
        self.connect_str = QtWidgets.QLineEdit(qt_connect)
        self.connect_str.setGeometry(QtCore.QRect(210, 120, 113, 21))
        self.connect_str.setObjectName("connect_str")
        self.connect_str.setText("//192.168.56.101/imc_cdbc")
        self.uname_l = QtWidgets.QLabel(qt_connect)
        self.uname_l.setGeometry(QtCore.QRect(50, 20, 59, 16))
        self.uname_l.setObjectName("uname_l")
        self.label_2 = QtWidgets.QLabel(qt_connect)
        self.label_2.setGeometry(QtCore.QRect(50, 70, 59, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(qt_connect)
        self.label_3.setGeometry(QtCore.QRect(50, 120, 101, 16))
        self.label_3.setObjectName("label_3")
        self.db=None
        self.retranslateUi(qt_connect)
        self.Connect.accepted.connect(self.accept)#qt_connect.accept)
        self.Connect.rejected.connect(self.reject)#qt_connect.reject)
        QtCore.QMetaObject.connectSlotsByName(qt_connect)
    def accept(self):
        self.is_accepted=True
        try:
            self.full_cstr=self.uname.text()+"/"+self.password.text()+"@"+self.connect_str.text()
            self.db=cx_Oracle.connect(self.full_cstr)
            cursor=self.db.cursor();
            cursor.execute("select sys_context('userenv','con_id'), dbid from v$database")
            for row in cursor:
                self.con_id=int(row[0])
                self.con_dbid=int(row[1])
            self.qt_connect.close()
        except cx_Oracle.DatabaseError as exc:
                error, = exc.args
                choice = QMessageBox.question(self.qt_connect, 'Error',
                                                            "Cannot connect to the db, please verify",
                                                            QMessageBox.Yes)


    def reject(self):
        self.is_accepted=False
        self.qt_connect.close()

    def retranslateUi(self, qt_connect):
        _translate = QtCore.QCoreApplication.translate
        qt_connect.setWindowTitle(_translate("qt_connect", "Connect to Database"))
        self.uname_l.setText(_translate("qt_connect", "User Name"))
        self.label_2.setText(_translate("qt_connect", "Password"))
        self.label_3.setText(_translate("qt_connect", "Connect String"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    qt_connect = QtWidgets.QDialog()
    ui = Ui_qt_connect()
    ui.setupUi(qt_connect)
    qt_connect.show()
    sys.exit(app.exec_())
