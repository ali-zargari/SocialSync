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

        # ASD Practitioner button
        self.practitioner_button = SimpleButton("ASD Practitioner", self.container)
        self.practitioner_button.setFixedSize(300, 50)
        self.practitioner_button.clicked.connect(self.show_asd_practitioner_registration)
        layout.addWidget(self.practitioner_button, alignment=Qt.AlignCenter)

        # ASD Patient button
        self.patient_button = SimpleButton("ASD Patient", self.container)
        self.patient_button.setFixedSize(300, 50)
        self.patient_button.clicked.connect(self.show_asd_patient_registration)
        layout.addWidget(self.patient_button, alignment=Qt.AlignCenter)

        # Cancel button
        self.cancel_button = SimpleButton("Cancel", self.container)
        self.cancel_button.setFixedSize(300, 50)
        self.cancel_button.clicked.connect(self.cancel_registration)
        layout.addWidget(self.cancel_button, alignment=Qt.AlignCenter)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Create gradient background
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor("#71B89A"))
        gradient.setColorAt(1, QColor("#5A9A7F"))
        painter.fillRect(self.rect(), gradient)

    def show_asd_practitioner_registration(self):
        if self.parent:
            self.parent.show_asd_practitioner_registration()

    def show_asd_patient_registration(self):
        if self.parent:
            self.parent.show_asd_patient_registration()

    def cancel_registration(self):
        if self.parent:
            self.parent.show_login_page()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginPage()
    window.show()
    sys.exit(app.exec_())

