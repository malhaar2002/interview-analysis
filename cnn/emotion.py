import os
import cv2
import pandas as pd
from fer import FER

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


def process_videos(directory_path):
    # Create an empty DataFrame for storing results
    result_df = pd.DataFrame(columns=["InterviewID", "angry", "fear", "happy", "sad", "surprise", "neutral"])

    # Process each video in the directory
    for video_file in os.listdir(directory_path):
        print("Processing", video_file)
        video_path = os.path.join(directory_path, video_file)
        avg_emotions = extract_emotions(video_path)

        # Append results to the DataFrame
        interview_id = video_file.split(".")[0]
        result_df = pd.concat([result_df, pd.DataFrame([{"InterviewID": interview_id, **avg_emotions}])], ignore_index=True)

        # Save the results to a CSV file
        result_df.to_csv("../pp_data/emotions.csv", index=False)


# Replace 'your_video_directory' with the path to your directory containing videos
video_directory = '../data/Videos'
process_videos(video_directory)
