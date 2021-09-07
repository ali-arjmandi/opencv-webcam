from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from view import Ui_view
from model import Camera

class Setting(Ui_view):
    def __init__(self, dialog):
        Ui_view.__init__(self)
        self.setupUi(dialog)

        self.threshold_min = 0
        self.threshold_max = 100
        self.threshold_default =20

        self.power_min = 80
        self.power_max = 5
        self.power_default = 20

        self.motion_contour_min = 0
        self.motion_contour_max = 2000
        self.motion_contour_default = 2000

        self.bg_sub_contour_min = 0
        self.bg_sub_contour_max = 2000
        self.bg_sub_contour_default = 2000

        self.bg_sub_threshold_min = 0
        self.bg_sub_threshold_max = 130
        self.bg_sub_threshold_default =40

        self.select_val = 50

        self.setting()

    def setting(self):
        self.setting_frame.setEnabled(False)
        self.mode_frame.setEnabled(False)
        self.motion_frame.setVisible(False)
        self.bg_sub_frame.setVisible(False)
        self.tracking_frame.setVisible(False)
        self.timer = QtCore.QTimer()
        self.select_timer = QtCore.QTimer()
        self.select_flag = False
        self.track_flag = False
        self.mode_flags = 0
        self.bg_img = None

        self.threshold_slider.setMinimum(self.threshold_min)
        self.threshold_slider.setMaximum(self.threshold_max)
        self.threshold_slider.setValue(self.threshold_default)
        self.threshold_slider.setTickInterval(self.threshold_slider.value())
        self.threshold_val = self.threshold_slider.value()

        self.power_slider.setMinimum(self.power_max)
        self.power_slider.setMaximum(self.power_min)
        self.power_slider.setValue((self.power_min+self.power_max)-self.power_slider.value())
        self.power_slider.setTickInterval(self.power_slider.value())
        self.power_val = self.power_slider.value()

        self.motion_contour_slider.setMinimum(self.motion_contour_min)
        self.motion_contour_slider.setMaximum(self.motion_contour_max)
        self.motion_contour_slider.setValue(self.motion_contour_default)
        self.motion_contour_slider.setTickInterval(self.motion_contour_slider.value())
        self.motion_contour_val = self.motion_contour_slider.value()

        self.bg_sub_contour_slider.setMinimum(self.bg_sub_contour_min)
        self.bg_sub_contour_slider.setMaximum(self.bg_sub_contour_max)
        self.bg_sub_contour_slider.setValue(self.bg_sub_contour_default)
        self.bg_sub_contour_slider.setTickInterval(self.bg_sub_contour_slider.value())
        self.bg_sub_contour_val = self.bg_sub_contour_slider.value()

        self.bg_sub_threshold_slider.setMinimum(self.bg_sub_threshold_min)
        self.bg_sub_threshold_slider.setMaximum(self.bg_sub_threshold_max)
        self.bg_sub_threshold_slider.setValue(self.bg_sub_threshold_default)
        self.bg_sub_threshold_slider.setTickInterval(self.bg_sub_threshold_slider.value())
        self.bg_sub_threshold_val = self.bg_sub_threshold_slider.value()
