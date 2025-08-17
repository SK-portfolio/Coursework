import cv2
import time
import mediapipe as mp

# Prepare video capture.
# 0 to take the video frames from the camera device
# (0)->FrontCam, (1)->BackCam, ("___.mp4")->VideoFile
cap = cv2.VideoCapture('input.mp4')
currentTime = 0
previousTime = 0

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

drawingSpec = mp_drawing.DrawingSpec(
	color=(255, 255, 255),
	thickness=1,
	circle_radius=3
)

face_mesh = mp_face_mesh.FaceMesh(
	max_num_faces=3,
	refine_landmarks=True,
	min_detection_confidence=0.5,
	min_tracking_confidence=0.5
)

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*"MJPG")
out = cv2.VideoWriter("output.avi", fourcc, 30.0, (frame_width, frame_height))

# As long as device is ready
while cap.isOpened():
	# Read the video frame
	success, image = cap.read()
	results = face_mesh.process(image)

	if not success:
		continue

	if results.multi_face_landmarks:
		for face_landmarks in results.multi_face_landmarks:
			mp_drawing.draw_landmarks(
				image=image,
				landmark_list=face_landmarks,
				connections=mp_face_mesh.FACEMESH_TESSELATION,
				landmark_drawing_spec=drawingSpec,
				connection_drawing_spec=drawingSpec
			)
	
	# Flip the image for a front-facing webcam view
	#image = cv2.flip(image, 1)
	
	# Resizing the frame
	aspect_ratio = image.shape[1] / image.shape[0]
	image = cv2.resize(image, (frame_width, frame_height))
	out.write(image)

	# Calculating the FPS
	currentTime = time.time()
	fps = 1 / (currentTime - previousTime)
	previousTime = currentTime

	# Displaying FPS on the image
	cv2.putText(image, str(int(fps))+" FPS", (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

	# Display
	#cv2.imshow('OpenCV camera', image)
	cv2.imshow('video', image)
	if cv2.waitKey(5) & 0xFF == 27:
		break

# Clean up after the loop
cap.release()
out.release()
cv2.destroyAllWindows()