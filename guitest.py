# testing some of opencv tools

import cv2
import numpy as np


def window_is_open(windowname):
	return True if cv2.getWindowProperty(windowname, cv2.WND_PROP_VISIBLE) >= 1 else False


def mouse_callback(event,x,y,flags,param):
	img = param
	if event == cv2.EVENT_FLAG_LBUTTON:
		cv2.circle(img,(x,y),5,(0,0,255),-1)

'''
def mouse_callback_medidas(event,x,y,flags,param):
	if event == cv2.EVENT_FLAG_LBUTTON:
		cv2.circle(medidas,(x,y),10,(255,0,0),-1)
	elif event == cv2.EVENT_FLAG_RBUTTON:
		global oldx2
		global oldy2
		# green line from (oldx,oldy) to (x,y) with thickness=2 and antialiasing
		cv2.line(medidas,(x,y),(oldx2,oldy2),(0,255,0),2,cv2.LINE_AA)
		oldx2 = x
		oldy2 = y
'''

mar2 = cv2.imread('maracana2.jpg')
cv2.namedWindow('mar2', flags=cv2.WINDOW_GUI_NORMAL)
cv2.resizeWindow('mar2', mar2.shape[1], mar2.shape[0])
cv2.setMouseCallback('mar2', mouse_callback, mar2)

medidas = cv2.imread('maraca.png')
medidas = cv2.resize(medidas, None, fx=0.3, fy=0.3)
cv2.namedWindow('medidas do campo', flags=cv2.WINDOW_GUI_NORMAL)
cv2.resizeWindow('medidas do campo', medidas.shape[1], medidas.shape[0])
cv2.moveWindow('medidas do campo', 500,500)
cv2.setMouseCallback('medidas do campo', mouse_callback, medidas)


while window_is_open('mar2') and window_is_open('medidas do campo'):
	cv2.imshow('mar2',mar2)
	cv2.imshow('medidas do campo', medidas)
	if cv2.waitKey(20) == 27:
		break
cv2.destroyAllWindows()