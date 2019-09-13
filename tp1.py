import cv2
import numpy as np


""" Pixel Coordinates: """

# PeqArea SupDir 473,99
pc1 = [99, 473]
# PeqArea SupEsq 508,177
pc2 = [177, 508]
# PeqArea InfDir 577,99
pc3 = [99, 577] 
# GraArea SupEsq 265,237
pc4 = [237, 265]
# GraArea SupDir 267,61
pc5 = [61, 267]
# GraArea InfDir 551,61
pc6 = [61, 551]
# Campo   InfDir 525,23
pc7 = [23, 525]

pixelCoords = [pc1, pc2, pc3, pc4, pc5, pc6, pc7]


""" World Coordinates: """
#Origem na trave direita, X paralelo à linha de fundo e Y paralelo à lateral
# wc = [x, y, x, w]

# PeqArea SupDir
wc1 = [0, 5.5, 0, 1] 
# PeqArea SupEsq
wc2 = [-18.32, 5.5, 0, 1] 
# PeqArea InfDir 
wc3 = [0, 0, 0, 1]
# GraArea SupEsq
wc4 = [-29.32, 16.5, 0, 1] 
# GraArea InfDir 
wc5 = [11, 0, 0, 1]
# GraArea SupDir 
wc6 = [11, 16.5, 0, 1]
# Campo   InfDir 
wc7 = [24.84, 0, 0, 1]

worldCoords = [wc1, wc2, wc3, wc4, wc5, wc6, wc7]


if len(pixelCoords) != len(worldCoords):
    print("Erro: Quantidade diferente de pontos.")
else:	
    numPoints = len(worldCoords)


""" Camera Resectioning - Finding the Camera Matrix P """  

A = []

for i in range(numPoints): 
    x, y, z, w = worldCoords[i][0], worldCoords[i][1], worldCoords[i][2], worldCoords[i][3] 
    u, v = pixelCoords[i][0], pixelCoords[i][1]
    A.append([x, y, z, w, 0, 0, 0, 0, -u*x, -u*y, -u*z, -u])
    A.append([0, 0, 0, 0, x, y, z, w, -v*x, -v*y, -v*z, -v])

U, S, Vh = np.linalg.svd(A)

P = Vh[-1,:] # P receives the last line of Vh
P = P.reshape(3,4)



