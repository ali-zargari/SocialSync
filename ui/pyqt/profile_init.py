import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QLabel, QFrame, QSpacerItem, QSizePolicy)
from PyQt5.QtGui import QFont, QIcon, QPainter, QColor, QPen, QPixmap
from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtSvg import QSvgRenderer

class ProfileSetup(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Profile Setup")
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #8FBC8F;")

        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignCenter)

        # White rounded rectangle container
        container = QFrame()
        container.setStyleSheet("""
            background-color: white;
            border-radius: 70px;
        """)
        container.setFixedSize(800, 600)
        container_layout = QVBoxLayout(container)
        container_layout.setAlignment(Qt.AlignHCenter)
        container_layout.setSpacing(0)
        container_layout.setContentsMargins(50, 50, 50, 50)

        # Profile Setup title
        title = QLabel("Profile Setup")
        title.setStyleSheet("""
            color: #8FBC8F;
            font-size: 48px;
            font-weight: bold;
        """)
        title.setAlignment(Qt.AlignCenter)

        # Upload Photo button
        upload_photo = QPushButton()
        upload_photo.setFixedSize(120, 120)
        upload_photo.setStyleSheet("""
            background-color: #D3D3D3;
            border-radius: 60px;
        """)
        upload_photo.clicked.connect(self.upload_photo_clicked)

        # Load and set the SVG icon
        svg_renderer = QSvgRenderer("A:\\OneDrive\\Documents\\Ali's Documents\\SE_\\CMPE 195B Senior Project II\\SocialSync\\ui\\assets\\add_photo.svg")
        pixmap = QPixmap(100, 100)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        svg_renderer.render(painter)
        painter.end()
        upload_photo.setIcon(QIcon(pixmap))
        upload_photo.setIconSize(QSize(80, 80))

        upload_label = QLabel("Upload Photo")
        upload_label.setStyleSheet("""
            color: #4682B4;
            font-size: 24px;
            text-decoration: underline;
        """)
        upload_label.setAlignment(Qt.AlignCenter)

        # Vocal and Visual Settings button
        vocal_visual = QPushButton("Vocal and Visual Settings")
        vocal_visual.setStyleSheet("""
            background-color: #E0E0E0;
            color: #000080;
            border-radius: 30px;
            padding: 15px;
            font-size: 24px;
            font-weight: bold;
        """)
        vocal_visual.setFixedSize(400, 60)
        vocal_visual.clicked.connect(self.vocal_visual_clicked)

        # Next button
        next_button = QPushButton("Next")
        next_button.setStyleSheet("""
            background-color: #8FBC8F;
            color: white;
            border-radius: 30px;
            padding: 15px;
            font-size: 28px;
            font-weight: bold;
        """)
        next_button.setFixedSize(250, 60)
        next_button.clicked.connect(self.next_clicked)

        # Skip button
        skip_button = QPushButton("Skip")
        skip_button.setStyleSheet("""
            background-color: transparent;
            color: black;
            border: none;
            font-size: 24px;
        """)
        skip_button.clicked.connect(self.skip_clicked)

        # Add widgets to container layout with spacers
        container_layout.addWidget(title)
        container_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        container_layout.addWidget(upload_photo, alignment=Qt.AlignCenter)
        container_layout.addWidget(upload_label)
        container_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        container_layout.addWidget(vocal_visual, alignment=Qt.AlignCenter)
        container_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        container_layout.addWidget(next_button, alignment=Qt.AlignCenter)
        container_layout.addWidget(skip_button, alignment=Qt.AlignCenter)

        # Add container to main layout
        main_layout.addWidget(container)

    def upload_photo_clicked(self):
        print("Upload Photo clicked")

    def vocal_visual_clicked(self):
        print("Vocal and Visual Settings clicked")

    def next_clicked(self):
        print("Next clicked")

    def skip_clicked(self):
        print("Skip clicked")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor("#8FBC8F"))
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProfileSetup()
    window.show()
    sys.exit(app.exec_())