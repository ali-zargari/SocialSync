from ui.utils.cache_utils import save_login_data
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, \
    QGraphicsDropShadowEffect, QMessageBox
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor, QLinearGradient, QPen
from PyQt5.QtCore import Qt, QRect, QPropertyAnimation, QEasingCurve, QPoint, QTimer
from urllib3 import request
import requests
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

class LoginPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.parent = parent

    def initUI(self):
        self.setWindowTitle('SocialSync')
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #71B89A;")

        # Main container
        self.container = QWidget(self)
        self.container.setGeometry(QRect(190, 30, 900, 660))
        self.container.setStyleSheet("""
            background-color: white;
            border-radius: 40px;
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 10)
        self.container.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)

        # Logo
        logo_label = QLabel(self.container)
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images/v26_279.png")
        logo_pixmap = QPixmap(image_path)
        logo_label.setPixmap(logo_pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setFixedSize(170, 170)
        layout.addWidget(logo_label, alignment=Qt.AlignCenter)

        # SocialSync text
        title_label = QLabel("SocialSync", self.container)
        title_label.setStyleSheet("color: #71B89A; font-size: 42px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Username input
        self.username_input = self.create_input("Username")
        layout.addWidget(self.username_input, alignment=Qt.AlignCenter)

        # Password input
        self.password_input = self.create_input("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input, alignment=Qt.AlignCenter)

        # Sign In button
        self.sign_in_button = AnimatedButton("Sign In", self.container)
        self.sign_in_button.setFixedSize(300, 50)
        self.sign_in_button.clicked.connect(self.login)
        layout.addWidget(self.sign_in_button, alignment=Qt.AlignCenter)

        # New User button
        self.new_user_button = AnimatedButton("New User?", self.container)
        self.new_user_button.setFixedSize(300, 50)
        self.new_user_button.clicked.connect(self.register_page)
        layout.addWidget(self.new_user_button, alignment=Qt.AlignCenter)

        # Forgot Password button
        self.forgot_password_button = AnimatedButton("Forgot Password?", self.container)
        self.forgot_password_button.setFixedSize(300, 50)
        layout.addWidget(self.forgot_password_button, alignment=Qt.AlignCenter)

        # Add hover animations
        for button in [self.sign_in_button, self.new_user_button, self.forgot_password_button]:
            button.setCursor(Qt.PointingHandCursor)

        # Animate container on show
        self.show_animation = QPropertyAnimation(self.container, b"pos")
        self.show_animation.setDuration(1000)
        self.show_animation.setStartValue(QPoint(190, -660))
        self.show_animation.setEndValue(QPoint(190, 30))
        self.show_animation.setEasingCurve(QEasingCurve.OutBack)

        # Start animation after a short delay
        QTimer.singleShot(100, self.show_animation.start)

    def create_input(self, placeholder):
        input_field = QLineEdit(self.container)
        input_field.setPlaceholderText(placeholder)
        input_field.setFixedSize(300, 50)
        input_field.setStyleSheet("""
            QLineEdit {
                background-color: #F0F0F0;
                border: 2px solid #E0E0E0;
                border-radius: 25px;
                padding-left: 20px;
                font-size: 16px;
                color: #555;
            }
            QLineEdit:focus {
                border: 2px solid #71B89A;
            }
        """)
        return input_field

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Create gradient background
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor("#71B89A"))
        gradient.setColorAt(1, QColor("#5A9A7F"))
        painter.fillRect(self.rect(), gradient)

    def login(self):
        # Get input from the fields
        email = self.username_input.text()
        password = self.password_input.text()

        # Prepare the data payload
        data = {
            "email": email,
            "password": password
        }

        try:
            # Send the POST request with JSON data
            response = requests.post("http://127.0.0.1:8081/login", json=data)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Check if login was successful
            if response.status_code == 200:
                # Parse the JSON response
                login_data = response.json()

                # Save login data to a JSON file
                save_login_data(login_data)

                # Navigate to the home page or next component
                self.parent.show_home_page()
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid credentials or server error.")

        except requests.exceptions.RequestException as e:
            # Handle connection errors or other exceptions
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def register_page(self):
        if self.parent:
            self.parent.show_new_user_flow()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginPage()
    window.show()
    sys.exit(app.exec_())

