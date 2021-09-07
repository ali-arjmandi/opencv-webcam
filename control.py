from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import cv2
from settings import Setting
from view import Ui_view
from model import Camera
import sys

dots = []

class Project(Setting):
    def __init__(self, dialog):
        Setting.__init__(self, dialog)

        self.btnExit.clicked.connect(self.exit_act)
        self.btnWebcam.clicked.connect(self.webcam_act)
        self.btnLoad.clicked.connect(self.load_act)
        self.btnPlay.clicked.connect(self.play_act)
        self.btnTest.clicked.connect(self.test_act)
        self.btnMotion.clicked.connect(self.motion_act)
        self.btnBgSub.clicked.connect(self.bg_sub_act)
        self.btnSetBg.clicked.connect(self.set_bg_act)
        self.btnTracking.clicked.connect(self.tracking_act)
        self.btnSelectTracking.clicked.connect(self.select_tracking_act)
        self.timer.timeout.connect(self.show_movie)
        self.select_timer.timeout.connect(self.select)
        self.power_slider.valueChanged.connect(self.power_change)
        self.motion_contour_slider.valueChanged.connect(self.motion_counter_change)
        self.threshold_slider.valueChanged.connect(self.threshold_change)
        self.bg_sub_threshold_slider.valueChanged.connect(self.bg_sub_threshold_change)
        self.motion_contour_check.stateChanged.connect(self.motion_contour_check_on_off)
        self.threshold_check.stateChanged.connect(self.threshold_check_on_off)
        self.bg_sub_contour_check.stateChanged.connect(self.bg_sub_contour_check_on_off)
        self.optical_flow_check.stateChanged.connect(self.optical_flow_check_on_off)
        self.label.mousePressEvent = self.getPos

    def test_act(self):
        print("Ssssssssssss")

    def threshold_check_on_off(self):
        if not self.threshold_check.isChecked():
            self.threshold_slider.setEnabled(False)
        else:
            self.threshold_slider.setEnabled(True)

    def motion_contour_check_on_off(self):
        if self.motion_contour_check.isChecked():
            self.motion_contour_slider.setEnabled(True)
        else:
            self.motion_contour_slider.setEnabled(False)

    def bg_sub_contour_check_on_off(self):
        if self.bg_sub_contour_check.isChecked():
            self.bg_sub_threshold_check.setChecked(True)
            self.bg_sub_threshold_check.setEnabled(False)
        else:
            self.bg_sub_threshold_check.setEnabled(True)

    def optical_flow_check_on_off(self):
        if self.optical_flow_check.isChecked():
            self.camera.optical_flow_initialize(self.camera.get_frame())

    def power_change(self):
        self.power_val = (self.power_min+self.power_max)-self.power_slider.value()
        if self.timer.isActive:
            self.timer.setInterval(self.power_val)

    def motion_counter_change(self):
        self.motion_contour_val = self.motion_contour_slider.value()

    def threshold_change(self):
        self.threshold_val = self.threshold_slider.value()

    def bg_sub_threshold_change(self):
        self.bg_sub_threshold_val = self.bg_sub_threshold_slider.value()

    def select_tracking_act(self):
        global dots
        dots = []
        self.select_flag = False
        self.track_flag = False


    def select(self):
        print(x1,y1,x2,y2)

    def tracking_act(self):
        if self.btnTracking.text() == "ON":
            self.btnTracking.setText("OFF")
            if self.btnMotion.text() == "OFF" or self.btnBgSub.text() == "OFF":
                self.btnMotion.setText("ON")
                self.btnBgSub.setText("ON")
            else:
                self.mode_flags += 1
            self.setting_frame.setVisible(False)
            self.motion_frame.setVisible(False)
            self.bg_sub_frame.setVisible(False)
            self.tracking_frame.setVisible(True)
            self.motion_contour_check.setChecked(False)
            self.bg_sub_contour_check.setChecked(False)

        else:
            self.btnTracking.setText("ON")
            self.setting_frame.setVisible(True)
            self.tracking_frame.setVisible(False)
            self.mode_flags -= 1

    def bg_sub_act(self):
        if self.btnBgSub.text() == "ON":
            self.btnBgSub.setText("OFF")
            if self.btnMotion.text() == "OFF" or self.btnTracking.text() == "OFF":
                self.btnMotion.setText("ON")
                self.btnTracking.setText("ON")
            else:
                self.mode_flags += 1
            try:
                if not self.bg_img:
                    self.bg_img = self.camera.get_frame()
            except:
                pass
            self.setting_frame.setVisible(False)
            self.motion_frame.setVisible(False)
            self.tracking_frame.setVisible(False)
            self.bg_sub_frame.setVisible(True)
            self.motion_contour_check.setChecked(False)

        else:
            self.btnBgSub.setText("ON")
            self.bg_sub_contour_check.setChecked(False)
            self.bg_sub_frame.setVisible(False)
            self.setting_frame.setVisible(True)
            self.mode_flags -= 1

    def motion_act(self):
        if self.btnMotion.text() == "ON":
            self.btnMotion.setText("OFF")
            if self.btnBgSub.text() == "OFF" or self.btnTracking.text() == "OFF":
                self.btnBgSub.setText("ON")
                self.btnTracking.setText("ON")
            else:
                self.mode_flags += 1
            self.setting_frame.setVisible(False)
            self.bg_sub_frame.setVisible(False)
            self.tracking_frame.setVisible(False)
            self.motion_frame.setVisible(True)
            self.bg_sub_contour_check.setChecked(False)
        else:
            self.btnMotion.setText("ON")
            self.motion_frame.setVisible(False)
            self.motion_contour_check.setChecked(False)
            self.setting_frame.setVisible(True)
            self.mode_flags -= 1

    def set_bg_act(self):
        self.bg_img = self.camera.last_frame

    def play_act(self):
        if self.btnPlay.text() =="Play":
            self.btnPlay.setText("Pause")
            self.timer.start(self.power_val)
        else:
            self.btnPlay.setText("Pause")
            self.btnPlay.setText("Play")
            self.timer.stop()

    def load_act(self):
        name = QFileDialog.getOpenFileName(None,"Open video File", '.')
        self.btnPlay.setEnabled(True)
        self.setting_frame.setEnabled(True)
        self.mode_frame.setEnabled(True)
        self.camera = Camera(name[0])
        self.camera.initialize()
        self.camera.get_frame()

    def webcam_act(self):
        self.btnPlay.setEnabled(True)
        self.setting_frame.setEnabled(True)
        self.mode_frame.setEnabled(True)
        self.camera = Camera(0)
        self.camera.initialize()
        self.camera.get_frame()

    def show_movie(self):
        try:
            global dots
            frame = self.camera.get_frame()
            # Not mode
            if self.mode_flags == 0:
                if self.gray_radio.isChecked():
                    frame = self.camera.gray(frame)
                elif self.hsv_radio.isChecked():
                    frame = self.camera.hsv(frame)
                if self.threshold_check.isChecked():
                    frame = self.camera.threshold(frame,self.threshold_val)
            else:   # mode

                if self.btnMotion.text()=="OFF":
                    if self.motion_gray_radio.isChecked():
                        flag = True
                    else:
                        flag = False
                    frame = self.camera.motion(frame,flag)
                    if self.motion_contour_check.isChecked():
                        frame = self.camera.find_contours(frame, self.motion_contour_val, self.label)

                elif self.btnBgSub.text()=="OFF":
                    frame = self.camera.bg_sub(self.bg_img,frame)
                    if self.bg_sub_threshold_check.isChecked():
                        frame = self.camera.threshold(frame, self.bg_sub_threshold_val)
                    if self.bg_sub_contour_check.isChecked():
                        frame = self.camera.find_contours(frame, self.bg_sub_contour_val, self.label)

                elif self.btnTracking.text()=="OFF":
                    if self.track_flag == True and not self.optical_flow_check.isChecked():
                        frame = self.camera.tracking(frame)
                    if self.optical_flow_check.isChecked():
                        frame = self.camera.optical_flow(frame)



            if not self.bg_sub_contour_check.isChecked() or not self.motion_gray_radio.isChecked():
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = QImage(img, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(image)
                pixmap = pixmap.scaledToWidth(self.label.width())
                self.label.setPixmap(pixmap)


        except:
           self.btnPlay.setText("Pause")
           self.btnPlay.setText("Play")
           self.timer.stop()
           self.camera.initialize()

    def getPos(self, event):
        if self.btnPlay.text() =="Pause":
            global dots
            m = self.camera.last_frame.shape[1]/self.label.width()
            if self.track_flag == False and self.btnTracking.text() == "OFF":
                if self.select_flag == False :
                    dots = []
                    self.select_flag = True
                    x1 = int(event.pos().x()*m)
                    dots.append(x1)
                    y1 = int(event.pos().y()*m)
                    dots.append(y1)
                else:
                    self.select_flag = False
                    x2 = int(event.pos().x()*m)
                    dots.append(x2)
                    y2 = int(event.pos().y()*m)
                    dots.append(y2)
                    self.track_flag = True
                    self.camera.tracking_initialize(self.camera.get_frame(), dots)

    def exit_act(self):
        print("exit")

def main():


    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    prog = Project(dialog)
    dialog.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
