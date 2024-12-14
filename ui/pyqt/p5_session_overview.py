import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
                             QFrame, QSizePolicy, QGraphicsDropShadowEffect, QGridLayout)
from PyQt5.QtGui import QFont, QPixmap, QColor, QPainter, QLinearGradient
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QTimer
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


class CustomAddUserButton(AnimatedButton):
    def __init__(self, parent=None):
        super().__init__("Add User", parent)
        self.initUI()

    def initUI(self):
        self.setStyleSheet("""
        QPushButton {
            background-color: white;
            color: #71B89A;
            border-radius: 25px;
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
            text-align: left;
            padding-left: 60px;
        }
        QPushButton:hover {
            background-color: #F0F0F0;
        }
    """)

        plus_label = QLabel(self)
        plus_label.setFixedSize(40, 40)
        plus_label.setStyleSheet("""
            background-color: #71B89A;
            border-radius: 20px;
        """)
        plus_label.move(10, 5)

        plus_sign = QLabel("+", plus_label)
        plus_sign.setAlignment(Qt.AlignCenter)
        plus_sign.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: white;
        """)
        plus_sign.setGeometry(0, 0, 40, 40)

        self.setText("Add User")
        self.setFixedSize(300, 50)
        self.setCursor(Qt.PointingHandCursor)


class OverviewScreen(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.initUI()
        self.parent = parent

    def initUI(self):
        self.setWindowTitle('Session Overview')
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

        header_title = QLabel('Session Overview Home', self)
        header_title.setFont(QFont('Arial', 28, QFont.Bold))
        header_title.setStyleSheet("color: #71B89A;")
        header_inner_layout.addWidget(header_title, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        header_inner_layout.addStretch()

        profile_button = AnimatedButton("Profile", self)
        profile_button.setFixedSize(120, 50)
        profile_button.clicked.connect(self.go_to_care_profile_settings)

        header_inner_layout.addWidget(profile_button, alignment=Qt.AlignRight | Qt.AlignVCenter)

        return header_container

    def createMainContent(self):
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(50, 50, 50, 50)
        content_layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel("Please Select User", self)
        title_label.setFont(QFont('Arial', 48, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        title_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(title_label, alignment=Qt.AlignCenter)

        content_layout.addSpacing(40)

        name_label = QLabel("Individual's Name:", self)
        name_label.setFont(QFont('Arial', 20, QFont.Bold))
        name_label.setStyleSheet("color: white;")
        name_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(name_label, alignment=Qt.AlignCenter)

        content_layout.addSpacing(20)

        name_button = AnimatedButton("John Doe", self)
        name_button.setFixedSize(300, 60)
        name_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #71B89A;
                border-radius: 30px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        """)
        name_button.clicked.connect(self.go_to_session_overview)

        content_layout.addWidget(name_button, alignment=Qt.AlignCenter)

        content_layout.addSpacing(20)

        add_user_button = CustomAddUserButton(self)
        content_layout.addWidget(add_user_button, alignment=Qt.AlignCenter)

        return content

    def go_to_care_profile_settings(self):
        """Navigate to the Care Profile Settings page (p6) in the main window."""
        if self.parent:
            self.parent.show_care_profile_settings()  # Call the parent's navigation method

    def go_to_add_user(self):
        """Navigate to the Add User page (p7) in the main window."""
        pass

    def go_to_session_overview(self):
        """Navigate to the Session Overview page (p5) in the main window."""
        if self.parent:
            self.parent.show_selected_user_session_overview()




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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OverviewScreen()
    window.show()
    sys.exit(app.exec_())