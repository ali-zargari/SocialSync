import sys
from collections import deque
import time
import cv2
import numpy as np
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
                             QFrame, QSizePolicy, QGraphicsDropShadowEffect, QProgressBar)
from PyQt5.QtGui import QFont, QPixmap, QImage, QColor, QPainter, QLinearGradient
from PyQt5.QtCore import Qt, QPoint, QPropertyAnimation, QTimer, QThread, pyqtSignal
from ui.controllers.emotion_recognition import detect_face, detect_emotion, preprocess, EmotionDetectionWorker
from ui.pyqt.cv_window import VideoWindow
import os

# Tested and working
class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #71B89A;
                color: white;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #5A9A7F;
            }
            QPushButton:pressed {
                background-color: #4A8A6F;
            }
        """)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.shadow.setOffset(0, 5)
        self.setGraphicsEffect(self.shadow)

    def enterEvent(self, event):
        self.animate_shadow(25, 0, 8)

    def leaveEvent(self, event):
        self.animate_shadow(15, 0, 5)

    def animate_shadow(self, end_blur, end_x, end_y):
        self.anim_blur = QPropertyAnimation(self.shadow, b"blurRadius")
        self.anim_blur.setEndValue(end_blur)
        self.anim_blur.setDuration(200)

        self.anim_offset = QPropertyAnimation(self.shadow, b"offset")
        self.anim_offset.setEndValue(QPoint(end_x, end_y))
        self.anim_offset.setDuration(200)

        self.anim_blur.start()
        self.anim_offset.start()


class RoundedFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.2);
            border-radius: 20px;
        """)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 10)
        self.setGraphicsEffect(shadow)


# class RoundedFrame(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setAttribute(Qt.WA_StyledBackground, True)
#
#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.Antialiasing)
#         path = QPainterPath()
#         path.addRoundedRect(0, 0, self.width(), self.height(), 10, 10)
#         painter.fillPath(path, self.palette().window())


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent  # Reference to the main stacked window

        # Initialize attributes before UI setup
        self.current_emotion = "Annoyed"
        self.emotion_start_time = time.time()

        # Initialize camera worker
        self.camera_worker = None
        self.video_thread = None

        # Load emotion descriptions
        self.emotion_descriptions = {
            "Happiness": self.load_description_from_file("u5_Emotion_session_happy.py"),
            "Sad": self.load_description_from_file("u6_Emotion_session_sad.py"),
            "Annoyed": self.load_description_from_file("u8_Emotion_session_annoyed.py"),
            "Upset": self.load_description_from_file("u12_Emotion_session_upset.py")
        }

        # Emotion emoji paths
        self.emotion_emojis = {
            "Happiness": "images/happy.png",
            "Sad": "images/sad.png",
            "Annoyed": "images/annoyed.png",
            "Upset": "images/upset.png"
        }

        self.initUI()

        # Initialize emotion detection worker
        self.worker = EmotionDetectionWorker()
        self.worker.result_signal.connect(self.process_worker_result)
        self.worker.start()

        # Initialize a deque to store the last 100 emotion detections
        self.emotion_history = deque(maxlen=100)

        # Timer for emotion stability check - reduced frequency
        self.emotion_timer = QTimer()
        self.emotion_timer.timeout.connect(self.check_emotion_stability)
        self.emotion_timer.start(2000)  # Check every 2 seconds

    def process_worker_result(self, frame, emotions, confidence):
        try:
            # Define class names if not already defined in worker
            if not hasattr(self.worker, 'class_names'):
                self.worker.class_names = ["Annoyed", "Happiness", "Sad", "Upset"]

            # Update emotion history
            for emotion_label, conf in emotions.items():
                if emotion_label in self.worker.class_names:
                    idx = self.worker.class_names.index(emotion_label)
                    self.emotion_history.append((idx, conf))

            # Update the UI elements directly
            self.update_video_label(frame)
            self.update_emotional_feedback()
            self.update_confidence_label(confidence)
        except Exception as e:
            print(f"Error in process_worker_result: {str(e)}")

    def update_video_label(self, frame):
        try:
            # Resize frame before conversion for better performance
            frame = cv2.resize(frame, (288, 208))
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.video_label.setPixmap(pixmap)
        except Exception as e:
            print(f"Error updating video label: {str(e)}")

    def update_confidence_label(self, confidence):
        confidence_percent = int(confidence * 100)
        self.confidence_label.setText(f"Confidence: {confidence_percent}%")
        # Show/hide face detection message based on confidence
        self.face_detection_label.setVisible(confidence_percent == 0)

    def initUI(self):
        self.setWindowTitle('Emotion Recognition UI')
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #71B89A;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self.createHeader())
        main_layout.addWidget(self.createMainContent())
        main_layout.addWidget(self.createBottomSection())

    def createHeader(self):
        header_container = QWidget(self)
        header_container.setStyleSheet("background-color: white;")
        header_container.setFixedHeight(80)
        header_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 2)
        header_container.setGraphicsEffect(shadow)

        header_inner_layout = QHBoxLayout(header_container)
        header_inner_layout.setContentsMargins(20, 0, 20, 0)
        header_inner_layout.setSpacing(20)

        logo_label = QLabel(self)
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images/v20_308.png")
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        header_inner_layout.addWidget(logo_label, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        header_title = QLabel('Emotion Recognition', self)
        header_title.setFont(QFont('Arial', 28, QFont.Bold))
        header_title.setStyleSheet("color: #71B89A;")
        header_inner_layout.addWidget(header_title, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        header_inner_layout.addStretch()

        for text in ["Profile", "History", "Sign Out"]:
            button = AnimatedButton(text, self)
            button.setFixedSize(120, 50)
            button.clicked.connect(lambda checked, btn=text: self.handle_button_click(btn))
            header_inner_layout.addWidget(button, alignment=Qt.AlignRight | Qt.AlignVCenter)

        return header_container

    def handle_button_click(self, btn_name):
        """ Handle button clicks for Profile, History, and Sign Out """
        if btn_name == "Profile":
            self.main_window.show_profile_setting_gui()
        elif btn_name == "History":
            self.main_window.show_history_page()
        elif btn_name == "Sign Out":
            self.main_window.show_login_page()

    def createMainContent(self):
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(40, 15, 40, 40)  # Reduced top margin to move content up
        content_layout.setSpacing(40)
        content_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)  # Changed from just AlignCenter to include AlignTop

        content_layout.addStretch(1)

        # Create and add the Confidence section (smaller size)
        confidence_section = self.createConfidenceSection()
        confidence_section.setFixedSize(250, 180)
        content_layout.addWidget(confidence_section, alignment=Qt.AlignTop)

        # Create and add the Emotional Feedback section (wider and higher on the page)
        emotional_feedback = self.createEmotionalFeedback()
        emotional_feedback.setFixedSize(500, 300)  # Increased width
        content_layout.addWidget(emotional_feedback, alignment=Qt.AlignTop)

        # Create and add the Video Feed section
        video_feed = self.createVideoFeedSection()
        video_feed.setFixedSize(320, 240)
        content_layout.addWidget(video_feed, alignment=Qt.AlignTop)

        # Add stretch after last component to center everything
        content_layout.addStretch(1)

        return content

    def createEmotionalFeedback(self):
        feedback = RoundedFrame()
        feedback.setFixedSize(500, 300)  # Increased width from 400 to 500

        layout = QVBoxLayout(feedback)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        header = QLabel("Emotional Feedback", feedback)
        header.setStyleSheet("color: white; font-size: 28px; font-weight: bold;")  # Increased from 22px
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Initialize the emotions data structure to update later, including percentage labels
        self.emotions_data = {
            "Annoyed": (QColor(255, 193, 7), QLabel(feedback), QProgressBar(feedback), QLabel("0%", feedback)),
            "Happiness": (QColor(46, 204, 113), QLabel(feedback), QProgressBar(feedback), QLabel("0%", feedback)),
            "Sad": (QColor("#999999"), QLabel(feedback), QProgressBar(feedback), QLabel("0%", feedback)),
            "Upset": (QColor(231, 76, 60), QLabel(feedback), QProgressBar(feedback), QLabel("0%", feedback))
        }

        for emotion, (color, label, progress_bar, percentage_label) in self.emotions_data.items():
            emotion_layout = QHBoxLayout()
            label.setText(emotion)
            label.setStyleSheet("color: white; font-size: 22px; background: transparent;")  # Increased from 18px

            percentage_label.setStyleSheet(
                "color: white; font-size: 22px; font-weight: bold; background: transparent;")  # Increased from 18px

            progress_bar.setRange(0, 100)
            progress_bar.setValue(0)
            progress_bar.setTextVisible(False)
            progress_bar.setFixedHeight(15)  # Increased from 10
            progress_bar.setStyleSheet(f"""
                QProgressBar {{
                    background-color: rgba(255, 255, 255, 0.3);
                    border-radius: 7px;  # Increased from 5px
                }}
                QProgressBar::chunk {{
                    background-color: {color.name()};
                    border-radius: 7px;  # Increased from 5px
                }}
            """)

            emotion_layout.addWidget(label)
            emotion_layout.addWidget(progress_bar)
            emotion_layout.addWidget(percentage_label)

            layout.addLayout(emotion_layout)

        return feedback

    def createConfidenceSection(self):
        section = RoundedFrame()
        section.setFixedSize(298, 298)  # Consistent size for all emotions

        layout = QVBoxLayout(section)
        layout.setContentsMargins(10, 10, 10, 10)  # Standard margins
        layout.setSpacing(10)

        # Initialize a QLabel for confidence display to update later
        self.confidence_label = QLabel("Confidence: 0%", section)
        self.confidence_label.setStyleSheet("font-size: 20px; color: white; font-weight: bold;")  # Reduced font size
        self.confidence_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.confidence_label)

        self.annoyed_face_label = QLabel(section)
        image_path2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images/annoyed.png")
        annoyed_face_pixmap = QPixmap(image_path2).scaled(245, 245, Qt.KeepAspectRatio,
                                                          Qt.SmoothTransformation)  # MODIFIED: Increased emoji size from 120x120 to 160x160
        self.annoyed_face_label.setPixmap(annoyed_face_pixmap)
        self.annoyed_face_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.annoyed_face_label)

        return section

    def update_feedback(self, emotions, confidence):
        # Update each emotion's progress bar and label
        for emotion, (color, label, progress_bar) in self.emotions_data.items():
            if emotion in emotions:
                percentage = emotions[emotion]
                progress_bar.setValue(percentage)
                percentage_label = progress_bar.parent().findChildren(QLabel)[-1]  # Locate percentage label in layout
                percentage_label.setText(f"{percentage}%")

        # Update the confidence label
        self.confidence_label.setText(f"Confidence: {int(confidence * 100)}%")

    def createVideoFeedSection(self):
        section = RoundedFrame()
        section.setFixedSize(320, 280)  # Increased height to accommodate message

        layout = QVBoxLayout(section)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        self.video_label = QLabel(section)
        self.video_label.setFixedSize(288, 208)
        self.video_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.video_label)

        # Add label for face detection message
        self.face_detection_label = QLabel("Please make sure face is in the camera", section)
        self.face_detection_label.setStyleSheet(
            "color: red; font-size: 14px; font-weight: bold; border: 2px solid black; "
            "padding: 4px; border-radius: 5px")
        self.face_detection_label.setAlignment(Qt.AlignCenter)
        self.face_detection_label.setVisible(False)  # Hidden by default
        layout.addWidget(self.face_detection_label)

        return section

    def createBottomSection(self):
        section = QFrame()
        layout = QVBoxLayout(section)
        layout.setContentsMargins(50, 0, 50, 20)
        layout.setSpacing(20)

        explanation = self.createExplanationSection()
        layout.addWidget(explanation)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()

        # Add the existing Help button
        help_button = AnimatedButton('Help', self)
        help_button.setFixedSize(120, 50)
        help_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #39687C;
                border-radius: 25px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        """)
        button_layout.addWidget(help_button)

        # Add stretch to push buttons to opposite sides
        button_layout.addStretch()

        # Add the new End Session button
        end_session_button = AnimatedButton('End Session', self)
        end_session_button.setFixedSize(120, 50)
        end_session_button.setStyleSheet("""
            QPushButton {
                background-color: #FF0000;
                color: white;
                border-radius: 25px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #CC0000;
            }
        """)
        end_session_button.clicked.connect(self.endSession)
        button_layout.addWidget(end_session_button)

        # Add the button layout to the main layout
        layout.addLayout(button_layout)

        return section

    def createExplanationSection(self):
        self.explanation_section = QLabel()
        self.explanation_section.setFixedSize(1180, 240)
        self.explanation_section.setText(self.emotion_descriptions[self.current_emotion])
        self.explanation_section.setWordWrap(True)
        self.explanation_section.setStyleSheet("""
            font-size: 20px;
            color: #333333;
            background-color: #C1F0D1;
            padding: 28px;
            border-radius: 25px;
        """)
        self.explanation_section.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 10)
        self.explanation_section.setGraphicsEffect(shadow)

        return self.explanation_section

    def detect_face(self, frame):
        """Detect faces in the frame using OpenCV"""
        if frame is None:
            return None, []

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        try:
            # Initialize face cascade if not already done
            if not hasattr(self, 'face_cascade'):
                cascade_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ml",
                                            "haarcascade_frontalface_default.xml")
                self.face_cascade = cv2.CascadeClassifier(cascade_path)
                if self.face_cascade.empty():
                    print(f"Error: Unable to load cascade classifier from {cascade_path}")
                    return gray, []

            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(120, 120),
                maxSize=(400, 400)
            )
        except Exception as e:
            print(f"Error in face detection: {str(e)}")
            return gray, []

        return gray, faces

    def update_video_feed(self, frame):
        try:
            # Maintain aspect ratio
            frame = cv2.resize(frame, (640, 480))
            self.update_video_label(frame)
        except Exception as e:
            print(f"Error updating video feed: {str(e)}")

    def process_faces(self, gray, faces):
        try:
            for (x, y, w, h) in faces:
                face_roi_gray = gray[y:y + h, x:x + w]
                face_roi_gray = preprocess(face_roi_gray)
                idx, conf = detect_emotion(face_roi_gray)

                self.emotion_history.append((idx, conf))

            self.update_emotional_feedback()
        except Exception as e:
            print(f"Error processing faces: {str(e)}")

    def load_description_from_file(self, filename):
        """Extract description text from emotion session files"""
        try:
            with open(os.path.join(os.path.dirname(__file__), filename), 'r') as file:
                content = file.read()
                start = content.find('section.setText("""') + 16
                end = content.find('""")', start)
                if start >= 16 and end != -1:
                    description = content[start:end].strip()
                    # Remove any leading/trailing quotes and whitespace
                    description = description.strip('"\' \n')
                    # Remove any leading newlines while preserving internal formatting
                    while description.startswith('\n'):
                        description = description[1:]
                    return description
                else:
                    print(f"Warning: Could not find description markers in {filename}")
                    return """<p><strong style='font-size: 30px;'>Error:</strong><br>
Description not available.</p>"""
        except Exception as e:
            print(f"Error loading description from {filename}: {str(e)}")
            return """<p><strong style='font-size: 30px;'>Error:</strong><br>
Description not available.</p>"""

    def check_emotion_stability(self):
        """Check if an emotion has been dominant for 1.5 seconds"""
        if not self.emotion_history or not self.worker:
            return

        # Ensure class_names is initialized
        if not hasattr(self.worker, 'class_names'):
            self.worker.class_names = ["Annoyed", "Happiness", "Sad", "Upset"]

        # Calculate current emotion percentages
        emotion_counts = np.zeros(len(self.worker.class_names))
        total_conf = 0

        for idx, conf in self.emotion_history:
            emotion_counts[idx] += conf
            total_conf += conf

        if total_conf > 0:
            emotion_percentages = (emotion_counts / total_conf) * 100
            max_emotion_idx = np.argmax(emotion_percentages)
            max_emotion = self.worker.class_names[max_emotion_idx]

            # Only update if the new emotion has a higher percentage
            if max_emotion != self.current_emotion and emotion_percentages[max_emotion_idx] > max(
                    emotion_percentages[i] for i, emotion in enumerate(self.worker.class_names)
                    if emotion != max_emotion
            ):
                self.update_emotion_display(max_emotion)

    def update_emotion_display(self, new_emotion):
        """Update the UI with new emotion information"""
        current_time = time.time()

        # Only update if enough time has passed since last change
        if current_time - self.emotion_start_time >= 1.5:
            self.current_emotion = new_emotion
            self.emotion_start_time = current_time

            # Update emoji with appropriate size based on emotion
            emoji_path = os.path.join(os.path.dirname(__file__), self.emotion_emojis[new_emotion])

            # Use consistent size for all emojis, but make annoyed emoji 15% bigger
            base_size = 238
            emoji_size = (int(base_size * 1.15), int(base_size * 1.15)) if new_emotion == "Annoyed" else (
                base_size, base_size)
            emoji_pixmap = QPixmap(emoji_path).scaled(emoji_size[0], emoji_size[1], Qt.KeepAspectRatio,
                                                      Qt.SmoothTransformation)
            self.annoyed_face_label.setPixmap(emoji_pixmap)

            # Keep confidence section size constant
            self.annoyed_face_label.parent().setFixedSize(298, 298)

            # Update description using the pre-loaded description and set appropriate color
            if new_emotion in self.emotion_descriptions:
                self.explanation_section.setText(self.emotion_descriptions[new_emotion])
                # Set background color based on emotion
                if new_emotion == "Happiness":
                    bg_color = "#B2FFD1"
                elif new_emotion == "Sad":
                    bg_color = "#999999"
                elif new_emotion == "Upset":
                    bg_color = "#E07D7D"
                elif new_emotion == "Annoyed":
                    bg_color = "#ECD60D"
                else:
                    bg_color = "#C1F0D1"  # Default color

                self.explanation_section.setStyleSheet(f"""
                    font-size: 20px;
                    color: #333333;
                    background-color: {bg_color};
                    padding: 28px;
                    border-radius: 25px;
                """)
            else:
                print(f"Warning: No description found for emotion {new_emotion}")

    def update_emotional_feedback(self):
        emotion_counts = np.zeros(len(self.worker.class_names))
        total_conf = 0

        for idx, conf in self.emotion_history:
            emotion_counts[idx] += conf
            total_conf += conf

        if total_conf > 0:
            emotion_percentages = (emotion_counts / total_conf) * 100
        else:
            emotion_percentages = np.zeros(len(self.worker.class_names))

        for i, (emotion, (color, label, progress_bar, percentage_label)) in enumerate(self.emotions_data.items()):
            percentage = int(emotion_percentages[i])
            progress_bar.setValue(percentage)
            percentage_label.setText(f"{percentage}%")

            progress_bar.setStyleSheet(f"""
                QProgressBar {{
                    background-color: rgba(255, 255, 255, 0.3);
                    border-radius: 5px;
                }}
                QProgressBar::chunk {{
                    background-color: {color.name() if percentage > 0 else 'rgba(0, 0, 0, 0)'};
                    border-radius: 5px;
                }}
            """)

        avg_confidence = total_conf / len(self.emotion_history) if self.emotion_history else 0
        self.confidence_label.setText(f"Confidence: {int(avg_confidence * 100)}%")

    def closeEvent(self, event):
        """Ensure video resources are released when closing the window."""
        try:
            self.worker.stop()
            self.worker.wait()
            self.stop_camera()
        except Exception as e:
            print(f"Error in closeEvent: {str(e)}")
        finally:
            event.accept()

    def endSession(self):
        """Handle the End Session button click"""
        try:
            if self.worker:
                self.worker.stop()
                self.worker.wait()
                self.worker = None
            if self.camera_worker:
                self.camera_worker.stop()
                self.camera_worker = None
            # Clear emotion history
            self.emotion_history.clear()
            if self.main_window:
                self.main_window.show_home_page()
            else:
                print("Warning: main_window is None, cannot show user session overview")
                self.close()
        except Exception as e:
            print(f"Error in endSession: {str(e)}")

    def showEvent(self, event):
        """Start the camera when the window is shown"""
        super().showEvent(event)

        # Clean up any existing workers
        if hasattr(self, 'camera_worker') and self.camera_worker:
            self.camera_worker.stop()
            self.camera_worker = None

        if hasattr(self, 'worker') and self.worker:
            self.worker.stop()
            self.worker.wait()
            self.worker = None

        # Create and initialize new workers
        self.camera_worker = CameraWorker()
        self.camera_worker.frame_ready.connect(self.update_video_feed)
        self.camera_worker.faces_detected.connect(self.process_faces)

        self.worker = EmotionDetectionWorker()
        self.worker.result_signal.connect(self.process_worker_result)

        # Start the workers
        self.camera_worker.start_camera()
        self.worker.start()

        # Clear emotion history for fresh start
        self.emotion_history.clear()

    def hideEvent(self, event):
        """Release camera resources when the window is hidden"""
        super().hideEvent(event)
        try:
            if hasattr(self, 'camera_worker') and self.camera_worker:
                self.camera_worker.stop()
                self.camera_worker = None
            if hasattr(self, 'worker') and self.worker:
                self.worker.stop()
                self.worker.wait()
                self.worker = None
            self.emotion_history.clear()
        except Exception as e:
            print(f"Error in hideEvent: {str(e)}")

    def start_camera(self):
        if not self.camera_worker:
            self.camera_worker = CameraWorker()
            self.camera_worker.frame_ready.connect(self.update_video_feed)
            self.camera_worker.faces_detected.connect(self.process_faces)

        if not self.camera_worker.isRunning():
            self.camera_worker.start_camera()

    def stop_camera(self):
        if self.camera_worker:
            self.camera_worker.stop()
            self.camera_worker = None


class CameraWorker(QThread):
    frame_ready = pyqtSignal(np.ndarray)
    faces_detected = pyqtSignal(np.ndarray, object)  # Using object to allow both list and ndarray

    def __init__(self):
        super().__init__()
        self.running = True
        self.camera = None
        self.face_cascade = None
        self.frame_count = 0
        self.skip_frames = 1  # Process every other frame
        self.current_faces = []  # Store current face detections
        self.frame_buffer = []  # Buffer for frame processing
        self.buffer_size = 3  # Number of frames to buffer

    def run(self):
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                print("Error: Unable to open camera")
                return

            # Lower resolution for better performance
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

            # Initialize face cascade once
            cascade_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "..", "ml", "haarcascade_frontalface_default.xml")
            self.face_cascade = cv2.CascadeClassifier(cascade_path)

            # Main capture loop
            while self.running:
                ret, frame = self.camera.read()
                if ret:
                    self.frame_count += 1
                    frame_copy = frame.copy()

                    # Process frames at regular intervals
                    if self.frame_count % (self.skip_frames + 1) == 0:
                        # Face detection
                        gray = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2GRAY)
                        faces = self.face_cascade.detectMultiScale(
                            gray,
                            scaleFactor=1.1,
                            minNeighbors=5,
                            minSize=(60, 60),
                            maxSize=(200, 200)
                        )

                        # Update current faces if faces are detected
                        if len(faces) > 0:
                            self.current_faces = [(int(x), int(y), int(w), int(h)) for x, y, w, h in faces]

                        # Draw detection boxes using current faces
                        for (x, y, w, h) in self.current_faces:
                            cv2.rectangle(frame_copy, (x, y), (x + w, y + h), (255, 0, 0), 3)

                        # Process face detection results
                        self.faces_detected.emit(gray, self.current_faces)
                    else:
                        # Draw previous detection boxes on non-processing frames
                        for (x, y, w, h) in self.current_faces:
                            cv2.rectangle(frame_copy, (x, y), (x + w, y + h), (255, 0, 0), 3)

                    # Emit processed frame
                    self.frame_ready.emit(frame_copy)

                # Add a small sleep to prevent CPU overload
                time.sleep(0.01)

        except Exception as e:
            print(f"Camera error: {str(e)}")
        finally:
            if self.camera:
                self.camera.release()

    def stop(self):
        self.running = False
        self.wait()

    def start_camera(self):
        if not self.running:
            self.running = True
            self.start()
        elif self.camera and not self.camera.isOpened():
            self.camera.open(0)

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#71B89A"))
        gradient.setColorAt(1, QColor("#5A9A7F"))
        painter.fillRect(self.rect(), gradient)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


