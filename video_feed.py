import cv2
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import time

class_names = ["Angry", "Happy", "Sad", "Surprise"]
model = tf.keras.models.load_model("model.h5")  # Move model loading outside the loop to optimize



def detect_emotion(frame_p):
    emotion = list(model.predict(tf.expand_dims(frame_p, axis=0)))
    num = max(emotion[0])
    idx = list(emotion[0]).index(num)

    fig, ax = plt.subplots()  # Create a figure and an axis.
    ax.imshow(frame_p)  # Plot image.
    ax.text(5, 5, str(idx), bbox=dict(fill=False, edgecolor='red', linewidth=2))
    fig.canvas.draw()  # Draw the figure so you can find the renderer.

    # Save the figure to a file.
    frame = np.array(fig.canvas.renderer.buffer_rgba())
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)

    # Timestamped filename.
    timestamp = int(time.time())
    frame_name = f'dataset/classified_frame_{timestamp}.jpeg'
    cv2.imwrite(frame_name, frame_bgr)

    return idx, num



def preprocess(frame_p):
    frame_p = cv2.cvtColor(frame_p, cv2.COLOR_BGR2RGB)
    frame_p = cv2.resize(frame_p, (48, 48))
    frame_p = frame_p / 255.0

    return frame_p


def detect_face(frame_p):
    cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame_p, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, 1.1, 4)

    return gray, faces



video_path = 'test.mp4'
video = cv2.VideoCapture(video_path)


while True:
    ret, frame = video.read()

    if ret:  # Check if frame is successfully captured
        gray, faces = detect_face(frame)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face_roi_gray = gray[y:y + h, x:x + w]  # Region Of Interest (face area)
            face_roi_gray = preprocess(face_roi_gray)
            idx, conf = detect_emotion(face_roi_gray)

            class_name = class_names[idx]

            if conf > 0.3:  # Only show predictions with confidence greater than 0.3
                cv2.putText(frame, class_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Window", frame)

    else:
        break  # Exit the loop if there are no more frames to read

    # Press 'q' to quit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
