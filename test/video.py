import cv2

cv2.namedWindow("preview")
cap = cv2.VideoCapture(1)

rval, frame = cap.read()

while True:
    if frame is not None:
        cv2.imshow("preview", frame)
    rval, frame = cap.read()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()