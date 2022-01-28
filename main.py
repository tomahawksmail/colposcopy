import cv2
import os
import time
import datetime as DT
import ctypes
import json
interpolation = ""
#pyinstaller -F --noconsole main.py
#http://www.learningaboutelectronics.com/images/Text-added-to-blank-image-Python-OpenCV.png
# Сохранить изображение - ЛКМ
# Закрыть - q или Esc
#import imutils

# 192.168.4.136
# 2592x1944
# 0. CV_CAP_PROP_POS_MSEC Current position of the video file in milliseconds.
# 1. CV_CAP_PROP_POS_FRAMES 0-based index of the frame to be decoded/captured next.
# 2. CV_CAP_PROP_POS_AVI_RATIO Relative position of the video file
# 3. CV_CAP_PROP_FRAME_WIDTH Width of the frames in the video stream.
# 4. CV_CAP_PROP_FRAME_HEIGHT Height of the frames in the video stream.
# 5. CV_CAP_PROP_FPS Frame rate.
# 6. CV_CAP_PROP_FOURCC 4-character code of codec.
# 7. CV_CAP_PROP_FRAME_COUNT Number of frames in the video file.
# 8. CV_CAP_PROP_FORMAT Format of the Mat objects returned by retrieve() .
# 9. CV_CAP_PROP_MODE Backend-specific value indicating the current capture mode.
# 10. CV_CAP_PROP_BRIGHTNESS Brightness of the image (only for cameras).
# 11. CV_CAP_PROP_CONTRAST Contrast of the image (only for cameras).
# 12. CV_CAP_PROP_SATURATION Saturation of the image (only for cameras).
# 13. CV_CAP_PROP_HUE Hue of the image (only for cameras).
# 14. CV_CAP_PROP_GAIN Gain of the image (only for cameras).
# 15. CV_CAP_PROP_EXPOSURE Exposure (only for cameras).
# 16. CV_CAP_PROP_CONVERT_RGB Boolean flags indicating whether images should be converted to RGB.
# 17. CV_CAP_PROP_WHITE_BALANCE Currently unsupported
# 18. CV_CAP_PROP_RECTIFICATION Rectification flag for stereo cameras (note: only supported by DC1394 v 2.x backend currently)

f = open('config.json')
data = json.load(f)

name = data['name']
dir = os.path.abspath(os.curdir)
dirfull = dir + '\\' + str(DT.datetime.now().strftime("%Y%m%d"))
if not os.path.exists(os.path.abspath(dirfull)):
    os.mkdir(dirfull)


user32 = ctypes.windll.user32
width_display = user32.GetSystemMetrics(0)
height_display = user32.GetSystemMetrics(1)

cap = cv2.VideoCapture(data['channel'])

width_cam = int(cap.get(3))
height_cam = int(cap.get(4))

if data['interpolation' ] == 0:
    cap.set(3, width_cam)
    cap.set(4, height_cam)
    interpolation = "interpolation off"
elif data['interpolation'] == 1:
    cap.set(3, width_display)
    cap.set(4, height_display)
    width_cam = int(cap.get(3))
    height_cam = int(cap.get(4))

    if width_cam >= 1280:
        startx = int(width_cam * 0.2)
        endx = int(width_cam * 0.8)
        starty = int(height_cam * 0.07)
        endy = int(height_cam * 0.93)
        print(startx, starty, endx, endy)
    else:
        startx = int(width_cam * 0.05)
        endx = int(width_cam * 0.7)
        starty = int(height_cam * 0.05)
        endy = int(height_cam * 0.7)
        print(startx, starty, endx, endy)
    interpolation = "interpolation " + str(width_cam) +" X "+ str(height_cam)
cap.set(cv2.CAP_PROP_FPS, data['CAP_PROP_FPS'])
cap.set(15, data['Exp'])

cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, data['CAP_PROP_AUTO_EXPOSURE'])
cap.set(cv2.CAP_PROP_AUTO_WB, data['CAP_PROP_AUTO_WB'])
cap.set(cv2.CAP_PROP_AUTOFOCUS, data['CAP_PROP_AUTOFOCUS'])


def savepic(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        safedata = DT.datetime.strftime((DT.datetime.now()), '%Y-%m-%d-%H:%M')
        time.sleep(0.1)
        format = (str(DT.datetime.now()).split('.')[0].replace(':', '').replace('-', '').replace(' ', ''))
        cv2.putText(frame, safedata, (int(endx*0.75), int(endy*0.97)), font, fontScale, fontColor, lineType)
        img = frame[starty:endy, startx:endx]
        # img = frame[28:28 + 1024, 320:320 + 1280]

            # cv2.imwrite(os.path.join(dirfull, "colposcopy_{}.png".format(format)), img)
        cv2.imwrite(os.path.join("D:\\", "colposcopy_{}.png".format(format)), img)



        time.sleep(0.1)


def exceptions(E):
    fail = open('fail.txt', 'a')
    fail.write(str(DT.datetime.now()) +" >> "+ E + '\n')
    fail.close()




while (cap.isOpened()):

    # Создаем объект изображения

    ret, frame = cap.read()


    # Накладываем текст
    # font = cv2.FONT_HERSHEY_PLAIN
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    dementions_display_position = (15, 20)
    dementions_camera_position = (15, 40)
    brand_position = (int(endx*0.8), int(starty*2))
    fontScale = 1
    fontColor = (150, 150, 150)
    lineType = 1

    dementions_display = "display resolution " + str(int(width_display)) + 'px X ' + str(int(height_display)) + 'px'
    cv2.putText(frame, dementions_display, dementions_display_position, font, fontScale, fontColor, lineType)

    dementions_camera = "camera resolution " + str(int(width_cam)) + 'px X ' + str(int(height_cam)) + 'px ' + interpolation
    cv2.putText(frame, dementions_camera, dementions_camera_position, font, fontScale, fontColor, lineType)



    dementions_brand = data['brand']
    cv2.putText(frame, dementions_brand, brand_position, cv2.FONT_HERSHEY_SIMPLEX, fontScale * 2,
                fontColor,
                lineType * 2)
    cv2.rectangle(frame, (startx, starty), (endx, endy), (255, 255, 255), 2)
    # cv2.rectangle(image, start_point, end_point, color, thickness)
    # cv2.rectangle(frame, (width_display, height_display), (width_display + 1280, height_display + 1024), (255, 255, 255), 3)
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.moveWindow(name, 0, 0)
    cv2.imshow(name, frame)
    cv2.setMouseCallback(name, savepic)
    w = cv2.waitKey(1)

    if w & 0xFF == ord('q') or w == 27:
        break

cap.release()
cv2.destroyAllWindows()
f.close()
