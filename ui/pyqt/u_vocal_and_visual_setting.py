import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QSlider, QCheckBox, QMainWindow
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()
        


    def initUI(self):

        # Set up main window
        self.setFixedSize(1280, 720)  # Fixed window size (16:9 aspect ratio)
        self.setStyleSheet("background-color: #71b79a;")  # Background color

        # Header with a placeholder "Logo"
        self.logo_label = QLabel('Logo', self)
        self.logo_label.setGeometry(30, 20, 100, 40)
        self.logo_label.setFont(QFont('Josefin Sans', 28, QFont.Bold))
        self.logo_label.setStyleSheet("color: white;")  # No background, no border

        # Main content container with rounded corners (white box)
        self.main_container = QWidget(self)  # Changed to QWidget to hold child widgets
        self.main_container.setGeometry(230, 50, 820, 600)  # Adjusted for the 1280x720 window
        self.main_container.setStyleSheet(
            "background-color: white; border-radius: 50px;"  # Removed the border
        )

        # Vocal and Visual Settings Title (inside white box)
        self.vocal_and_visual_label = QLabel('Vocal and Visual Settings', self.main_container)
        self.vocal_and_visual_label.setGeometry(110, 30, 600, 50)
        self.vocal_and_visual_label.setFont(QFont('Josefin Sans', 36, QFont.Bold))
        self.vocal_and_visual_label.setStyleSheet("color: #71b89a;")  # Text color only, no border

        # Visual Overlay label and switch (inside white box)
        self.visual_overlay_label = QLabel('Visual Overlay', self.main_container)
        self.visual_overlay_label.setGeometry(130, 130, 226, 40)
        self.visual_overlay_label.setFont(QFont('Josefin Sans', 28, QFont.Bold))
        self.visual_overlay_label.setStyleSheet("color: #23465a;")  # Text color only, no border

        self.visual_overlay_switch = QCheckBox(self.main_container)
        self.visual_overlay_switch.setGeometry(520, 130, 100, 40)
        self.visual_overlay_switch.setStyleSheet("""
            QCheckBox::indicator {
                width: 40px;
                height: 20px;
                border: 1px solid #000000;  # Black border by default
            }
            QCheckBox::indicator:checked {
                border: 2px solid #71b79a;  # Thicker green border when checked
            }
        """)

        # Voice Option label and switch (inside white box)
        self.voice_option_label = QLabel('Voice Option', self.main_container)
        self.voice_option_label.setGeometry(130, 210, 226, 40)
        self.voice_option_label.setFont(QFont('Josefin Sans', 28, QFont.Bold))
        self.voice_option_label.setStyleSheet("color: #23465a;")  # Text color only, no border

        self.voice_option_switch = QCheckBox(self.main_container)
        self.voice_option_switch.setGeometry(520, 210, 100, 40)
        self.voice_option_switch.setStyleSheet("""
            QCheckBox::indicator {
                width: 40px;
                height: 20px;
                border: 1px solid #000000;  # Black border by default
            }
            QCheckBox::indicator:checked {
                border: 2px solid #71b79a;  # Thicker green border when checked
            }
        """)

        # Voice Volume Label and Slider (inside white box)
        self.voice_volume_label = QLabel('Voice Volume: 50%', self.main_container)
        self.voice_volume_label.setGeometry(130, 290, 300, 40)
        self.voice_volume_label.setFont(QFont('Josefin Sans', 28, QFont.Bold))
        self.voice_volume_label.setStyleSheet("color: #23465a;")  # Text color only, no border

        self.volume_slider = QSlider(Qt.Horizontal, self.main_container)
        self.volume_slider.setGeometry(520, 290, 200, 40)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.update_volume_label)
        self.volume_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #D3D3D3;
                height: 10px;
                border-radius: 5px;
            }
            QSlider::handle:horizontal {
                background: #4682B4;
                width: 20px;
                height: 20px;
                border-radius: 10px;
            }
            QSlider::sub-page:horizontal {
                background: #4682B4;
                border-radius: 5px;
            }
        """)  # Removed border for the slider

        # Buttons: Skip and Continue (inside white box)
        self.skip_button = self.create_button('Skip', 230, 450, 120, 50, bg_color="white", text_color="black")
        self.continue_button = self.create_button('Continue', 410, 450, 200, 50, bg_color="#71b89a", text_color="white")

        self.continue_button.clicked.connect(self.parent.show_video_window)

        self.show()

    def update_volume_label(self):
        value = self.volume_slider.value()
        self.voice_volume_label.setText(f'Voice Volume: {value}%')

    def create_button(self, text, x, y, width, height, bg_color, text_color):
        button = QPushButton(text, self.main_container)  # Added to main_container
        button.setGeometry(x, y, width, height)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border-radius: 25px;
                font-size: 18px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #A9A9A9;
            }}
        """)
        button.clicked.connect(lambda: print(f"{text} button clicked"))  # Placeholder event listener
        return button


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
