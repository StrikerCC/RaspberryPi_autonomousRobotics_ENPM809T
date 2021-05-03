import cv2
import os

command = 'sudo modprobe bcm2835-v4l2'
os.system(command)

# open video capture
cap = cv2.VideoCapture(0)

# define detector
detector = cv2.QRCodeDetector()

while True:
    check, img = cap.read()
    img = cv2.flip(img, -1)
    data, bbox, _ = detector.detectAndDecode(img)

    if bbox is not None:
        for i in range(len(bbox)):
            cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(0, 0, 255), thickness=4)
    
    if data is not None:
        print("Data: ", data)

    # show frame
    cv2.imshow("QR code detector", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

