import cv2
import numpy as np

clicked = False
right_clicked = False
cursorX = 0
cursorY = 0


def mouse_callback(event,x,y,flags,param):
	if event == cv2.EVENT_FLAG_LBUTTON:
		global clicked, cursorX, cursorY
		clicked = True
		cursorX = x
		cursorY = y
	elif event == cv2.EVENT_FLAG_RBUTTON:
		global right_clicked
		right_clicked = True
		
def window_is_open(windowname):
	return True if cv2.getWindowProperty(windowname, cv2.WND_PROP_VISIBLE) >= 1 else False

#Direct Linear Transformation
def dlt(pixelCoords, worldCoords, dim):
	if len(pixelCoords) != len(worldCoords):
		print("Erro: Quantidade diferente de pontos.")
		return None
	else:    
		numPoints = len(worldCoords)

	A = []

	# 2D DLT
	if dim is 2:
		for i in range(numPoints): 
			x, y, w = worldCoords[i][0], worldCoords[i][1], 1
			u, v = pixelCoords[i][0], pixelCoords[i][1]
			A.append([x, y, w, 0, 0, 0, -u*x, -u*y, -u])
			A.append([0, 0, 0, x, y, w, -v*x, -v*y, -v])
	# 3D DLT
	elif dim is 3:
		for i in range(numPoints): 
			x, y, z, w = worldCoords[i][0], worldCoords[i][1], worldCoords[i][2], 1
			u, v = pixelCoords[i][0], pixelCoords[i][1]
			A.append([x, y, z, w, 0, 0, 0, 0, -u*x, -u*y, -u*z, -u])
			A.append([0, 0, 0, 0, x, y, z, w, -v*x, -v*y, -v*z, -v])
		
	_, _, Vh = np.linalg.svd(A)

	P = Vh[-1,:]	# The parameters are in the last line of Vh 
	P = P.reshape(3,dim+1)
	
	return P


def ex1():

	'''
					   I_______________
					  /
					 /
					/___________
				   /			/
			   C  G_____E      /
			  /| /     /      /
			D/ |/     /      /
			|  A     /      /
			| /     /      /
			B/     /      /
			/     /      /
		   H_____F      /
		  /            /
		 /____________/
		/

	'''

	pixelCoords =  [[319, 277], # A
					[247, 313], # B
					[318, 220], # C
					[245, 253], # D
					[482, 261], # E
					[320, 351], # F
					[368, 253], # G
					[191, 342], # H
					[545, 166]] # I
					
	
	worldCoords =  [[     0,  105,    0],   # A
					[ -7.32,  105,    0],   # B
					[     0,  105, 2.44],   # C
					[ -7.32,  105, 2.44],   # D
					[   5.5, 99.5,    0],   # E
					[-12.32, 99.5,    0],   # F 
					[   5.5,  105,    0],   # G 
					[-12.32,  105,    0],   # H 
					[ 30.34,  105,    0]]   # I 
	
	P = dlt(pixelCoords, worldCoords, 3)

	origImg = cv2.imread('maracana1.jpg')
	origImg = cv2.resize(origImg, None, fx=2, fy=2)
	img = origImg.copy()
	cv2.namedWindow('EX1', flags=cv2.WINDOW_GUI_NORMAL)    # hides status, toolbar etc.
	cv2.resizeWindow('EX1', img.shape[1], img.shape[0])
	cv2.setMouseCallback('EX1', mouse_callback)

	while window_is_open('EX1'):
		cv2.imshow('EX1',img)

		global clicked, right_clicked

		if clicked:

			Ptemp = np.hstack((P[:,:2],P[:,3:]))			# ignores third column (Z)
			Pinv = np.linalg.inv(Ptemp)						# to calculate inverse matrix
			
			# Cursor position in world coordinates: P^(-1) * [cursorX, cursorY, 0, 1]
			xyz = np.dot( Pinv,[[cursorX],[cursorY],[1]] ) 
			(cx, cy) = xyz[0:2]/xyz[2]

			# Player head position in pixel coordinates: P * [cx, cy, 1.80, 1]
			point = np.dot(P, np.array([[cx], [cy], [1.80], [1]]))
			point = point / point[2]
			
			img = origImg.copy()
			cv2.line(img, (cursorX, cursorY),(point[0],point[1]), (255,0,0),2,cv2.LINE_AA)

			clicked = False

		if right_clicked:

			img = origImg.copy()

			j = "A"
			for i in pixelCoords:
				cv2.circle(img,(i[0],i[1]),5,(0,0,255),-1)
				cv2.putText(img, j, (i[0]+10,i[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2, cv2.LINE_AA)
				j = chr(ord(j[0])+1)	# j = next char

			right_clicked = False

		if cv2.waitKey(20) == 27:
			break
	cv2.destroyAllWindows()


def ex2():

	'''________________
					   G
					   |
					   |
		 ______________F
		E              |
		|              |
		|        ______|
		|       A      C
		|       |      |___
		|       |      |  |
		|       |      |  |
		|       |      |__|
		|       |      |
		|       B______|
		|              |
		|              |
		D______________|
					   |
					   |
					   |
		_______________|
	'''

	pixelCoords =  [[474, 100], # A - PeqArea SupDir
					[509, 179], # B - PeqArea SupEsq
					[577, 100], # C - PeqArea InfDir
					[266, 238], # D - GraArea SupEsq 
					[268,  63], # E - GraArea SupDir
					[550,  63], # F - GraArea InfDir
					[525,  24]] # G - Campo   InfDir
	
	#Origem na trave direita, X paralelo à linha de fundo e Y paralelo à lateral
	worldCoords =  [[   5.5,  5.5], # A - PeqArea SupDir
					[-12.32,  5.5], # B - PeqArea SupEsq
					[   5.5,    0], # C - PeqArea InfDir
					[-23.82, 16.5], # D - GraArea SupEsq
					[  16.5, 16.5], # E - GraArea SupDir
					[  16.5,    0], # F - GraArea InfDir 
					[ 30.34,    0]] # G - Campo   InfDir 
	
	P = dlt(pixelCoords, worldCoords, 2)

	origImg = cv2.imread('maracana2.jpg')
	img = origImg.copy()
	cv2.namedWindow('EX2', flags=cv2.WINDOW_GUI_NORMAL)    # hides status, toolbar etc.
	cv2.resizeWindow('EX2', img.shape[1], img.shape[0])
	cv2.setMouseCallback('EX2', mouse_callback)

	while window_is_open('EX2'):
		cv2.imshow('EX2',img)

		global clicked, right_clicked

		if clicked:

			Pinv = np.linalg.inv(P)
			
			# Cursor position in world coordinates: P^(-1) * [cursorX, cursorY, 1]
			xyz = np.dot( Pinv,[cursorX,cursorY,1] ) 
			(cx, cy) = xyz[0:2]/xyz[2]

			# First point (on the right touchline) in pixel coordinates: P * [30.34, cy, 1]
			point1 = np.dot(P, np.array([[30.34], [cy], [1]]))
			point1 = point1 / point1[2]
			
			# Second point (on the left touchline) in pixel coordinates: P * [-37.66, cy, 1]
			point2 = np.dot(P, np.array([[-37.66], [cy], [1]]))
			point2 = point2 / point2[2] 

			img = origImg.copy()
			cv2.line(img, (point1[0],point1[1]), (point2[0],point2[1]),(0,0,255),2,cv2.LINE_AA)

			clicked = False

		if right_clicked:

			img = origImg.copy()
			
			j = "A"
			for i in pixelCoords:
				cv2.circle(img,(i[0],i[1]),5,(0,0,255),-1)
				cv2.putText(img, j, (i[0]-20,i[1]+10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2, cv2.LINE_AA)
				j = chr(ord(j[0])+1)	# j = next char

			right_clicked = False

		if cv2.waitKey(20) == 27:
			break
	cv2.destroyAllWindows()


if __name__ == "__main__":
	#ex1()
	ex2()