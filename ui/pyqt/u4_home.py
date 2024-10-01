import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSlider, QFrame, \
    QStyleOptionSlider, QStyle
from PyQt5.QtGui import QFont, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QRectF, pyqtSignal


class CustomSwitch(QWidget):
    stateChanged = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 30)
        self._is_on = True  # Default state is on

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#71B89A" if self._is_on else "#FF6B6B"))  # Green when on, red when off
        painter.drawRoundedRect(0, 0, 60, 30, 15, 15)

        painter.setBrush(QColor("#4F5D75"))  # Same color as arrow buttons
        painter.drawEllipse(30 if self._is_on else 0, 0, 30, 30)

    def mousePressEvent(self, event):
        self.toggle()

    def toggle(self):
        self._is_on = not self._is_on
        self.update()
        self.stateChanged.emit(self._is_on)

    def is_on(self):
        return self._is_on

    def set_state(self, state):
        if self._is_on != state:
            self._is_on = state
            self.update()
            self.stateChanged.emit(self._is_on)


class CustomButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(50)
        self.setCursor(Qt.PointingHandCursor)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(self.palette().button().color()))
        painter.drawRoundedRect(self.rect(), 25, 25)

        painter.setPen(QColor(self.palette().buttonText().color()))
        painter.setFont(QFont('Arial', 20, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())


class CustomSlider(QSlider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedHeight(30)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw background
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#D3D3D3"))
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 15, 15)

        # Draw filled part
        width = int((self.value() - self.minimum()) / (self.maximum() - self.minimum()) * self.width())
        if width > 0:
            painter.setBrush(QColor("#6AAFA2"))
            painter.drawRoundedRect(0, 0, width + 15, self.height(), 15, 15)  # Extend by handle radius

        # Draw handle
        painter.setBrush(QColor("#4F5D75"))
        handle_position = int((self.value() - self.minimum()) / (self.maximum() - self.minimum()) * (self.width() - 30))
        painter.drawEllipse(handle_position, 0, 30, 30)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            val = self.pixelPosToRangeValue(event.pos())
            self.setValue(val)
            event.accept()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        val = self.pixelPosToRangeValue(event.pos())
        self.setValue(val)
        event.accept()
        super().mouseMoveEvent(event)

    def pixelPosToRangeValue(self, pos):
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)
        gr = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderGroove, self)
        sr = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderHandle, self)

        if self.orientation() == Qt.Horizontal:
            sliderLength = sr.width()
            sliderMin = gr.x()
            sliderMax = gr.right() - sliderLength + 1
        else:
            sliderLength = sr.height()
            sliderMin = gr.y()
            sliderMax = gr.bottom() - sliderLength + 1

        pr = pos - sr.center() + sr.topLeft()
        p = pr.x() if self.orientation() == Qt.Horizontal else pr.y()
        return QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), p - sliderMin,
                                              sliderMax - sliderMin, opt.upsideDown)
class VocalVisualSettingsScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #71B89A;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # White rounded rectangle
        white_frame = QFrame(self)
        white_frame.setFixedWidth(600)
        white_frame.setStyleSheet("""
            background-color: white;
            border-radius: 30px;
        """)
        white_layout = QVBoxLayout(white_frame)
        white_layout.setSpacing(20)
        white_layout.setContentsMargins(40, 40, 40, 40)

        # Title
        title = QLabel("Vocal and Visual Settings")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 31px; color: #6AAFA2; font-weight: bold;")
        white_layout.addWidget(title)

        # Visual Overlay
        visual_layout = QHBoxLayout()
        visual_label = QLabel("Visual Overlay")
        visual_label.setStyleSheet("font-size: 20px; color: #2F4858; font-weight: bold;")
        self.visual_switch = CustomSwitch()
        self.visual_switch.stateChanged.connect(self.on_visual_overlay_changed)
        visual_layout.addWidget(visual_label)
        visual_layout.addStretch()
        visual_layout.addWidget(self.visual_switch)
        white_layout.addLayout(visual_layout)

        # Voice Option
        voice_layout = QHBoxLayout()
        voice_label = QLabel("Voice Option")
        voice_label.setStyleSheet("font-size: 20px; color: #2F4858; font-weight: bold;")
        self.voice_switch = CustomSwitch()
        self.voice_switch.stateChanged.connect(self.on_voice_option_changed)
        voice_layout.addWidget(voice_label)
        voice_layout.addStretch()
        voice_layout.addWidget(self.voice_switch)
        white_layout.addLayout(voice_layout)

        # Voice Volume
        volume_layout = QVBoxLayout()
        self.volume_label = QLabel("Voice Volume: 0%")
        self.volume_label.setStyleSheet("font-size: 20px; color: #2F4858; font-weight: bold;")
        self.volume_label.setAlignment(Qt.AlignCenter)
        volume_layout.addWidget(self.volume_label)

        slider_layout = QHBoxLayout()
        self.volume_slider = CustomSlider(Qt.Horizontal)
        self.volume_slider.setFixedSize(400, 30)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(0)
        self.volume_slider.valueChanged.connect(self.update_volume)
        slider_layout.addWidget(self.volume_slider)

        up_down_layout = QVBoxLayout()
        up_button = CustomButton("▲")
        up_button.setFixedSize(40, 40)
        up_button.setStyleSheet("background-color: #4F5D75; color: white; border-radius: 20px;")
        up_button.clicked.connect(self.increase_volume)
        down_button = CustomButton("▼")
        down_button.setFixedSize(40, 40)
        down_button.setStyleSheet("background-color: #4F5D75; color: white; border-radius: 20px;")
        down_button.clicked.connect(self.decrease_volume)
        up_down_layout.addWidget(up_button)
        up_down_layout.addWidget(down_button)

        slider_layout.addLayout(up_down_layout)
        volume_layout.addLayout(slider_layout)
        white_layout.addLayout(volume_layout)

        white_layout.addStretch(1)

        # Confirm and Skip buttons
        confirm_button = CustomButton("Confirm")
        confirm_button.setFixedSize(200, 50)
        confirm_button.setStyleSheet("background-color: #71B89A; color: white; font-size: 20px; font-weight: bold;")
        confirm_button.clicked.connect(self.on_confirm_clicked)
        white_layout.addWidget(confirm_button, alignment=Qt.AlignCenter)

        skip_button = CustomButton("Skip")  # Changed to CustomButton
        skip_button.setFixedSize(200, 50)
        skip_button.setStyleSheet(
            "background-color: transparent; color: #2F4858; font-size: 20px; font-weight: bold; border: none;")
        skip_button.clicked.connect(self.on_skip_clicked)
        white_layout.addWidget(skip_button, alignment=Qt.AlignCenter)

        main_layout.addWidget(white_frame, alignment=Qt.AlignCenter)

    def on_visual_overlay_changed(self, state):
        print(f"Visual Overlay {'enabled' if state else 'disabled'}")

    def on_voice_option_changed(self, state):
        print(f"Voice Option {'enabled' if state else 'disabled'}")

    def update_volume(self, value):
        self.volume_label.setText(f"Voice Volume: {value}%")

    def increase_volume(self):
        current_value = self.volume_slider.value()
        self.volume_slider.setValue(min(current_value + 1, 100))

    def decrease_volume(self):
        current_value = self.volume_slider.value()
        self.volume_slider.setValue(max(current_value - 1, 0))

    def on_confirm_clicked(self):
        print("Confirm button clicked")

    def on_skip_clicked(self):
        print("Skip button clicked")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VocalVisualSettingsScreen()
    window.show()
    sys.exit(app.exec_())