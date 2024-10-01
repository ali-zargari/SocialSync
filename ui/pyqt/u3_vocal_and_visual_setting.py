import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QSlider, QFrame)
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QPainterPath
from PyQt5.QtCore import Qt, QRectF


class CustomSwitch(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 30)
        self.isOn = True

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw background
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, 60, 30), 15, 15)
        painter.fillPath(path, QColor("#D3D3D3" if self.isOn else "#A9A9A9"))

        # Draw switch
        painter.setBrush(QColor("#4F5D75"))
        painter.drawEllipse(30 if self.isOn else 0, 0, 30, 30)

    def mousePressEvent(self, event):
        self.isOn = not self.isOn
        self.update()


class VocalVisualSettings(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #71B89A;
                color: #2F4858;
                font-family: Arial;
            }
            QLabel {
                font-size: 18px;
            }
            QPushButton {
                background-color: #9CC5B0;
                border: none;
                border-radius: 20px;
                padding: 10px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #8AB59F;
            }
        """)

        main_layout = QVBoxLayout(self)

        # White rounded rectangle
        white_frame = QFrame(self)
        white_frame.setStyleSheet("""
            background-color: white;
            border-radius: 30px;
        """)
        white_layout = QVBoxLayout(white_frame)

        # Title
        title = QLabel("Vocal and Visual Settings")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; color: #6AAFA2; font-weight: bold;")
        white_layout.addWidget(title)

        # Visual Overlay
        visual_layout = QHBoxLayout()
        visual_label = QLabel("Visual Overlay")
        visual_switch = CustomSwitch()
        visual_layout.addWidget(visual_label)
        visual_layout.addStretch()
        visual_layout.addWidget(visual_switch)
        white_layout.addLayout(visual_layout)

        # Voice Option
        voice_layout = QHBoxLayout()
        voice_label = QLabel("Voice Option")
        voice_switch = CustomSwitch()
        voice_layout.addWidget(voice_label)
        voice_layout.addStretch()
        voice_layout.addWidget(voice_switch)
        white_layout.addLayout(voice_layout)

        # Voice Volume
        volume_layout = QVBoxLayout()
        volume_label = QLabel("Voice Volume: 50%")
        volume_slider = QSlider(Qt.Horizontal)
        volume_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #D3D3D3;
                height: 30px;
                border-radius: 15px;
            }
            QSlider::handle:horizontal {
                background: #4F5D75;
                width: 30px;
                margin: -2px 0;
                border-radius: 15px;
            }
            QSlider::sub-page:horizontal {
                background: #6AAFA2;
                border-radius: 15px;
            }
        """)
        volume_slider.setValue(50)
        volume_layout.addWidget(volume_label)
        volume_layout.addWidget(volume_slider)

        up_down_layout = QVBoxLayout()
        up_button = QPushButton("▲")
        down_button = QPushButton("▼")
        up_down_layout.addWidget(up_button)
        up_down_layout.addWidget(down_button)

        volume_row = QHBoxLayout()
        volume_row.addLayout(volume_layout)
        volume_row.addLayout(up_down_layout)

        white_layout.addLayout(volume_row)

        # Confirm and Skip buttons
        confirm_button = QPushButton("Confirm")
        skip_button = QPushButton("Skip")
        skip_button.setStyleSheet("background-color: transparent; color: #2F4858;")

        white_layout.addWidget(confirm_button)
        white_layout.addWidget(skip_button)

        main_layout.addWidget(white_frame)
        self.setFixedSize(400, 500)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VocalVisualSettings()
    window.show()
    sys.exit(app.exec_())