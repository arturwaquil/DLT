# testing some of opencv tools

import cv2
import numpy as np


def window_is_open(windowname):
	return True if cv2.getWindowProperty(windowname, cv2.WND_PROP_VISIBLE) >= 1 else False



def mouse_callback(event,x,y,flags,param):
	if event == cv2.EVENT_FLAG_LBUTTON:
		cv2.circle(img,(x,y),10,(255,0,0),-1)
	elif event == cv2.EVENT_FLAG_RBUTTON:
		global oldx
		global oldy
		# green line from (oldx,oldy) to (x,y) with thickness=2 and antialiasing
		cv2.line(img,(x,y),(oldx,oldy),(0,255,0),2,cv2.LINE_AA)
		oldx = x
		oldy = y


# the global vars oldx and oldy are needed to store previous mouse position
oldx = 0
oldy = 0		
		
#img = np.zeros((512,512,3), np.uint8)
img = cv2.imread('maracana2.jpg')
cv2.namedWindow('image', flags=cv2.WINDOW_GUI_NORMAL)	# hides status, toolbar etc.
cv2.resizeWindow('image', img.shape[1], img.shape[0])
cv2.setMouseCallback('image', mouse_callback)

while window_is_open('image'):
	cv2.imshow('image',img)
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