import cv2
import time
import datetime
import ctypes
from win10toast import ToastNotifier
import win32api
import psutil

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
false_negative = 0
start_time = datetime.datetime.now()
savedpos = win32api.GetCursorPos()
while True:
    false_negative = 0
    savedpos = win32api.GetCursorPos()
    curpos = win32api.GetCursorPos()
    start_time = datetime.datetime.now()
    if savedpos != curpos:
        savedpos = curpos
    else:
        it_is_fine = False
        start_time = datetime.datetime.now()
        while savedpos == curpos:
            curpos = win32api.GetCursorPos()
            time_diff = datetime.datetime.now() - start_time
            time_diff = time_diff.total_seconds()/60
            if time_diff >= 5:
                while True:
                    curpos = win32api.GetCursorPos()
                    if savedpos!=curpos:
                        break
                    cap = cv2.VideoCapture(0)
                    _, img = cap.read()
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                    if len(faces) != 0:
                        false_negative = 0
                        it_is_fine = True
                        cap.release()
                        break
                    if (len(faces) == 0):
                        false_negative += 1
                        if false_negative == 2:
                            cap.release()
                            toaster = ToastNotifier()
                            toaster.show_toast("PC will Lock now in 1 Minute", "Show face/move mouse to prevent it!",
                                               icon_path="custom.ico")
                            for_ten_second = datetime.datetime.now()
                            while True:
                                curpos = win32api.GetCursorPos()
                                if savedpos!=curpos:
                                    toaster.show_toast("PC will not Lock!",
                                                       "Face Detected!",
                                                       icon_path="custom.ico")
                                    it_is_fine = True
                                    break
                                break_cond = datetime.datetime.now() - for_ten_second
                                break_cond = break_cond.total_seconds()/60
                                if break_cond >= .1:
                                    break
                            for_ten_second = datetime.datetime.now()
                            while True:
                                curpos = win32api.GetCursorPos()
                                if savedpos!=curpos:
                                    it_is_fine = True
                                    break
                                cap = cv2.VideoCapture(0)
                                _, img = cap.read()
                                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                                if len(faces) != 0:
                                    toaster.show_toast("PC will not Lock!",
                                                       "Face Detected!",
                                                       icon_path="custom.ico")
                                    false_negative = 0
                                    it_is_fine = True
                                    cap.release()
                                    break
                                time_diff_ten = datetime.datetime.now() - for_ten_second
                                time_diff_ten = time_diff_ten.total_seconds()/60
                                if time_diff_ten >= .1:
                                    false_negative = 3
                                    break
                            if it_is_fine:
                                break
                        if false_negative == 3:
                            ctypes.windll.user32.LockWorkStation()
                            out = False
                            cap.release()
                            while not out:
                                time.sleep(60)
                                inside = False
                                for proc in psutil.process_iter():
                                    if (proc.name() == "LogonUI.exe"):
                                        inside = True
                                if not inside:
                                    out = True
                                    break
                                false_negative = 0
                    cap.release()
                    time.sleep(60)
            if it_is_fine:
                break
    time.sleep(60)