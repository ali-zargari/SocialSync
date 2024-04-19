# Facial Emotion Recognition

This script detects human faces in real-time using a webcam feed and classifies their emotional state into one of four categories: Angry, Happy, Sad, or Surprise.

**For the smoothest experience, use PyCharm as your IDE.**


## Prerequisites

Before running the script, you must have the following installed:

- Python 3.6 or higher
- OpenCV library (cv2)
- TensorFlow


## Installation

1. **Install Python**: Download Python from the official [Python website](https://www.python.org/downloads/) and install it on your system.

2. **OPTIONAL: Set up a Virtual Environment** (**You Can Skip This Step**):
   
   Open a terminal and navigate to your project directory. Then run:
   ```sh
   python -m venv venv
   ```
   Activate the virtual environment:

   - On Windows:
     ```sh
     .\venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```sh
     source venv/bin/activate
     ```

3. **Install Dependencies**:

   Install the required Python packages using pip:
   ```sh
   pip install opencv-python tensorflow
   ```

   Note: TensorFlow might require a specific version depending on the system and Python version. Visit the [TensorFlow installation guide](https://www.tensorflow.org/install) for detailed instructions.


4. **Haar Cascade File**:

   Ensure the `haarcascade_frontalface_default.xml` file is present in the same directory as your script or update the script with its path.


5. **Model File**:

   Place the pre-trained model file `model.h5` in the same directory as the script.

## Running the Script

With all dependencies installed and the virtual environment activated, you can run the script as follows:
```sh
python FaceRecognition.py
```

## Exiting the Program

To exit the live video feed, focus on the video window and press the 'q' key on your keyboard.
