import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QLabel, QFrame, QHBoxLayout)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, QSize

class CareProfile(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #8FBC8F;")  # Sea Green color
        self.parent = parent

        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header = QWidget()
        header.setStyleSheet("background-color: white;")
        header.setFixedHeight(80)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)

        # Logo
        pixmap = QPixmap("A:\\OneDrive\\Documents\\Ali's Documents\\SE_\\CMPE 195B Senior Project II\\SocialSync\\ui\\PyQt\\images\\v20_308.png")
        scaled_pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label = QLabel()
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setFixedSize(60, 60)

        title_label = QLabel("Care Profile")
        title_label.setStyleSheet("font-size: 36px; font-weight: bold;")

        sign_out_button = self.create_button("Sign Out", "#8FBC8F", text_color="white")
        sign_out_button.setFixedSize(120, 40)

        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch(1)
        header_layout.addWidget(sign_out_button)

        # Content area
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.setSpacing(0)  # Set spacing to 0 to control the gap manually

        # Left sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(300)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setAlignment(Qt.AlignTop)
        sidebar_layout.setSpacing(20)

        info_labels = ["Full Name", "Email", "Caretaker ID"]
        for label in info_labels:
            info_label = QLabel(label)
            info_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
            sidebar_layout.addWidget(info_label)

        # Vertical line
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setStyleSheet("color: white;")  # Set the color of the line to white

        # Right content
        right_content = QWidget()
        right_layout = QVBoxLayout(right_content)
        right_layout.setAlignment(Qt.AlignTop)
        right_layout.setSpacing(20)

        # Reset section
        reset_section = QWidget()
        reset_layout = QVBoxLayout(reset_section)
        reset_layout.setAlignment(Qt.AlignCenter)
        reset_layout.setSpacing(20)

        reset_label = QLabel("Reset")
        reset_label.setStyleSheet("color: white; font-size: 36px; font-weight: bold;")
        reset_label.setAlignment(Qt.AlignCenter)

        password_button = self.create_button("Password", "#D3D3D3", text_color="#4682B4")
        email_button = self.create_button("Email", "#D3D3D3", text_color="#4682B4")

        reset_layout.addWidget(reset_label)
        reset_layout.addWidget(password_button)
        reset_layout.addWidget(email_button)

        # Accounts section
        accounts_section = QWidget()
        accounts_layout = QVBoxLayout(accounts_section)
        accounts_layout.setAlignment(Qt.AlignCenter)
        accounts_layout.setSpacing(20)

        accounts_label = QLabel("Accounts")
        accounts_label.setStyleSheet("color: white; font-size: 36px; font-weight: bold;")
        accounts_label.setAlignment(Qt.AlignCenter)

        edit_users_button = self.create_button("Edit Users", "#D3D3D3", text_color="#4682B4")

        accounts_layout.addWidget(accounts_label)
        accounts_layout.addWidget(edit_users_button)

        # Add sections to right layout
        right_layout.addWidget(reset_section)
        right_layout.addSpacing(40)
        right_layout.addWidget(accounts_section)
        right_layout.addStretch(1)

        # Add widgets to content layout
        content_layout.addWidget(sidebar)
        content_layout.addWidget(line)
        content_layout.addWidget(right_content)

        # Bottom buttons
        bottom_buttons = QWidget()
        bottom_layout = QHBoxLayout(bottom_buttons)
        bottom_layout.setContentsMargins(40, 0, 40, 40)

        help_button = self.create_button("Help", "white", text_color="#8FBC8F")
        back_button = self.create_button("Back", "#4682B4", text_color="white")

        bottom_layout.addWidget(help_button)
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(back_button)

        # Add all widgets to the main layout
        main_layout.addWidget(header)
        main_layout.addWidget(content)
        main_layout.addWidget(bottom_buttons)

    def create_button(self, text, bg_color, text_color="black"):
        button = QPushButton(text)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border-radius: 20px;
                padding: 10px;
                font-size: 18px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #A9A9A9;
            }}
        """)
        button.setFixedSize(200, 50)
        button.clicked.connect(lambda: print(f"{text} button clicked"))
        return button

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CareProfile()
    window.show()
    sys.exit(app.exec_())