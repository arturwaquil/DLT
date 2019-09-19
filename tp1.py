import cv2
import numpy as np
import DLT

clicked = False
cursorX = 0
cursorY = 0


def mouse_callback(event,x,y,flags,param):
	img, origImg = param
	if event == cv2.EVENT_FLAG_LBUTTON:
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

	A = []

	for i in range(numPoints): 
		x, y, z, w = worldCoords[i][0], worldCoords[i][1], 0, 1
		u, v = pixelCoords[i][0], pixelCoords[i][1]
		A.append([x, y, z, w, 0, 0, 0, 0, -u*x, -u*y, -u*z, -u])
		A.append([0, 0, 0, 0, x, y, z, w, -v*x, -v*y, -v*z, -v])
		
	U, S, Vh = np.linalg.svd(np.asarray(A))

	P = Vh[-1,:] / Vh[-1,-1]  # The parameters are in the last line of Vh 
	P = P.reshape(3,4)
	'''
	H = np.dot( np.dot( np.linalg.pinv(Tpixel), H ), Tworld )
	print(H)
	H = H / H[-1, -1]
	print(H)
	P = H.flatten(0)'''


	return P


def main():

	'''____________________. G
		                    |
		                    |
		                    |
		                    |
		                    |
	  E .___________________. F
		|                   |
		|                   |
		|                   |
		|        A .________. C
		|          |        |
		|          |        |
		|          |        | origem
		|          |        .___
		|          |        |  |
		|          |        |  |
		|          |        |  |
		|          |        |  |
		|          |        |__|
		|          |        |
		|          |        |
		|          |        |
		|        B .________|
		|                   |
		|                   |
		|                   |
	  D .___________________|
		                    |
		                    |
		                    |
		                    |
		                    |
		____________________|
	'''


	pixelCoords =  [[474, 100],	# A - PeqArea SupDir
					[509, 179],	# B - PeqArea SupEsq
					[577, 100],	# C - PeqArea InfDir
					[266, 238],	# D - GraArea SupEsq 
					[268,  63],	# E - GraArea SupDir
					[550,  63],	# F - GraArea InfDir
					[525,  24]]	# G - Campo   InfDir
	
	#Origem na trave direita, X paralelo à linha de fundo e Y paralelo à lateral
	worldCoords =  [[   5.5,  5.5],	# A - PeqArea SupDir
					[-12.32,  5.5],	# B - PeqArea SupEsq
					[   5.5,    0],	# C - PeqArea InfDir
					[-23.82, 16.5],	# D - GraArea SupEsq
					[  16.5, 16.5],	# E - GraArea SupDir
					[  16.5,    0],	# F - GraArea InfDir 
					[ 30.34,    0]]	# G - Campo   InfDir 
	
	""" Camera Resectioning - Finding the Camera Matrix P """
	'''P = dlt(pixelCoords, worldCoords)
	
	if P is None:
		return
 
	# 2D -> 2D projection (Z=0)
	P_2D = np.append(P[:,:2], P[:,3:], axis=1) # Elimination of column 3
	P_2D_Inv = np.linalg.inv(P_2D)
	'''

	P, _ = DLT.DLTcalib(2, worldCoords, pixelCoords)
	Pmatrix =[[P[0], P[1], P[2]], [P[3], P[4], P[5]], [P[6], P[7], P[8]]]
	#for i in Pmatrix: print(i)

	#P1 = dlt(pixelCoords, worldCoords)
	#print(P1)

	""" Ex2 """
	origImg = cv2.imread('maracana2.jpg')
	img = origImg.copy()
	cv2.namedWindow('image', flags=cv2.WINDOW_GUI_NORMAL)    # hides status, toolbar etc.
	cv2.resizeWindow('image', img.shape[1], img.shape[0])
	cv2.setMouseCallback('image', mouse_callback, (img,origImg))

	while window_is_open('image'):
		cv2.imshow('image',img)


		global clicked

		if clicked:

			#print('\n\n\n\n\n\n')

			cx, cy = DLT.DLTrecon(2, 1, P, (cursorX, cursorY, 1))
			#print(cx,cy)

			point1 = np.dot(Pmatrix, np.array([[30.34], [cy], [1]]))
			point1 = point1 / point1[2]
			#print(point1)
			
			point2 = np.dot(Pmatrix, np.array([[-37.66], [cy], [1]]))
			point2 = point2 / point2[2] 
			#print(point2)

			img = origImg.copy()
			cv2.line(img, (point1[0],point1[1]), (point2[0],point2[1]),(0,0,255),2,cv2.LINE_AA)

			clicked = False

		if cv2.waitKey(20) == 27:
			break
	cv2.destroyAllWindows()


if __name__ == "__main__":
	main()