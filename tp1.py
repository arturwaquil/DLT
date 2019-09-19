import cv2
import numpy as np
import DLT

clicked = False
cursorX = 0
cursorY = 0


def mouse_callback(event,x,y,flags,param):
	img, origImg = param
	if event == cv2.EVENT_FLAG_LBUTTON:
	#   img = origImg.copy()
	#    cv2.line(img,(x,0),(x,img.shape[0]),(0,0,255),2,cv2.LINE_AA)
	#elif event == cv2.EVENT_FLAG_RBUTTON:
		global clicked, cursorX, cursorY
		clicked = True
		cursorX = x
		cursorY = y
		
def window_is_open(windowname):
	return True if cv2.getWindowProperty(windowname, cv2.WND_PROP_VISIBLE) >= 1 else False

#Direct Linear Transformation
def dlt(pixelCoords, worldCoords):
	if len(pixelCoords) != len(worldCoords):
		print("Erro: Quantidade diferente de pontos.")
		return None
	else:    
		numPoints = len(worldCoords)

	#Tworld, worldCoords = Normalization(3, np.asarray(worldCoords))
	#Tpixel, pixelCoords = Normalization(2, np.asarray(pixelCoords))

	A = []

	for i in range(numPoints): 
		x, y, z, w = worldCoords[i][0], worldCoords[i][1], worldCoords[i][2], 1
		u, v = pixelCoords[i][0], pixelCoords[i][1]
		A.append([x, y, z, w, 0, 0, 0, 0, -u*x, -u*y, -u*z, -u])
		A.append([0, 0, 0, 0, x, y, z, w, -v*x, -v*y, -v*z, -v])
		

	#for i in A:
	#    print(i)

	U, S, Vh = np.linalg.svd(np.asarray(A))

	P = Vh[-1,:] / Vh[-1,-1]  # The parameters are in the last line of Vh 
	P = P.reshape(3,4)
	'''
	H = np.dot( np.dot( np.linalg.pinv(Tpixel), H ), Tworld )
	print(H)
	H = H / H[-1, -1]
	print(H)
	P = H.flatten(0)'''
	print(P)


	return P


def main():


	pixelCoords =  [[ 99, 473],	# PeqArea SupDir
					[177, 508],	# PeqArea SupEsq
					[ 99, 577],	# PeqArea InfDir
					[237, 265],	# GraArea SupEsq 
					[ 61, 267],	# GraArea SupDir
					[ 61, 551],	# GraArea InfDir
					[ 23, 525]]	# Campo   InfDir
	
	#Origem na trave direita, X paralelo à linha de fundo e Y paralelo à lateral
	worldCoords =  [[     0,  5.5, 0],	# PeqArea SupDir
					[-18.32,  5.5, 0],	# PeqArea SupEsq
					[     0,    0, 0],	# PeqArea InfDir
					[-29.32, 16.5, 0],	# GraArea SupEsq
					[    11, 16.5, 0],	# GraArea SupDir
					[    11,    0, 0],	# GraArea InfDir 
					[ 24.84,    0, 0]]	# Campo   InfDir 
	
	""" Camera Resectioning - Finding the Camera Matrix P """
	P = dlt(pixelCoords, worldCoords)
	
	if P is None:
		return
 
	# 2D -> 2D projection (Z=0)
	P_2D = np.append(P[:,:2], P[:,3:], axis=1) # Elimination of column 3
	P_2D_Inv = np.linalg.inv(P_2D)
	
		
	""" Ex2 """
	origImg = cv2.imread('maracana2.jpg')
	img = origImg.copy()
	cv2.namedWindow('image', flags=cv2.WINDOW_GUI_NORMAL)    # hides status, toolbar etc.
	cv2.resizeWindow('image', img.shape[1], img.shape[0])
	cv2.setMouseCallback('image', mouse_callback, (img,origImg))

	while window_is_open('image'):
		cv2.imshow('image',img)

		if clicked:
			# IMPLEMENTAR AQUI IDENTIFICACAO E PRINT DA LINHA
			img = origImg.copy()
			cv2.line(img,(cursorX,0),(cursorX,img.shape[0]),(0,0,255),2,cv2.LINE_AA)

		if cv2.waitKey(20) == 27:
			break
	cv2.destroyAllWindows()


if __name__ == "__main__":
	main()