import cv2
import os
import time
import datetime as DT
import ctypes
import json

# Сохранить изображение - ЛКМ
# Закрыть - q или Esc
import imutils

# 192.168.4.136
# 2592x1944

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
    interpolation = "interpolation " + str(width_display) +" X "+ str(height_display)
cap.set(cv2.CAP_PROP_FPS, data['CAP_PROP_FPS'])
cap.set(15, data['Exp'])

cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, data['CAP_PROP_AUTO_EXPOSURE'])
cap.set(cv2.CAP_PROP_AUTO_WB, data['CAP_PROP_AUTO_WB'])
cap.set(cv2.CAP_PROP_AUTOFOCUS, data['CAP_PROP_AUTOFOCUS'])


# if width_cam > 1280:
#     width_display_cam = 1280
#     height_display_cam = 960
# elif width_cam == 1280:
#     width_display_cam = 1024
#     height_display_cam = 768
# elif width_cam < 1280:
#     width_display_cam = 640
#     height_display_cam = 480
# print(width_display_cam, height_display_cam)

if width_display > 1280:

    startx = int((width_display - 1280) / 2)
    endx = int(width_display - startx)
    starty = int(height_display * 0.10)
    endy = int(height_display * 0.65)

    print(startx, starty, endx, endy)






def savepic(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        time.sleep(0.1)
        format = (str(DT.datetime.now()).split('.')[0].replace(':', '').replace('-', '').replace(' ', ''))
        img = frame[28:28 + 1024, 320:320 + 1280]
        cv2.imwrite(os.path.join(dirfull, "colposcopy_{}.png".format(format)), img)
        time.sleep(0.1)


def exceptions(E):
    fail = open('fail.txt', 'a')
    fail.write(str(DT.datetime.now()) + E + '\n')
    fail.close()




while (cap.isOpened()):

    # Создаем объект изображения
    try:
        ret, frame = cap.read()
    except Exception as Exc:
        print(Exc)
        exceptions(str(Exc))
        break

    # Накладываем текст
    # font = cv2.FONT_HERSHEY_PLAIN
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    dementions_display_position = (15, 20)
    dementions_camera_position = (15, 40)
    brand_position = (150, 300)
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
    cv2.rectangle(frame, (startx, starty), (endx, endy), (255, 255, 255), 3)
    # cv2.rectangle(image, start_point, end_point, color, thickness)
    #cv2.rectangle(frame, (width_display, height2), (width_display + 1280, height2 + 1024), (255, 255, 255), 3)
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.moveWindow(name, 0, 0)
    try:
        cv2.imshow(name, frame)
    except Exception as E:
        exceptions(str(E))
    cv2.setMouseCallback(name, savepic)
    w = cv2.waitKey(1)

    if w & 0xFF == ord('q') or w == 27:
        break
cap.release()
cv2.destroyAllWindows()
f.close()
