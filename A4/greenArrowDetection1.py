import numpy as np
import cv2
import imutils

debug = False

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
        img_blur = cv2.blur(np.float32(img), (5, 5))
        mask = self.colorMask(img)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if debug: print(len(contours))
        # print(contours)
        if len(contours) != 0:  # there is a contour
            index = 0
            contours.sort(key = lambda contour : len(contour)) 
            # increase epsilon until less than or only 7 vertices left 
            ep = 0
            corn_list = cv2.approxPolyDP(contours[index], ep, closed=True)
            while len(corn_list) > 7:
                ep += 1
                corn_list = cv2.approxPolyDP(contours[index], ep, closed=True)
            
            if len(corn_list) == 7: # if only 7 corners detected
                
                if debug: print(corn_list.shape)
                corn_list = np.squeeze(corn_list).T
                corn_mean = np.mean(corn_list, axis=1).reshape((2,1))
                corn_cov = np.cov(corn_list)
                eigen_value, eigen_vector = np.linalg.eig(corn_cov)
                p1, p2 = eigen_vector.T[np.argmax(eigen_value)], eigen_vector.T[(np.argmax(eigen_value)+1)%2]

                corn_normlized = corn_list - corn_mean  # corn coordinate in cordinate system from corner center 
                k = p2.reshape((2, 1))[::-1]    # slope vector
                k[1, 0] = -k[1, 0]
                side = np.dot(k.T, corn_normlized)
                
                if debug:
                    print('mean', corn_mean)
                    print('cov', corn_cov)
                    print('p1', p1, 'p2', p2)
                    print('k', k)
                    print('side', side)
                    print('side > 0', np.sum(side> 0))
                    print('side < 0', np.sum(side<= 0))
                
                # based on first principla compound and side value, conclude arrow direction
                if abs(p1[0]) < abs(p1[1]):  # up or down 
                    if np.sum(side > 0) < np.sum(side < 0): # most corner at right of second compound
                        return 'up'
                    else:
                        return 'down'
                else:   # left or right 
                    if np.sum(side > 0) < np.sum(side < 0): # most corner at right of second compound
                        return 'left'
                    else:
                        return 'right'
        return '0'

    def direction(dst):
        corners =  np.where(dst) 

#file_name = 'greenArrowRight.jpg'
#track = tracking()
# for file_name in ['greenArrowLeft.jpg', 'greenArrowRight.jpg' 'greenArrowUp.jpg', 'greenArrowDown.jpg']:
#img = cv2.imread(file_name)
    
#dir = track.showTracking(img)
#print(dir)
