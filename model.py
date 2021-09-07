import cv2
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Camera:
    def __init__(self, cam_val):
        self.cap = None
        self.cam_val = cam_val
        self.motion_mode =  cv2.createBackgroundSubtractorMOG2(history=70)

    def initialize(self):
        self.cap = cv2.VideoCapture(self.cam_val)

    def tracking_initialize(self,frame,dots):
        c,r,w,h = dots[0],dots[1],dots[2]-dots[0],dots[3]-dots[1]  # simply hardcoded the values
        self.track_window = (c,r,w,h)

        # set up the ROI for tracking
        roi = frame[r:r+h, c:c+w]
        hsv_roi =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
        self.roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
        cv2.normalize(self.roi_hist,self.roi_hist,0,255,cv2.NORM_MINMAX)
        # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
        self.term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

    def optical_flow_initialize(self,frame):
        feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )
        # Parameters for lucas kanade optical flow
        self.lk_params = dict( winSize  = (15,15),
                          maxLevel = 2,
                          criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        # Create some random colors
        self.color = np.random.randint(0,255,(100,3))
        # Take first frame and find corners in it
        old_frame = frame
        self.old_gray = self.gray(old_frame)
        self.p0 = cv2.goodFeaturesToTrack(self.old_gray, mask = None, **feature_params)
        # Create a mask image for drawing purposes
        self.mask = np.zeros_like(old_frame)

    def get_frame(self):
        ret, self.last_frame = self.cap.read()
        return self.last_frame

    def gray(self, input_frame):
        frame = cv2.cvtColor(input_frame, cv2.COLOR_BGR2GRAY)
        return frame

    def hsv(self, input_frame):
        frame = cv2.cvtColor(input_frame, cv2.COLOR_BGR2HSV)
        return frame

    def threshold(self, input_frame, val):
        retval, frame = cv2.threshold(input_frame, val, 255,0)
        return frame

    def motion(self, input_frame,flag=False):
        if flag:
            frame = self.gray(input_frame)
        else:
            frame = self.hsv(input_frame)
        frame = self.motion_mode.apply(frame)
        frame = self.threshold(frame,240)
        return frame

    def bg_sub(self,bg,img):
        bg = self.gray(bg)
        img = self.gray(img)
        diff = cv2.absdiff(bg, img)
        diff = cv2.GaussianBlur(diff, (3, 3), 0)
        return diff

    def tracking(self, frame):
        hsv = self.hsv(frame)
        dst = cv2.calcBackProject([hsv],[0],self.roi_hist,[0,180],1)

        # apply meanshift to get the new location
        ret, track_window = cv2.meanShift(dst, self.track_window, self.term_crit)

        # Draw it on image
        x,y,w,h = track_window
        frame = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
        #==============================================
        # hsv = self.hsv(frame)
        # dst = cv2.calcBackProject([hsv],[0],self.roi_hist,[0,180],1)
        #
        # ret, self.track_window = cv2.CamShift(dst, self.track_window, self.term_crit)
        #
        # # Draw it on image
        # pts = cv2.boxPoints(ret)
        # pts = np.int0(pts)
        # frame = cv2.polylines(frame,[pts],True, 255,2)

        return frame

    def optical_flow(self,frame):
        frame_gray = self.gray(frame)
        # calculate optical flow
        self.p1, st, err = cv2.calcOpticalFlowPyrLK(self.old_gray, frame_gray, self.p0, None, **self.lk_params)

        # Select good points
        good_new = self.p1[st==1]
        good_old = self.p0[st==1]

        # draw the tracks
        for i,(new,old) in enumerate(zip(good_new,good_old)):
            a,b = new.ravel()
            c,d = old.ravel()
            self.mask = cv2.line(self.mask, (a,b),(c,d), self.color[i].tolist(), 2)
            frame = cv2.circle(frame,(a,b),5,self.color[i].tolist(),-1)
        img = cv2.add(frame,self.mask)
        return img
    def find_contours(self, frame, contour_val, label):
         contours, _ = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
         for contour in contours:
            if cv2.contourArea(contour ) > contour_val:
                x,y,w,h = cv2.boundingRect(contour )
                frame = cv2.rectangle(self.last_frame,(x,y),(x+w,y+h),(0,255,0),2)
         img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
         image = QImage(img, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888)
         pixmap = QPixmap.fromImage(image)
         pixmap = pixmap.scaledToWidth(label.width())
         label.setPixmap(pixmap)
         return self.last_frame



    def close(self):
        self.cap.release()

    def __str__(self):
        return self.cam_val
