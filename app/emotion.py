import cv2
from fer import Video
from fer import FER

def get_emotions(VIDEO_FILE):
    video = Video(VIDEO_FILE)

    # Analyze video, displaying the output
    detector = FER(mtcnn=True)
    raw_data = video.analyze(detector, display=True)
    df = video.to_pandas(raw_data)
    return df