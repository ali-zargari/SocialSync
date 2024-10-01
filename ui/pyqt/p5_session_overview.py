import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

class CustomAddUserButton(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Create circular background with plus sign
        plus_label = QLabel(self)
        plus_label.setFixedSize(40, 40)  # Reverted size to 40x40
        plus_label.setStyleSheet("""
            background-color: white;
            border-radius: 20px;
        """)

        # Add "+" sign to the circular background
        plus_sign = QLabel("+", plus_label)
        plus_sign.setAlignment(Qt.AlignCenter)
        plus_sign.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: black;
        """)
        plus_sign.setGeometry(0, 0, 40, 40)  # Adjusted to match new size

        # Add User text
        text_label = QLabel("Add User", self)
        text_label.setStyleSheet("""
            color: black;
            font-size: 18px;
            font-weight: bold;
        """)

        layout.addWidget(plus_label)
        layout.addWidget(text_label)
        layout.addStretch()

        self.setFixedHeight(40)  # Adjusted height to match the circle
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        print("Add User button clicked")

class OverviewScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set fixed window size to 1280x720
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #71B89A;")  # Green background color

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)  # No margins

        # Header: Full width, with logo and profile button
        header_layout = QHBoxLayout()
        header_container = QWidget(self)  # Container for header
        header_container.setStyleSheet("background-color: white;")
        header_container.setFixedHeight(80)  # Height of the header
        header_container.setFixedWidth(1280)  # Full screen width

        header_inner_layout = QHBoxLayout(header_container)
        header_inner_layout.setContentsMargins(10, 0, 10, 0)  # Add left and right padding

        # Logo
        logo_label = QLabel(self)
        pixmap = QPixmap('images/v20_308.png')
        scaled_pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        header_inner_layout.addWidget(logo_label, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        # Title "Session Overview Home" next to logo
        header_title = QLabel('Session Overview Home', self)
        header_title.setFont(QFont('Arial', 28, QFont.Bold))
        header_title.setStyleSheet("color: black;")  # Black text for title
        header_inner_layout.addWidget(header_title, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        # Add stretch to push the profile button to the right
        header_inner_layout.addStretch()

        # Profile button on the right (now green with white text)
        profile_button = self.create_button('Profile', 120, 50, bg_color="#71B89A", text_color="white")
        header_inner_layout.addWidget(profile_button, alignment=Qt.AlignRight | Qt.AlignVCenter)

        header_layout.addWidget(header_container)
        main_layout.addLayout(header_layout)

        # Add vertical spacer to push "Please Select User" text lower
        main_layout.addItem(QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Title: "Please Select User"
        title_label = QLabel("Please Select User", self)
        title_label.setFont(QFont('Arial', 36, QFont.Bold))
        title_label.setStyleSheet("color: white;")  # White text color
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Add vertical spacer to push content down
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Individual's Name and Add User buttons
        individual_layout = QVBoxLayout()
        individual_layout.setSpacing(20)  # Increase vertical spacing between items

        name_label = QLabel("Individual's Name:", self)
        name_label.setFont(QFont('Arial', 20, QFont.Bold))
        name_label.setStyleSheet("color: black;")
        name_label.setAlignment(Qt.AlignCenter)
        individual_layout.addWidget(name_label)

        individual_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        name_button = self.create_button("John Doe", 0, 50, bg_color="white", text_color="black")  # Changed to "John Doe" as a placeholder
        name_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        individual_layout.addWidget(name_button, alignment=Qt.AlignCenter)

        individual_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Custom Add User button
        add_user_button = CustomAddUserButton(self)
        individual_layout.addWidget(add_user_button, alignment=Qt.AlignCenter)

        main_layout.addLayout(individual_layout)

        # Add vertical spacer to push content up
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Help button at the bottom left with padding
        help_button_layout = QHBoxLayout()
        help_button_layout.setContentsMargins(20, 0, 0, 20)  # Padding for bottom-left corner
        help_button = self.create_button('Help', 120, 50, bg_color="white", text_color="#39687C")
        help_button_layout.addWidget(help_button, alignment=Qt.AlignLeft)
        main_layout.addLayout(help_button_layout)

    def create_button(self, text, width, height, bg_color, text_color):
        button = QPushButton(text, self)
        if width > 0:
            button.setFixedWidth(width)
        button.setFixedHeight(height)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border-radius: 25px;
                font-size: 18px;
                font-weight: bold;
                padding: 0 20px;
            }}
            QPushButton:hover {{
                background-color: #A9A9A9;
            }}
        """)
        button.clicked.connect(lambda: print(f"{text} button clicked"))  # Placeholder event listener
        return button

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OverviewScreen()
    window.show()
    sys.exit(app.exec_())