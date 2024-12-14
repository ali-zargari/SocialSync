import sys
from collections import deque
import time
import cv2
import numpy as np
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
                             QFrame, QSizePolicy, QGraphicsDropShadowEffect, QProgressBar)
from PyQt5.QtGui import QFont, QPixmap, QImage, QColor, QPainter, QLinearGradient
from PyQt5.QtCore import Qt, QPoint, QPropertyAnimation, QTimer
from ui.controllers.emotion_recognition import detect_face, detect_emotion, preprocess, EmotionDetectionWorker
from ui.pyqt.cv_window import VideoWindow
import os

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

        # Timer for emotion stability check
        self.emotion_timer = QTimer()
        self.emotion_timer.timeout.connect(self.check_emotion_stability)
        self.emotion_timer.start(1500)  # Check every 1.5 seconds


    def process_worker_result(self, frame, emotions, confidence):
        # Update emotion history
        for emotion_label, conf in emotions.items():
            idx = self.worker.class_names.index(emotion_label)
            self.emotion_history.append((idx, conf))

        # Update the UI elements directly
        self.update_video_label(frame)
        self.update_emotional_feedback()
        self.update_confidence_label(confidence)

    def update_video_label(self, frame):
        # Convert the frame to QImage for PyQt display
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image).scaled(288, 208, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.video_label.setPixmap(pixmap)

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
        content_layout.setContentsMargins(40, 15, 40, 40)        # Reduced top margin to move content up
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

            percentage_label.setStyleSheet("color: white; font-size: 22px; font-weight: bold; background: transparent;")  # Increased from 18px

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
        annoyed_face_pixmap = QPixmap(image_path2).scaled(245, 245, Qt.KeepAspectRatio, Qt.SmoothTransformation) # MODIFIED: Increased emoji size from 120x120 to 160x160
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
        self.face_detection_label.setStyleSheet("color: red; font-size: 14px; font-weight: bold; border: 2px solid black; "
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

    def update_video_feed(self):
        """ Update video feed in the main window by reusing video logic from VideoWindow. """
        ret, frame = self.video_window.video.read()
        if ret:
            gray, faces = detect_face(frame)

            # Process each detected face
            for (x, y, w, h) in faces:
                # Draw a rectangle around the detected face
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 4)
                face_roi_gray = gray[y:y + h, x:x + w]
                face_roi_gray = preprocess(face_roi_gray)
                idx, conf = detect_emotion(face_roi_gray)

                # Get the emotion label based on the detected index
                emotion_label = self.video_window.class_names[idx]

                # Display the emotion label on the bounding box with larger font
                label_position = (x, y - 10) if y > 20 else (x, y + h + 20)
                cv2.putText(frame, emotion_label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 4)

                # Append current emotion data to history
                self.emotion_history.append((idx, conf))

                # Calculate the average emotion percentages over the last 100 frames
                self.update_emotional_feedback()

            # Convert the frame to QImage for PyQt display
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.video_label.setPixmap(
                QPixmap.fromImage(qt_image).scaled(288, 208, Qt.KeepAspectRatio, Qt.SmoothTransformation))

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
        if not self.emotion_history:
            return

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
            emoji_size = (int(base_size * 1.15), int(base_size * 1.15)) if new_emotion == "Annoyed" else (base_size, base_size)
            emoji_pixmap = QPixmap(emoji_path).scaled(emoji_size[0], emoji_size[1], Qt.KeepAspectRatio, Qt.SmoothTransformation)
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
        """ Ensure video resources are released when closing the window. """
        self.worker.stop()
        self.worker.wait()
        event.accept()

    def endSession(self):
        """Handle the End Session button click"""
        self.worker.stop()
        self.worker.wait()
        self.main_window.show_user_session_overview()

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
