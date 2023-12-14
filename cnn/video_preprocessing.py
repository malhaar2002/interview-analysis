import cv2
import os
import numpy as np

# Load the pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Define a function to extract frames from a video at regular intervals
def extract_frames(video_path, output_dir, frame_interval=3):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_interval == 0:
            # grayscale conversion
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            # check for number of faces detected
            if len(faces) == 0:
                continue
            elif len(faces) == 1:
                (x, y, w, h) = faces[0]
            else:
                # keep the largest face
                (x, y, w, h) = max(faces, key=lambda rectangle: (rectangle[2] * rectangle[3]))
            face = frame[y:y+h, x:x+w]
            # resize face
            face = cv2.resize(face, (224, 224))
            frames.append(face)
        frame_count += 1
    cap.release()
    cv2.destroyAllWindows()
    # join the frames to create a collage
    collage = np.hstack(frames)
    image_filename = f"{video_path.split('/')[-1][:-4]}.bmp"
    output_path = os.path.join(output_dir, image_filename)
    cv2.imwrite(output_path, collage)


# loop through all videos in the directory 'videos'
input_dir = r'D:\MLPR\interview-analysis\data\P_last'
for video_file in os.listdir(input_dir):
    video_path = os.path.join(input_dir, video_file)
    print(f"Extracting frames from {video_path}...")
    output_dir = r'D:\MLPR\interview-analysis\frames_collage_2'
    extract_frames(video_path, output_dir)