import cv2

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Không mở được webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Không lấy được frame.")
        break

    cv2.imshow("Test", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
