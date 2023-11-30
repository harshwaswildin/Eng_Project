import sys
import os
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import pyqtSlot, QTimer, QDate, Qt
import resource
import datetime
import csv
import time 
import threading

# from model import Model
from out_window2 import Ui_OutputDialog

def execute_script(name):
    os.system('python ' + name) 

class Ui_Dialog1(QDialog):
    
    def __init__(self):
        super(Ui_Dialog1, self).__init__()
        loadUi("onWindow.ui", self)
        self.runButton.clicked.connect(self.runSlot)

        
        
        now = QDate.currentDate()
        current_date = now.toString('ddd dd-MM-yyyy')
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.Date_Label.setText(current_time)

        with open('Attendance.csv', "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            self.Time_Label.setText(list(csv_reader)[-1][0])

        self._new_window = None
        self.Videocapture_ = None
        
    
    def execute_script(name):
        os.system('python ' + name) 

    def refreshAll(self):
        """
        Set the text of lineEdit once it's valid
        """
        self.Videocapture_ = "0"

    @pyqtSlot()
    def runSlot(self):
        """
        Called when the user presses the Run button
        """
        print("Clicked Run")
        self.refreshAll()
        print(self.Videocapture_)
        ui.hide()  # hide the main window
        self.outputWindow_()  # Create and open new output window

    def outputWindow_(self):
        """
        Created new window for vidual output of the video in GUI
        """
        self._new_window = Ui_OutputDialog()
        self._new_window.show()
        self._new_window.startVideo(self.Videocapture_)
        print("Video Played")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_Dialog1()
    ui.show()
    a = threading.Thread(target=execute_script, args=('laser_on.py',))
    a.start()
    sys.exit(app.exec_())
