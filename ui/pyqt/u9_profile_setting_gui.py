import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QFrame, QSizePolicy, QGraphicsDropShadowEffect)
from PyQt5.QtGui import QFont, QPixmap, QColor, QPainter, QLinearGradient
from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint
import os
import json

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


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent  # Store reference to parent for navigation
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Profile Settings')
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #71B89A;")

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
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
        logo_label.setPixmap(pixmap)
        header_inner_layout.addWidget(logo_label, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        header_title = QLabel('Profile Settings', self)
        header_title.setFont(QFont('Arial', 28, QFont.Bold))
        header_title.setStyleSheet("color: #71B89A;")
        header_inner_layout.addWidget(header_title, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        header_inner_layout.addStretch()

        sign_out_btn = AnimatedButton("Sign Out", self)
        sign_out_btn.setFixedSize(120, 50)
        sign_out_btn.clicked.connect(self.sign_out)  # Connect to the sign_out method


        header_inner_layout.addWidget(sign_out_btn, alignment=Qt.AlignRight | Qt.AlignVCenter)

        return header_container

    def sign_out(self):
        """Navigate to the login page if parent is available."""
        if self.parent:
            self.parent.show_login_page()  # Call the parent's show_login_page method


    def createMainContent(self):
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(50, 50, 50, 50)
        content_layout.setSpacing(20)

        left_column = self.createLeftColumn()
        right_column = self.createRightColumn()

        content_layout.addWidget(left_column, 1, alignment=Qt.AlignLeft | Qt.AlignTop)
        content_layout.addWidget(right_column, 1, alignment=Qt.AlignRight | Qt.AlignTop)

        return content

    def createLeftColumn(self):
        left_column = RoundedFrame()
        left_layout = QVBoxLayout(left_column)
        left_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.setSpacing(20)

        profile_pic_container = QLabel()
        image_path2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images/add_pic.png")
        profile_pixmap = QPixmap(image_path2)
        profile_pic_container.setPixmap(profile_pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        profile_pic_container.setAlignment(Qt.AlignCenter)

        left_layout.addWidget(profile_pic_container, alignment=Qt.AlignHCenter)

        # Load user info from JSON file
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(project_root, "data")
        json_path = os.path.join(data_dir, "login_data.json")

        try:
            with open(json_path, "r") as file:
                login_data = json.load(file)

            first_name = login_data["user_info"].get("first_name", "Unknown")
            last_name = login_data["user_info"].get("last_name", "Unknown")
            email = login_data["user_info"].get("email", "Email Not Available")
        except (FileNotFoundError, KeyError, json.JSONDecodeError):
            first_name, last_name, email = "Unknown", "Unknown", "Email Not Available"

        # Add user details
        for text in [f"First Name: {first_name}", f"Last Name: {last_name}", f"Email: {email}"]:
            label = QLabel(text)
            label.setStyleSheet("color: white; font-size: 24px; font-weight: bold; text-align: center;")
            label.setAlignment(Qt.AlignCenter)
            left_layout.addWidget(label)

        left_layout.addStretch()

        return left_column

    def createRightColumn(self):
        right_column = RoundedFrame()
        right_layout = QVBoxLayout(right_column)
        right_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(20)

        settings_label = QLabel("Settings")
        settings_label.setStyleSheet("color: white; font-size: 36px; font-weight: bold;")
        right_layout.addWidget(settings_label, alignment=Qt.AlignHCenter)

        for text in ["Vocal and Visual Settings", "Password", "Email", "Profile Pic", "Reset"]:
            btn = self.create_settings_button(text)
            right_layout.addWidget(btn, alignment=Qt.AlignHCenter)

        right_layout.addStretch()

        return right_column

    def createBottomSection(self):
        section = QFrame()
        layout = QHBoxLayout(section)
        layout.setContentsMargins(50, 0, 50, 20)
        layout.setSpacing(20)

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
        layout.addWidget(help_button, alignment=Qt.AlignLeft)

        layout.addStretch()

        back_button = AnimatedButton('Back', self)
        back_button.setFixedSize(120, 50)
        back_button.setStyleSheet("""
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
        back_button.clicked.connect(self.go_back)  # Connect to go_back method
        layout.addWidget(back_button, alignment=Qt.AlignRight)

        return section

    def create_settings_button(self, text):
        button = QPushButton(text, self)
        button.setFixedSize(400, 60)
        button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.3);
                color: white;
                border: none;
                border-radius: 30px;
                font-size: 18px;
                font-weight: bold;
                text-align: center;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.4);
            }
        """)
        return button

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#71B89A"))
        gradient.setColorAt(1, QColor("#5A9A7F"))
        painter.fillRect(self.rect(), gradient)

    def go_back(self):
        """Navigate to the previous page if parent is available."""
        if self.parent:
            self.parent.go_back()  # Call the parent's go_back method


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QWidget()  # Assuming there's a parent widget handling navigation
    window = MainWindow(parent=main_window)
    window.show()
    sys.exit(app.exec_())
