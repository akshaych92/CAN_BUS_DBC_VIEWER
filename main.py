from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from dbc import Ui_MainWindow as dbcui
import sys
import cantools


class UIhandler():
    def __init__(self):
        self.db = ""
        self.path = ""
        self.messages = ""
        self.namelist = []
        self.msg = QMessageBox()

    def itemselected(self, item: cantools.db.Message):
        message_name, id = str(item.text()).split(" ")
        row = 0
        messagesignals = self.db.get_message_by_name(message_name)
        dui.SignaltableWidget.setRowCount(len(messagesignals.signals))
        for i in messagesignals.signals:
            dui.SignaltableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(i.name)))
            dui.SignaltableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(i.start)))
            dui.SignaltableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(i.length)))
            dui.SignaltableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(i.offset)))
            dui.SignaltableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(i.scale)))
            dui.SignaltableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(str(i.unit)))

            row = row + 1

    def backbutton(self):
        dui.stackedWidget.setCurrentWidget(dui.welcomepage)

    def openbutton(self):
        self.path = QtWidgets.QFileDialog.getOpenFileName()
        filename, fileext = str(self.path[0]).split(".")
        if fileext != "dbc":
            self.msg.setWindowTitle("Error")
            self.msg.setText("Not a DBC file")
            self.msg.setIcon(QMessageBox.Critical)
            x = self.msg.exec_()
            return None

        # print(path[0])
        try:
            self.db = cantools.database.load_file(self.path[0])
            self.messages = self.db.messages
            dui.stackedWidget.setCurrentWidget(dui.viewerpage)
            self.namelist = []
            # print(self.messages[0].frame_id)
            for i in self.messages:
                self.namelist.append(i.name + " (" + str(hex(i.frame_id)) + ")")
            # print(self.namelist)
            dui.MessagelistWidget.clear()
            dui.MessagelistWidget.addItems(self.namelist)
            # print(self.namelist)

        except:
            self.msg.setWindowTitle("Error")
            self.msg.setText("Error in opening/parsing the DBC file")
            self.msg.setIcon(QMessageBox.Critical)
            x = self.msg.exec_()

    def newimplementation(self, text):
        self.msg.setWindowTitle(text)
        self.msg.setText("Implementation in Progress")
        self.msg.setIcon(QMessageBox.Information)
        x = self.msg.exec_()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = QtWidgets.QMainWindow()
    dui = dbcui()
    uihandler = UIhandler()

    dui.setupUi(mainwindow)
    dui.actionOpen.triggered.connect(uihandler.openbutton)
    dui.backmenubutton.clicked.connect(uihandler.backbutton)
    dui.MessagelistWidget.itemClicked.connect(uihandler.itemselected)
    dui.actionNew.triggered.connect(lambda: uihandler.newimplementation("New Dbc"))
    dui.actionSave.triggered.connect(lambda: uihandler.newimplementation("Save Dbc"))
    dui.actionCopy.triggered.connect(lambda: uihandler.newimplementation("Copy Dbc"))
    dui.actionPaste.triggered.connect(lambda: uihandler.newimplementation("Paste Dbc"))
    mainwindow.show()
    sys.exit(app.exec_())
