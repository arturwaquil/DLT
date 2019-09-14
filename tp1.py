import cv2
import numpy as np

clicked = False
cursorX = 0
cursorY = 0

# Variáveis usadas para normalização: menores e maiores valores possíveis para as coordenadas do mundo
minWorldX = -43.16
maxWorldX = 24.84
minWorldY = 0
maxWorldY = 105
minWorldZ = 0
maxWorldZ = 2.44 #Altura goleira

def mouse_callback(event,x,y,flags,param):
    if event == cv2.EVENT_FLAG_LBUTTON:
        clicked = True
        global cursorX, cursorY
        cursorX = x
        cursorY = y        
        
def window_is_open(windowname):
    return True if cv2.getWindowProperty(windowname, cv2.WND_PROP_VISIBLE) >= 1 else False
    
def normalize(value, min, max):
    return (value-min)/(max-min)

#Direct Linear Transformation
def dlt(pixelCoords, worldCoords, maxPixelU, maxPixelV):
    if len(pixelCoords) != len(worldCoords):
        print("Erro: Quantidade diferente de pontos.")
        return []
    else:    
        numPoints = len(worldCoords)

    A = []

    for i in range(numPoints): 
        x, y, z, w = worldCoords[i][0], worldCoords[i][1], worldCoords[i][2], worldCoords[i][3] 
        u, v = pixelCoords[i][0], pixelCoords[i][1]
        x, y, z = normalize(x, minWorldX, maxWorldX), normalize(y, minWorldY, maxWorldY), normalize(z, minWorldZ, maxWorldZ)
        u, v = normalize(u, 0, maxPixelU), normalize(v, 0, maxPixelV)
        A.append([x, y, z, w, 0, 0, 0, 0, -u*x, -u*y, -u*z, -u])
        A.append([0, 0, 0, 0, x, y, z, w, -v*x, -v*y, -v*z, -v])
    
    U, S, Vh = np.linalg.svd(A)

    P = Vh[-1,:] # P receives the last line of Vh
    P = P.reshape(3,4)
    return P


def main():    
    """ Maracana2 - Pixel Coordinates: """

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
    
    
    """ Maracana2 - World Coordinates: """
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
    # GraArea SupDir 
    wc5 = [11, 16.5, 0, 1]
    # GraArea InfDir 
    wc6 = [11, 0, 0, 1]
    # Campo   InfDir 
    wc7 = [24.84, 0, 0, 1]
    
    worldCoords = [wc1, wc2, wc3, wc4, wc5, wc6, wc7]

    
    """ Camera Resectioning - Finding the Camera Matrix P """
    originalImg = cv2.imread('maracana2.jpg')
    
    P = dlt(pixelCoords, worldCoords, originalImg.shape[0]-1, originalImg.shape[1]-1)
    
    if P == []:
        return
 
    # 2D -> 2D projection (Z=0)
    P_2D = np.append(P[:,:2], P[:,3:], axis=1) # Elimination of column 3
    P_2D_Inv = np.linalg.inv(P_2D)
    
        
    """ Ex2 """
    img = originalImg
    cv2.namedWindow('image', flags=cv2.WINDOW_GUI_NORMAL)    # hides status, toolbar etc.
    cv2.resizeWindow('image', img.shape[1], img.shape[0])
    cv2.setMouseCallback('image', mouse_callback)

    while window_is_open('image'):
        cv2.imshow('image',img)
        #if clicked:
            # IMPLEMENTAR AQUI IDENTIFICACAO E PRINT DA LINHA
            

        if cv2.waitKey(20) == 27:
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()