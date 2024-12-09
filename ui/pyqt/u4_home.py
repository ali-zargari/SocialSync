import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
                             QFrame, QSizePolicy, QGraphicsDropShadowEffect, QGridLayout)
from PyQt5.QtGui import QFont, QPixmap, QColor, QPainter, QLinearGradient
from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint


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


class MainWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window  # Reference to the main window with navigation methods
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Home Page')
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #71B89A;")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.main_layout.addWidget(self.createHeader())
        self.content_widget = QWidget()
        self.main_layout.addWidget(self.content_widget)
        self.main_layout.addWidget(self.createBottomSection())

        self.updateMainContent()

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

        header_title = QLabel('Home', self)
        header_title.setFont(QFont('Arial', 28, QFont.Bold))
        header_title.setStyleSheet("color: #71B89A;")
        header_inner_layout.addWidget(header_title, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        header_inner_layout.addStretch()

        # Create Profile, History, and Sign Out buttons
        for text in ["Profile", "History", "Sign Out"]:
            button = AnimatedButton(text, self)
            button.setFixedSize(120, 50)
            if text == "Profile":
                button.clicked.connect(self.main_window.show_profile_setting_gui)
            elif text == "History":
                button.clicked.connect(self.main_window.show_history_page)
            elif text == "Sign Out":
                button.clicked.connect(self.main_window.show_login_page)
            header_inner_layout.addWidget(button, alignment=Qt.AlignRight | Qt.AlignVCenter)

        return header_container

    def updateMainContent(self):
        # Clear the existing content
        if self.content_widget.layout():
            QWidget().setLayout(self.content_widget.layout())

        # Load user info from JSON file
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(project_root, "data")
        json_path = os.path.join(data_dir, "login_data.json")
        with open(json_path, "r") as file:
            login_data = json.load(file)

        # Extract first name and last name from the JSON
        first_name = login_data["user_info"]["first_name"]
        last_name = login_data["user_info"]["last_name"]

        content_layout = QGridLayout(self.content_widget)
        content_layout.setContentsMargins(50, 50, 50, 50)

        welcome_label = QLabel(f"Welcome, {first_name} {last_name}", self)
        welcome_label.setFont(QFont('Arial', 48, QFont.Bold))
        welcome_label.setStyleSheet("color: white;")
        welcome_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(welcome_label, 0, 0, 1, 1, Qt.AlignCenter)

        start_button = AnimatedButton("Start", self)
        start_button.setFixedSize(800, 200)
        start_button.setFont(QFont('Arial', 36, QFont.Bold))
        start_button.setStyleSheet("""
            QPushButton {
                background-color: #C1F0D1;
                color: black;
                border-radius: 100px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #A9E4BC;
            }
        """)
        content_layout.addWidget(start_button, 1, 0, 1, 1, Qt.AlignCenter)
        start_button.clicked.connect(lambda: self.main_window.show_video_window())

        content_layout.setRowStretch(0, 1)
        content_layout.setRowStretch(1, 1)
        content_layout.setRowStretch(2, 1)

    def createBottomSection(self):
        section = QFrame()
        layout = QHBoxLayout(section)
        layout.setContentsMargins(50, 0, 50, 20)
        layout.setSpacing(10)

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
        layout.addWidget(help_button, alignment=Qt.AlignLeft | Qt.AlignBottom)
        layout.addStretch()

        return section

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#71B89A"))
        gradient.setColorAt(1, QColor("#5A9A7F"))
        painter.fillRect(self.rect(), gradient)

    def showEvent(self, event):
        super().showEvent(event)
        self.updateMainContent()


if __name__ == '__main__':
    from ui.pyqt.main_window import MainWindow as AppMainWindow  # Import the actual MainWindow class
    app = QApplication(sys.argv)
    main_app_window = AppMainWindow()
    main_window = MainWindow(main_app_window)
    main_window.show()
    sys.exit(app.exec_())