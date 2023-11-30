# Modified by Augmented Startups & Geeky Bee
# October 2020
# Facial Recognition Attendence GUI
# Full Course - https://augmentedstartups.info/yolov4release
# *-
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer, QDate, Qt
from PyQt5.QtWidgets import QDialog,QMessageBox
import cv2
import face_recognition
import numpy as np
import datetime
import os
import csv
import sys
import threading

def execute_script(name):
    os.system('python ' + name)    

class Ui_OutputDialog(QDialog):
    def __init__(self):
        super(Ui_OutputDialog, self).__init__()
        loadUi("./outputwindow.ui", self)

        self.ClockInButton.clicked.connect(self.runClockIn)
        self.image = None
    

    def runClockIn(self):
        capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        success, frame = capture.read()
        frame = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        path = 'ImagesAttendance'
        images = []
        class_names = []
        encode_list = []
        attendance_list = os.listdir(path)

        for cl in attendance_list:
            cur_img = cv2.imread(f'{path}/{cl}')
            images.append(cur_img)
            class_names.append(os.path.splitext(cl)[0])
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(img)
            encodes_cur_frame = face_recognition.face_encodings(img, boxes)[0]
            encode_list.append(encodes_cur_frame)
        faces_cur_frame = face_recognition.face_locations(frame)
        encodes_cur_frame = face_recognition.face_encodings(frame, faces_cur_frame)
        match = face_recognition.compare_faces(encode_list, encodes_cur_frame[0], tolerance=0.50)
        face_dis = face_recognition.face_distance(encode_list, encodes_cur_frame[0])
        name = "unknown"
        best_match_index = np.argmin(face_dis)
        if match[best_match_index]:
            name = class_names[best_match_index].upper()
        if name!="unknown":
            print(name,"has switched the laser on")
            f  = open("Attendance.csv", 'a')
            date_string = datetime.datetime.now().strftime("%d/%m/%y")
            time_string = datetime.datetime.now().strftime("%H:%M:%S")
            f.writelines(f'\n{name},{date_string},{time_string},SWITCHED ON')
            capture.release()
            self.capture.release()
            f.close()
            self.close()
            #subprocess.run(["python", "onWindow.py"])
            #subprocess.run(["python", "laser_on.py"])
            os.system(f'python C:/Users/rkail/OneDrive/Desktop/LaserTripwireProject/onWindow.py')
            '''a = threading.Thread(target=execute_script, args=('onWindow.py',))
            a.start()
            b = threading.Thread(target=execute_script, args=('laser_on.py',))
            b.start()
            a.join()
            b.join()'''
            os._exit(0)
        else:
            print("Face unrecognised")
            return


    @pyqtSlot()
    def startVideo(self, camera_name):
        """
        :param camera_name: link of camera or usb camera
        :return:
        """
        if len(camera_name) == 1:
        	self.capture = cv2.VideoCapture(int(camera_name))
        else:
        	self.capture = cv2.VideoCapture(camera_name)
        self.timer = QTimer(self)  # Create Timer
        path = 'ImagesAttendance'
        if not os.path.exists(path):
            os.mkdir(path)
        # known face encoding and known face name list
        images = []
        self.class_names = []
        self.encode_list = []
        self.TimeList1 = []
        self.TimeList2 = []
        attendance_list = os.listdir(path)

        # print(attendance_list)
        for cl in attendance_list:
            cur_img = cv2.imread(f'{path}/{cl}')
            images.append(cur_img)
            self.class_names.append(os.path.splitext(cl)[0])
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(img)
            encodes_cur_frame = face_recognition.face_encodings(img, boxes)[0]
            # encode = face_recognition.face_encodings(img)[0]
            self.encode_list.append(encodes_cur_frame)
        self.timer.timeout.connect(self.update_frame)  # Connect timeout to the output function
        self.timer.start(10)  # emit the timeout() signal at x=40ms

    def face_rec_(self, frame, encode_list_known, class_names):
        """
        :param frame: frame from camera
        :param encode_list_known: known face encoding
        :param class_names: known face names
        :return:
        """
        # face recognition
        faces_cur_frame = face_recognition.face_locations(frame)
        encodes_cur_frame = face_recognition.face_encodings(frame, faces_cur_frame)
        # count = 0
        for encodeFace, faceLoc in zip(encodes_cur_frame, faces_cur_frame):
            match = face_recognition.compare_faces(encode_list_known, encodeFace, tolerance=0.50)
            face_dis = face_recognition.face_distance(encode_list_known, encodeFace)
            name = "unknown"
            best_match_index = np.argmin(face_dis)
            # print("s",best_match_index)
            if match[best_match_index]:
                name = class_names[best_match_index].upper()
                y1, x2, y2, x1 = faceLoc
                cv2.rectangle(frame, (x1, y1), (x2, y2), (164, 10, 12), 2)
                cv2.rectangle(frame, (x1, y2 - 20), (x2, y2), (164, 10, 12), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

        return frame



    def update_frame(self):
        ret, self.image = self.capture.read()
        self.displayImage(self.image, self.encode_list, self.class_names, 1)

    def displayImage(self, image, encode_list, class_names, window=1):
        """
        :param image: frame from camera
        :param encode_list: known face encoding list
        :param class_names: known face names
        :param window: number of window
        :return:
        """
        image = cv2.resize(image, (640, 480))
        try:
            image = self.face_rec_(image, encode_list, class_names)
        except Exception as e:
            print(e)
        qformat = QImage.Format_Indexed8
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        outImage = outImage.rgbSwapped()

        if window == 1:
            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.imgLabel.setScaledContents(True)
