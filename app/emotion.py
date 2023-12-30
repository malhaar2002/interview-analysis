import cv2
from fer import Video
from fer import FER
import pandas as pd

def extract_emotions(video_path):
    # Load the video
    cap = cv2.VideoCapture(video_path)
    
    # Initialize the FER detector
    detector = FER(mtcnn=True)

    # Create a DataFrame to store emotion values
    columns = ["angry", "fear", "happy", "sad", "surprise", "neutral"]
    df = pd.DataFrame(columns=columns)

    # Process each frame
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps)  # Extract one frame per second
    frame_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if frame_count % frame_interval == 0:
            # Detect emotions in the frame
            emotions = detector.detect_emotions(frame)
            
            # If faces are found, add emotions to the DataFrame
            if emotions:
                emotion_values = emotions[0]["emotions"]
                df = pd.concat([df, pd.DataFrame([emotion_values], columns=columns)], ignore_index=True)
            else:
                # If no faces are found, add NaN values
                df = pd.concat([df, pd.DataFrame({col: [None] for col in columns})], ignore_index=True)
        frame_count += 1

    # Calculate the average emotion values
    avg_emotions = df.mean()

    cap.release()

    return avg_emotions
