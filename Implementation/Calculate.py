import json
from PIL import Image
import numpy as np
from scipy.optimize import fsolve

def find_position(JSON):
    #gets image size
    image = Image.open(JSON["Image"])
    imageSize=image.size

    #runway image points
    L0= JSON['Results']['L0']
    R0= JSON['Results']['R0']
    L1= JSON['Results']['L1']
    R1= JSON['Results']['R1']
    imagePts=[R1,R0,L0,L1]
    
     #runway real world coordinates
    #dimensoes da pista
    Wid=JSON['Runway']["Width"]
    Len=JSON['Runway']["Length"]
    #real world coordinates of the edges of the runway
    posA=[Wid,Len,0]
    posB= [Wid,0,0]
    posC= [0,0,0]
    posD= [0,Len,0]

    runwayPoints=[posA,posB,posC,posD]
    #calibracao com https://www.learnopencv.com/camera-calibration-using-opencv/
    import cv2
    objectsPoints=np.array([runwayPoints], dtype='float32')
    imagesPoints=np.array([imagePts],dtype='float32')
    #finds the tranlation and rotation matrix for image points and real world coordinates
    retval, cameraMatrix, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(objectsPoints, imagesPoints, imageSize, None, None)
    rvecs=rvecs[0]
    tvecs=tvecs[0]
    
    #rotation matrix from vector
    R_mtx, jac = cv2.Rodrigues(rvecs)
    #calculates the position of (0,0,0) which is the camera
    #in real world coordinates
    cameraPosition = -R_mtx.T * np.matrix(tvecs)
    #np.array(cameraPosition).T[0]
    #JSON['Results']['Plane_pos']=cameraPosition
    JSON['Results']['Plane_pos']=np.array(cameraPosition).T[0].tolist()
    return JSON
