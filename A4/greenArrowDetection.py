import numpy as np
import cv2
import imutils

class tracking:
    def __init__(self):
        print("tracker ready")

    def colorMask(self, img):
        assert img.shape[0] != 0 and img.shape[1] != 0, "img cannot be empty" 
        img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        #cv2.imshow('HSV', img_HSV)
        #cv2.waitKey(0)

        ### hsv filter for green 
        low_h, low_s, low_v = (52, 74, 205)
        high_h, high_s, high_v = (82, 187, 255)

        img_thresh = cv2.inRange(img_HSV, (low_h, low_s, low_v), (high_h, high_s, high_v))
        # cv2.imshow('mask', img_thresh)
        # cv2.waitKey(0)
        
        return img_thresh

    def showTracking(self, img):
        # frame = cv2.flip(img, 0)
        
        mask = self.colorMask(img)

        img_blur = cv2.blur(np.float32(mask), (5, 5))
        # img_blur = cv2.bilateralFilterblur(img_thresh,20, 75, 75))
        
        dst = cv2.cornerHarris(img_blur, 2, 5, 0.01)
        dst = cv2.dilate(dst, None)
        cord_corn = np.where(dst>0.01*dst.max())
        
        print('# of corner points', len(cord_corn[0]))
        

        # compute the principal components 
        cord_corn = np.array(cord_corn) # list of cordinates of corners 
        cov_matrix = np.cov(cord_corn)  # covariance matrix of corner points 
        mean = np.mean(cord_corn, axis=1)
        eigen_value, eigen_vector = np.linalg.eig(cov_matrix)   # 

        print('covar', cov_matrix)
        print('mean', mean)
        print('v', eigen_value)
        print('u', eigen_vector)
        
        principal_comp_1 = eigen_vector.T[np.argmax(eigen_value)]
        
        principal_comp_2 = eigen_vector.T[(np.argmax(eigen_value)+1)%2]
        print(file_name,1, principal_comp_1)
        print(file_name,2, principal_comp_2)
        
        # comupte direction of arrow
        cord_corn = cord_corn.T - mean # normalize corners 
        
        # print(cord_corn)
        print(np.mean(cord_corn, 0))
        print(cord_corn.shape)
        # print(np.dot(cord_corn, principal_comp_2)) 
        # print(np.sum(np.dot(cord_corn, principal_comp_2)))



        img[dst>0.01*dst.max()] = [0, 0, 255]
        
        #cv2.imshow('mask', img_blur)
        #cv2.waitKey(0)

        # cv2.imshow('corner', dst)
        #cv2.waitKey(0)

         
        #cv2.imshow('img', img)
        #cv2.waitKey(0)

        # cv2.imshow('tracking', frame)
        # cv2.waitKey(0)
        return dst

    def direction(dst):
        corners =  np.where(dst) 

file_name = 'greenArrowDown.jpg'
track = tracking()
# for file_name in ['greenArrowLeft.jpg', 'greenArrowRight.jpg' 'greenArrowUp.jpg', 'greenArrowDown.jpg']:
img = cv2.imread(file_name)
    
track.showTracking(img)
