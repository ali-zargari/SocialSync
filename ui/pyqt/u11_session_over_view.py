import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor, QPen, QFontMetrics
from PyQt5.QtCore import Qt, QRectF
import os
class CustomButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.setFixedHeight(50)
        self.setCursor(Qt.PointingHandCursor)
        self.adjustSize()

    def adjustSize(self):
        font = QFont('Arial', 18, QFont.Bold)
        metrics = QFontMetrics(font)
        text_width = metrics.width(self.text())
        self.setFixedWidth(text_width + 40)  # Add some padding

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw rounded rectangle
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor('white'))
        painter.drawRoundedRect(self.rect(), 25, 25)

        # Draw text
        painter.setPen(QColor('black'))
        painter.setFont(QFont('Arial', 18, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())

class CircleTextButton(QWidget):
    def __init__(self, text, circle_text, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setCircleText(circle_text)
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Create circular background with sign
        self.circle_label = QLabel(self)
        self.circle_label.setFixedSize(40, 40)
        self.circle_label.setStyleSheet("""
            background-color: white;
            border-radius: 20px;
        """)

        # Add sign to the circular background
        self.sign_label = QLabel(self.circle_text, self.circle_label)
        self.sign_label.setAlignment(Qt.AlignCenter)
        self.sign_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: black;
        """)
        self.sign_label.setGeometry(0, 0, 40, 40)

        # Add text
        self.text_label = QLabel(self.text, self)
        self.text_label.setStyleSheet("""
            color: black;
            font-size: 18px;
            font-weight: bold;
        """)

        layout.addWidget(self.circle_label)
        layout.addWidget(self.text_label)
        layout.addStretch()

        self.setFixedHeight(40)
        self.setCursor(Qt.PointingHandCursor)

    def setText(self, text):
        self.text = text

    def setCircleText(self, circle_text):
        self.circle_text = circle_text

    def mousePressEvent(self, event):
        print(f"{self.text} button clicked")

class OverviewScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.initUI()
        self.parent = parent

    def initUI(self):
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #71B89A;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

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
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images/v20_308.png")
        pixmap = QPixmap(image_path)
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

        # History button on the right
        history_button = self.create_button('History', 120, 50, bg_color="#71B89A", text_color="white")
        header_inner_layout.addWidget(history_button, alignment=Qt.AlignRight | Qt.AlignVCenter)
        history_button.clicked.connect(self.go_to_history)

        # Profile button on the right (now green with white text)
        profile_button = self.create_button('Profile', 120, 50, bg_color="#71B89A", text_color="white")
        header_inner_layout.addWidget(profile_button, alignment=Qt.AlignRight | Qt.AlignVCenter)
        profile_button.clicked.connect(self.go_to_profile_settings)

        header_layout.addWidget(header_container)
        main_layout.addLayout(header_layout)

        # Content
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(40, 20, 40, 20)

        # Individual's Name and Preferences
        top_section = QHBoxLayout()

        name_section = QVBoxLayout()
        name_label = QLabel("Individual's Name:", self)
        name_label.setFont(QFont('Arial', 21, QFont.Bold))
        name_label.setStyleSheet("color: white;")
        name_section.addWidget(name_label)

        name_button = CustomButton("John Doe")
        name_section.addWidget(name_button)


        top_section.addLayout(name_section)

        top_section.addStretch(1)

        preferences_section = QVBoxLayout()
        preferences_label = QLabel("Individual's Preferences:", self)
        preferences_label.setFont(QFont('Arial', 21, QFont.Bold))
        preferences_label.setStyleSheet("color: white;")
        preferences_section.addWidget(preferences_label)

        preferences_button = CustomButton("Teddy bear calms down John Doe")
        preferences_section.addWidget(preferences_button)

        add_preference_button = CircleTextButton("Add Preference", "+")
        preferences_section.addWidget(add_preference_button)

        top_section.addLayout(preferences_section)

        content_layout.addLayout(top_section)

        # Individual's Percentages
        percentages_label = QLabel("Individual's Percentages:", self)
        percentages_label.setFont(QFont('Arial', 21, QFont.Bold))
        percentages_label.setStyleSheet("color: black;")
        content_layout.addWidget(percentages_label)

        percentages_widget = QWidget(self)
        percentages_widget.setStyleSheet("background-color: white; border-radius: 25px;")
        percentages_layout = QHBoxLayout(percentages_widget)
        percentages_layout.setContentsMargins(20, 15, 20, 15)  # Reduced padding

        # Left side: percentages
        left_layout = QVBoxLayout()
        left_layout.setSpacing(10)  # Reduced spacing between items
        percentages = [
            ("Happiness:", "90%", "#4CAF50"),
            ("Sad:", "3%", "#607D8B"),
            ("Upset:", "2%", "#F44336"),
            ("Annoyed:", "1%", "#FFC107")
        ]

        for label, value, color in percentages:
            row = QHBoxLayout()
            text = QLabel(f"{label} {value}")
            text.setFont(QFont('Arial', 22, QFont.Bold))  # Increased font size by 20%
            text.setStyleSheet(f"color: {color};")
            row.addWidget(text)
            row.addStretch(1)
            left_layout.addLayout(row)

        percentages_layout.addLayout(left_layout)

        # Middle: Confidence
        confidence_layout = QVBoxLayout()
        confidence_layout.addStretch(1)
        confidence_text = QLabel("Confidence: 78%")
        confidence_text.setFont(QFont('Arial', 29, QFont.Bold))  # Increased font size by 20%
        confidence_text.setStyleSheet("color: black;")
        confidence_text.setAlignment(Qt.AlignCenter)
        confidence_layout.addWidget(confidence_text)
        confidence_layout.addStretch(1)
        percentages_layout.addLayout(confidence_layout)

        # Right side: empty space to balance the layout
        right_layout = QVBoxLayout()
        percentages_layout.addLayout(right_layout)

        content_layout.addWidget(percentages_widget)

        main_layout.addLayout(content_layout)

        # Help button
        help_button = self.create_button("Help", 132, 55, "white", "#39687C")
        help_layout = QHBoxLayout()
        help_layout.addWidget(help_button, 0, Qt.AlignLeft | Qt.AlignBottom)
        help_layout.setContentsMargins(20, 0, 0, 20)
        main_layout.addLayout(help_layout)

    def go_to_history(self):
        """Navigate to the History page (p10) in the main window."""
        if self.parent:
            self.parent.show_history_page()  # Call the parent's method to show History page

    def go_to_profile_settings(self):
        """Navigate to the Profile Settings page (p6) in the main window."""
        if self.parent:
            self.parent.show_care_profile_settings()  # Call the parent's method to show Profile Settings

    def create_button(self, text, width, height, bg_color, text_color):
        button = QPushButton(text, self)
        button.setFixedSize(width, height)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border-radius: {height // 2}px;
                font-size: 18px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #A9A9A9;
            }}
        """)
        return button

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = OverviewScreen()
    window.show()
    sys.exit(app.exec_())
