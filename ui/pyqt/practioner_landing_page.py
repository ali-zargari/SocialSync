import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPixmap, QPainter, QColor, QLinearGradient
from PyQt5.QtCore import Qt, QRect

class SimpleButton(QPushButton):
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
        self.setCursor(Qt.PointingHandCursor)

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
        self.container.setGeometry(QRect(290, 100, 700, 520))
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

        # SocialSync text
        title_label = QLabel("SocialSync", self.container)
        title_label.setStyleSheet("color: #71B89A; font-size: 42px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Register New Patients button
        self.register_button = SimpleButton("Register New Patients", self.container)
        self.register_button.setFixedSize(300, 50)
        self.register_button.clicked.connect(self.register_page)
        layout.addWidget(self.register_button, alignment=Qt.AlignCenter)

        # Patients List button
        self.patients_list_button = SimpleButton("Patients List", self.container)
        self.patients_list_button.setFixedSize(300, 50)
        layout.addWidget(self.patients_list_button, alignment=Qt.AlignCenter)

        # Sessions button
        self.sessions_button = SimpleButton("Sessions", self.container)
        self.sessions_button.setFixedSize(300, 50)
        layout.addWidget(self.sessions_button, alignment=Qt.AlignCenter)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Create gradient background
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor("#71B89A"))
        gradient.setColorAt(1, QColor("#5A9A7F"))
        painter.fillRect(self.rect(), gradient)

    def register_page(self):
        # Placeholder for register page functionality
        if self.parent:
            self.parent.show_register_page()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginPage()
    window.show()
    sys.exit(app.exec_())

