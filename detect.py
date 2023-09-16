import cv2

# Load the pre-trained HOG people detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Open a video capture object for webcam
cap = cv2.VideoCapture(0)  # 0 indicates the default webcam

while True:
    ret, frame = cap.read()  # Read a frame from the webcam

    if not ret:
        break

    # Convert the frame to grayscale for processing
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect people in the frame
    rectangles, weights = hog.detectMultiScale(gray_frame, winStride=(8, 8), padding=(4, 4), scale=1.05)

    # Draw rectangles around detected people
    for (x, y, w, h) in rectangles:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the frame with detected people
    cv2.imshow("Person Detection", frame)

    # Exit the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the windows
cap.release()
cv2.destroyAllWindows()
