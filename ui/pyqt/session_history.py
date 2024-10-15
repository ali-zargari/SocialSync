import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QLabel, QFrame, QHBoxLayout, QScrollArea)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, QSize


class HistoryPage(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("History")
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
        content = QScrollArea()
        content.setWidgetResizable(True)
        content.setStyleSheet("background-color: transparent; border: none;")
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.setSpacing(20)

        sessions_label = QLabel("Sessions:")
        sessions_label.setStyleSheet("color: white; font-size: 32px; font-weight: bold;")
        content_layout.addWidget(sessions_label)

        # Sample session data
        sessions = [
            {"name": "John Doe", "date": "02-20-2024", "time_elapsed": "2hrs 30mins"},
            {"name": "John Doe", "date": "03-25-2024", "time_elapsed": "30mins"},
            {"name": "Jane Smith", "date": "04-01-2024", "time_elapsed": "1hr 45mins"},
            {"name": "Alice Johnson", "date": "04-05-2024", "time_elapsed": "45mins"},
            {"name": "Bob Williams", "date": "04-10-2024", "time_elapsed": "3hrs 15mins"},
        ]

        for session in sessions:
            session_widget = self.create_session_widget(session)
            content_layout.addWidget(session_widget)

        content_layout.addStretch(1)
        content.setWidget(content_widget)

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
        button.setFixedSize(120, 40)
        button.clicked.connect(lambda: print(f"{text} button clicked"))
        return button

    def create_session_widget(self, session):
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 10px;
            }
        """)
        layout = QHBoxLayout(widget)

        name_date = QLabel(f"{session['name']} {session['date']}")
        name_date.setStyleSheet("color: white; font-size: 18px;")

        time_elapsed = QLabel(f"Time Elapsed: {session['time_elapsed']}")
        time_elapsed.setStyleSheet("color: white; font-size: 18px;")

        layout.addWidget(name_date)
        layout.addStretch(1)
        layout.addWidget(time_elapsed)

        return widget


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HistoryPage()
    window.show()
    sys.exit(app.exec_())