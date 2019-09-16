# testing some of opencv tools

import cv2
import numpy as np


def window_is_open(windowname):
	return True if cv2.getWindowProperty(windowname, cv2.WND_PROP_VISIBLE) >= 1 else False



def mouse_callback_mar2(event,x,y,flags,param):
	if event == cv2.EVENT_FLAG_LBUTTON:
		cv2.circle(mar2,(x,y),10,(255,0,0),-1)
	elif event == cv2.EVENT_FLAG_RBUTTON:
		global oldx
		global oldy
		# green line from (oldx,oldy) to (x,y) with thickness=2 and antialiasing
		cv2.line(mar2,(x,y),(oldx,oldy),(0,255,0),2,cv2.LINE_AA)
		oldx = x
		oldy = y


# the global vars oldx and oldy are needed to store previous mouse position
oldx = 0
oldy = 0		
		
mar2 = cv2.imread('maracana2.jpg')
cv2.namedWindow('mar2', flags=cv2.WINDOW_GUI_NORMAL)	# hides status, toolbar etc.
cv2.resizeWindow('mar2', mar2.shape[1], mar2.shape[0])
cv2.setMouseCallback('mar2', mouse_callback_mar2)

medidas = cv2.imread('maraca.png')
medidas = cv2.resize(medidas, None, fx=0.25, fy=0.25)
cv2.namedWindow('medidas do campo', flags=cv2.WINDOW_GUI_NORMAL)	# hides status, toolbar etc.
cv2.resizeWindow('medidas do campo', medidas.shape[1], medidas.shape[0])
cv2.moveWindow('medidas do campo', 500,500)
#cv2.setMouseCallback('medidas do campo', mouse_callback_medidas)


while window_is_open('mar2') and window_is_open('medidas do campo'):
	cv2.imshow('mar2',mar2)
	cv2.imshow('medidas do campo', medidas)
	if cv2.waitKey(20) == 27:
		break
cv2.destroyAllWindows()




# PeqArea SupDir 473,99
#         SupEsq 508,177
#         InfDir 577,99 
# GraArea SupEsq 265,237
#         SupDir 267,61
#         InfDir 551,61
# Campo   InfDir 525,23