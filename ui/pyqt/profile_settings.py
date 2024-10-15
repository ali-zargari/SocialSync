import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QFrame, QSizePolicy)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, QSize


class ProfilePage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #8FBC8F;")  # Sea Green color

        # Main layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header = QWidget()
        header.setStyleSheet("background-color: white;")
        header.setFixedHeight(80)
        header_layout = QHBoxLayout(header)

        logo_label = QLabel("Logo")
        logo_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        profile_label = QLabel("Profile")
        profile_label.setStyleSheet("font-size: 36px; font-weight: bold;")

        sign_out_button = self.create_button("Sign Out", "#8FBC8F")
        sign_out_button.setFixedSize(120, 40)

        header_layout.addWidget(logo_label)
        header_layout.addWidget(profile_label)
        header_layout.addStretch(1)
        header_layout.addWidget(sign_out_button)
        header_layout.setContentsMargins(20, 0, 20, 0)

        # Content area
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        # Left sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(300)
        sidebar_layout = QVBoxLayout(sidebar)

        profile_pic = QLabel()
        profile_pic.setPixmap(QPixmap("placeholder.png").scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        profile_pic.setAlignment(Qt.AlignCenter)

        username_label = QLabel("Username")
        full_name_label = QLabel("Full Name")
        email_label = QLabel("Email")

        for label in [username_label, full_name_label, email_label]:
            label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")

        sidebar_layout.addWidget(profile_pic)
        sidebar_layout.addWidget(username_label)
        sidebar_layout.addWidget(full_name_label)
        sidebar_layout.addWidget(email_label)
        sidebar_layout.addStretch(1)

        # Right content
        right_content = QWidget()
        right_layout = QVBoxLayout(right_content)
        right_layout.setAlignment(Qt.AlignCenter)
        right_layout.setSpacing(20)

        settings_label = QLabel("Settings")
        settings_label.setStyleSheet("color: white; font-size: 48px; font-weight: bold;")
        settings_label.setAlignment(Qt.AlignCenter)

        vocal_visual_button = self.create_button("Vocal and Visual Settings", "#D3D3D3")
        reset_label = QLabel("Reset")
        reset_label.setStyleSheet("color: white; font-size: 36px; font-weight: bold;")
        reset_label.setAlignment(Qt.AlignCenter)

        password_button = self.create_button("Password", "#D3D3D3")
        email_button = self.create_button("Email", "#D3D3D3")
        profile_pic_button = self.create_button("Profile Pic", "#D3D3D3")

        right_layout.addWidget(settings_label)
        right_layout.addWidget(vocal_visual_button)
        right_layout.addWidget(reset_label)
        right_layout.addWidget(password_button)
        right_layout.addWidget(email_button)
        right_layout.addWidget(profile_pic_button)

        # Bottom buttons
        bottom_buttons = QWidget()
        bottom_layout = QHBoxLayout(bottom_buttons)

        help_button = self.create_button("Help", "white")
        back_button = self.create_button("Back", "#4682B4")  # Steel Blue color

        bottom_layout.addWidget(help_button)
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(back_button)

        # Add all widgets to the main layout
        main_layout.addWidget(header)
        content_layout.addWidget(sidebar)
        content_layout.addWidget(right_content)
        main_layout.addWidget(content)
        main_layout.addWidget(bottom_buttons)

    def create_button(self, text, color):
        button = QPushButton(text)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border-radius: 20px;
                padding: 10px;
                font-size: 18px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #A9A9A9;
            }}
        """)
        button.clicked.connect(lambda: print(f"{text} button clicked"))
        return button


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProfilePage()
    window.show()
    sys.exit(app.exec_())