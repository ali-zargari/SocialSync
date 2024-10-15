import sys

import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtGui import QFont, QPixmap, QImage, QColor
from PyQt5.QtCore import Qt, QTimer
from backend.controllers.emotion_recognition import detect_face, detect_emotion, preprocess
from ui.pyqt.cv_window import VideoWindow

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent  # Reference to the main stacked window
        self.initUI()

        # Initialize video feed from VideoWindow
        self.video_window = VideoWindow()  # Create an instance of VideoWindow for video handling
        self.video_window.timer.timeout.connect(self.update_video_feed)  # Use the timer from VideoWindow

    def initUI(self):
        self.setWindowTitle('Emotion Recognition UI')
        self.setGeometry(100, 100, 1280, 720)
        self.setStyleSheet("background-color: rgba(113,183,154,1);")
        self.setFont(QFont("Josefin Sans", 12))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self.createHeader())
        layout.addWidget(self.createMainContent())
        layout.addWidget(self.createBottomSection())

    def createHeader(self):
        header = QWidget()
        header.setFixedHeight(100)
        header.setStyleSheet("background-color: white;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(50, 0, 50, 0)

        home_label = QLabel('Home', self)
        home_label.setFont(QFont('Josefin Sans', 32, QFont.Bold))
        home_label.setStyleSheet("color: black;")
        header_layout.addWidget(home_label, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        header_layout.addStretch()

        # Buttons for Profile, History, and Sign Out
        for text in ["Profile", "History", "Sign Out"]:
            button = QPushButton(text, self)
            button.setFixedSize(150, 50)
            button.setFont(QFont('Josefin Sans', 16))
            button.setStyleSheet("""
                color: white;
                background-color: rgba(113, 184, 154, 1);
                border-radius: 25px;
            """)
            button.clicked.connect(lambda checked, btn=text: self.handle_button_click(btn))
            header_layout.addWidget(button)
            if text != "Sign Out":
                header_layout.addSpacing(20)

        return header

    def handle_button_click(self, btn_name):
        """ Handle button clicks for Profile, History, and Sign Out """
        if btn_name == "Profile":
            self.main_window.show_care_profile_settings()
        elif btn_name == "History":
            self.main_window.show_history_page()
        elif btn_name == "Sign Out":
            self.main_window.show_login_page()

    def createMainContent(self):
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(50, 50, 50, 50)
        content_layout.setSpacing(50)

        content_layout.addWidget(self.createEmotionBubble())
        content_layout.addWidget(self.createConfidenceSection())
        content_layout.addWidget(self.createVideoFeedSection())  # Use the video feed

        return content

    def createEmotionBubble(self):
        bubble = QFrame()
        bubble.setFixedSize(360, 360)
        bubble.setStyleSheet("background-color: transparent;")

        oval = QLabel(bubble)
        oval.setFixedSize(360, 360)
        oval.setStyleSheet("""
            background-color: white;
            border-radius: 180px;
        """)

        profile_logo = QLabel(bubble)
        profile_logo.setPixmap(
            QPixmap("images/v20_308.png").scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        profile_logo.move(20, 20)

        emotions = [
            ("Annoyed: 90%", 90, 110, QColor(255, 193, 7)),
            ("Happiness: 3%", 90, 170, QColor(12, 150, 67)),
            ("Sad: 2%", 90, 230, QColor(77, 77, 77)),
            ("Upset: 1%", 90, 290, QColor(191, 27, 27))
        ]

        for text, x, y, color in emotions:
            label = QLabel(text, bubble)
            label.setStyleSheet(f"""
                font-size: 22px;
                color: rgb({color.red()}, {color.green()}, {color.blue()});
                background-color: transparent;
                font-weight: bold;
            """)
            label.move(x, y)

        return bubble

    def createConfidenceSection(self):
        section = QFrame()
        section.setFixedSize(360, 360)
        layout = QVBoxLayout(section)

        confidence_label = QLabel("Confidence: 78%", section)
        confidence_label.setStyleSheet("font-size: 32px; color: white;")
        confidence_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(confidence_label)

        annoyed_face_label = QLabel(section)
        annoyed_face_label.setPixmap(
            QPixmap("images/v25_545.png").scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        annoyed_face_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(annoyed_face_label)

        return section

    def createVideoFeedSection(self):
        """ This method sets up the video feed section. """
        self.video_label = QLabel(self)
        self.video_label.setFixedSize(360, 360)
        return self.video_label

    def createBottomSection(self):
        section = QFrame()
        layout = QVBoxLayout(section)
        layout.setContentsMargins(50, 20, 50, 50)

        explanation = self.createExplanationSection()
        layout.addWidget(explanation)

        help_button = QPushButton('Help', self)
        help_button.setFixedSize(100, 40)
        help_button.setFont(QFont('Josefin Sans', 16, QFont.Bold))
        help_button.setStyleSheet("""
            QPushButton {
                color: #5F9EA0;
                background-color: white;
                border: none;
                border-radius: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F0F0F0;
            }
        """)
        layout.addWidget(help_button, alignment=Qt.AlignLeft)

        return section

    def update_video_feed(self):
        """ Update video feed in the main window by reusing video logic from VideoWindow. """
        ret, frame = self.video_window.video.read()
        if ret:
            gray, faces = detect_face(frame)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                face_roi_gray = gray[y:y + h, x:x + w]
                face_roi_gray = preprocess(face_roi_gray)
                idx, conf = detect_emotion(face_roi_gray)

                class_name = self.video_window.class_names[idx]

                if conf > 0.3:
                    cv2.putText(frame, class_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Convert the frame to QImage for PyQt display
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(qt_image))

    def createExplanationSection(self):
        section = QLabel()
        section.setText("""
        <p><strong style='font-size: 24px;'>Upset:</strong><br>
        Being upset is when you feel bad because something didn't go the way you hoped.</p>

        <p><strong style='font-size: 24px;'>Respond:</strong><br>
        Frown Lower your tone Tell them they are making you upset</p>
        """)
        section.setWordWrap(True)
        section.setStyleSheet("""
            font-size: 18px;
            color: #333;
            background-color: rgba(255,150,150,1);
            padding: 30px;
            border-radius: 20px;
        """)
        section.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        return section

    def closeEvent(self, event):
        """ Ensure video resources are released when closing the window. """
        self.video_window.timer.stop()
        self.video_window.video.release()
        event.accept()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
