import os
import cv2
import tensorflow as tf


# Get the directory of the current script
script_dir = os.path.dirname(__file__)

# Construct the absolute path to the Haar Cascade file
cascade_path = os.path.join(script_dir, '..', 'ml', 'haarcascade_frontalface_default.xml')

# Load the cascade
cascade = cv2.CascadeClassifier(cascade_path)

# Check if the cascade was loaded correctly
if cascade.empty():
    raise IOError(f"Failed to load Haar Cascade from {cascade_path}")

# for some reason this path here has to be absolute.
model = tf.keras.models.load_model("/Users/joshuamedina/PycharmProjects/SocialSync/backend/ml/model.h5")


def detect_emotion(frame_p):
    emotion = list(model.predict(tf.expand_dims(frame_p, axis=0)))
    num = max(emotion[0])
    idx = list(emotion[0]).index(num)

    return idx, num


def preprocess(frame_p):
    frame_p = cv2.cvtColor(frame_p, cv2.COLOR_BGR2RGB)
    frame_p = cv2.resize(frame_p, (48, 48))
    frame_p = frame_p / 255.

    return frame_p


def detect_face(frame_p):
    cascade = cv2.CascadeClassifier("/Users/joshuamedina/PycharmProjects/SocialSync/backend/ml/haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(frame_p, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, 1.1, 4)

    return gray, faces,


