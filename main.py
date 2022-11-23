from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from Ui_files.dbc import Ui_MainWindow as dbcui
from PyQt5 import QtGui
import sys
import cantools


class UIhandler():
    def __init__(self):
        self.db = ""
        self.path = ""
        self.messages = ""
        self.namelist = []
        self.msg = QMessageBox()
        self.signal_selected = ""
        self.message_selected = ""
        self.message_clicked = ""

    def messageselected(self, item: cantools.db.Message):
        self.message_clicked = item
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
        self.db = ""

    def openbutton(self):
        self.path = QtWidgets.QFileDialog.getOpenFileName()
        try:
            filename, fileext = str(self.path[0]).split(".")

            if fileext != "dbc":
                self.msg.setWindowTitle("Error")
                self.msg.setText("Not a DBC file")
                self.msg.setIcon(QMessageBox.Critical)
                x = self.msg.exec_()
                return None
        except:
            return None

        try:
            self.db = cantools.db.load_file(self.path[0])
            self.messages = self.db.messages
            dui.stackedWidget.setCurrentWidget(dui.viewerpage)
            self.displaymessaages()

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

    def signalrowselected(self):
        # print("Signal Row", dui.SignaltableWidget.currentRow())
        self.signal_selected = dui.SignaltableWidget.currentRow()

    def messagerowselected(self):
        # print("Message Row", dui.MessagelistWidget.currentRow())
        self.message_selected = dui.MessagelistWidget.currentRow()

    def displaymessaages(self):
        self.namelist = []
        # print(self.messages[0].frame_id)
        for i in self.messages:
            self.namelist.append(i.name + " (" + str(hex(i.frame_id)) + ")")
        dui.MessagelistWidget.clear()
        dui.MessagelistWidget.addItems(self.namelist)

    def deletemessage(self):
        del self.messages[self.message_selected]
        self.displaymessaages()

    def deletesignal(self):
        del self.db.messages[self.message_selected].signals[self.signal_selected]
        self.messageselected(self.message_clicked)

    def savedbc(self):
        if self.db != "":
            self.path = QtWidgets.QFileDialog.getSaveFileName()
            cantools.db.dump_file(self.db, self.path[0])

        else:
            self.msg.setWindowTitle("Error")
            self.msg.setText("Nothing to save")
            self.msg.setIcon(QMessageBox.Critical)
            x = self.msg.exec_()
            return None


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = QtWidgets.QMainWindow()
    mainwindow.setWindowIcon(QtGui.QIcon("Ui_files/Ui_pics/icons8.png"))
    dui = dbcui()
    uihandler = UIhandler()

    dui.setupUi(mainwindow)
    dui.actionOpen.triggered.connect(uihandler.openbutton)
    dui.backmenubutton.clicked.connect(uihandler.backbutton)
    dui.MessagelistWidget.itemClicked.connect(uihandler.messageselected)
    dui.actionNew.triggered.connect(lambda: uihandler.newimplementation("New Dbc"))
    dui.actionSave.triggered.connect(uihandler.savedbc)
    dui.actionCopy.triggered.connect(lambda: uihandler.newimplementation("Copy Dbc"))
    dui.actionPaste.triggered.connect(lambda: uihandler.newimplementation("Paste Dbc"))
    dui.MessagelistWidget.currentRowChanged.connect(uihandler.messagerowselected)
    dui.SignaltableWidget.currentItemChanged.connect(uihandler.signalrowselected)

    dui.DelMessage.clicked.connect(uihandler.deletemessage)
    dui.DelSignal.clicked.connect(uihandler.deletesignal)

    mainwindow.show()
    sys.exit(app.exec_())
