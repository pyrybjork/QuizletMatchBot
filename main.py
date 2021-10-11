import win32api, win32con
import keyboard
import time
import cv2
from PIL import ImageGrab
from PIL import Image
import numpy as np

# show | click
mode = 'click'

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

#loading my images of the answer pairs
#needle images
imgs = [[cv2.imread('./kpl4/anemia0.png', 1), cv2.imread('./kpl4/anemia1.png', 1)],
[cv2.imread('./kpl4/fibriini0.png', 1), cv2.imread('./kpl4/fibriini1.png', 1)],
[cv2.imread('./kpl4/punasolu0.png', 1), cv2.imread('./kpl4/punasolu1.png', 1)],
[cv2.imread('./kpl4/valkosolu0.png', 1), cv2.imread('./kpl4/valkosolu1.png', 1)],
[cv2.imread('./kpl4/verihiutale0.png', 1), cv2.imread('./kpl4/verihiutale1.png', 1)],
[cv2.imread('./kpl4/verineste0.png', 1), cv2.imread('./kpl4/erineste1.png', 1)]]

colors = [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255)]

keyboard.wait('enter')
print('started')

while True:

    #game area on my screen 1530, 146 ; 2054, 1376
    #haystack image
    img = ImageGrab.grab(bbox=(1530, 146, 2054, 1376))
    img_np = np.array(img)

    for i in range(6):
        img1 = imgs[i][0]
        img2 = imgs[i][1]

        result1 = cv2.matchTemplate(img_np, img1, cv2.TM_CCOEFF_NORMED)
        result2 = cv2.matchTemplate(img_np, img2, cv2.TM_CCOEFF_NORMED)

        min_val1, max_val1, min_loc1, max_loc1 = cv2.minMaxLoc(result1)
        min_val2, max_val2, min_loc2, max_loc2 = cv2.minMaxLoc(result2)

        print('1', max_loc1, '|', max_val1, '\n2', max_loc2, '|', max_val2)

        if max_val1 > 0.8 and max_val2 > 0.8:

            if mode == 'click':
                time.sleep(0.05)
                click(max_loc1[0]+1530, max_loc1[1]+146)
                time.sleep(0.05)
                click(max_loc2[0]+1530, max_loc2[1]+146)
            elif mode == 'show':
                cv2.rectangle(img_np, max_loc1, (max_loc1[0] + imgs[i][0].shape[1], max_loc1[1] + imgs[i][0].shape[0]),
                                color=colors[i], thickness=2, lineType=cv2.LINE_4)
                cv2.rectangle(img_np, max_loc2, (max_loc2[0] + imgs[i][1].shape[1], max_loc2[1] + imgs[i][1].shape[0]),
                                color=colors[i], thickness=2, lineType=cv2.LINE_4)

        else:
            print('not found')


    if mode == 'show':
        im_pil = Image.fromarray(img_np)
        im_pil.show()

    keyboard.wait('enter')
