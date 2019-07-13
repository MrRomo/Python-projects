import time
import cv2
import numpy as np
import math

#Import an image to map:
import matplotlib.image as mpimg
cap = cv2.VideoCapture(0) 
  
# loop runs if capturing has been initialized. 
while 1:  
  
    # reads frames from a camera 
    ret, img = cap.read() 
    frame_size = img.shape[0]*img.shape[1]
    imgRight = img[:,img.shape[1]/2:]
    inputBounds = np.array([0, 2, -2, 2])
    inputResolution = imgRight.shape
    # figure(0, (6,6))

    outputBounds = 6.5*np.array([-1,1,-1,1])
    outputResolution = [1200,1200]
    #Create x and y sampling vectors
    xInput=np.linspace(inputBounds[0], inputBounds[1], inputResolution[1])
    yInput=np.linspace(inputBounds[2], inputBounds[3], inputResolution[0])
    #Put sampling vectors on 2d grid:
    x,y=np.meshgrid(xInput,yInput)
    z=x+1j*y
    w = z**2
    reSlope = float(outputResolution[1])/(outputBounds[1]-outputBounds[0])
    imSlope = float(outputResolution[0])/(outputBounds[3]-outputBounds[2])

    reIndex = (w.real*reSlope + outputResolution[1]/2).round().astype('int')
    imIndex = (w.imag*imSlope + outputResolution[0]/2).round().astype('int')

    outputImageSize = outputResolution[:]
    outputImageSize.append(3)

    mappedImage = np.empty(outputImageSize)
    # mappedImage[:] = NULL
    whiteThresh = 200
    startTime = time.time()

    for i in range(inputResolution[0]):
        for j in range(inputResolution[1]):
            #Only map pixels in the output range:
            if reIndex[i, j] > 0 and reIndex[i, j] < outputResolution[1]:
                if imIndex[i,j] > 0 and imIndex[i,j] < outputResolution[0]:
                    #Check if that pixel has been filled yet: 
                    if isnan(mappedImage[imIndex[i,j], reIndex[i,j], 0]):
                        mappedImage[imIndex[i,j], reIndex[i,j], :] =  imgRight[i, j, :]
                    #Check if non-white:
                    elif imgRight[i, j, 0]< whiteThresh or imgRight[i, j, 1]< whiteThresh or \
                        imgRight[i, j, 2:]< whiteThresh:
                        mappedImage[imIndex[i,j], reIndex[i,j], :] =  imgRight[i, j, :] 
                        
    print 'Time Elapsed = ' + str(time.time()-startTime) + 's.'

    cv2.imshow('img',imgRight) 
  
    # Wait for Esc key to stop 
    k = cv2.waitKey(30) & 0xff
    if k == 27: 
        break
  
# Close the window 
cap.release() 
  
# De-allocate any associated memory usage 
cv2.destroyAllWindows()