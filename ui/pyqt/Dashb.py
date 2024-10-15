import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QFrame, QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap


class CustomPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Custom PyQt Design')
        self.setFixedSize(1280, 1024)  # Set fixed size based on CSS

        # Setting up the main background style
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(113, 183, 154, 1);
            }
        """)

        # Container for top section
        top_container = QFrame(self)
        top_container.setFixedSize(self.width(), 141)  # 100% width, 141px height
        top_container.move(0, 0)
        top_container.setStyleSheet("background-color: rgba(255,255,255,1); border: 1px solid rgba(0,0,0,1);")

        # Home label - Minor adjustment
        home_label = QLabel('Home', top_container)
        home_label.setFont(QFont('Josefin Sans', 70, QFont.Bold))
        home_label.setStyleSheet("color: rgba(0,0,0,1); background-color: rgba(178,255,209,1);")
        home_label.setFixedSize(220, 100)  # Reduce size for better alignment
        home_label.move(20, 20)  # Adjusted position for better placement

        # Profile, History, and Sign Out buttons - Adjusted sizes and positions
        self.create_top_button('Profile', 800, 45, 90, 40)  # Adjusted position for spacing
        self.create_top_button('History', 910, 45, 90, 40)
        self.create_top_button('Help', 1020, 45, 90, 40)  # New Help button in between History and Sign Out
        self.create_top_button('Sign Out', 1130, 45, 90, 40)

        # Welcome label - Adjusted
        welcome_label = QLabel('Welcome, John Doe', self)
        welcome_label.setFont(QFont('Josefin Sans', 48, QFont.Bold))  # Reduced font size for better fit
        welcome_label.setStyleSheet("color: rgba(255,255,255,1);")
        welcome_label.move(150, 200)  # Slightly moved for better alignment

        # Middle container for "Start" button - Adjusted position and size
        middle_container = QFrame(self)
        middle_container.setFixedSize(900, 400)  # Adjust height to accommodate the larger button
        middle_container.move(190, 400)  # Adjust position
        middle_container.setStyleSheet("""
            background-color: rgba(178,255,209,1);
            border: 1px solid rgba(0,0,0,1);
            border-radius: 100px;  # Adjusted for rounded effect
            box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
        """)

        # Start button - Increase size 3x
        start_button = QPushButton('Start', middle_container)
        start_button.setFont(QFont('Josefin Sans', 96, QFont.Bold))  # Increase font size
        start_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255,255,255,1);
                color: rgba(0,0,0,1);
                border: 1px solid rgba(0,0,0,1);
                border-radius: 40px;
            }
            QPushButton:hover {
                background-color: rgba(240,240,240,1);
            }
        """)
        start_button.setFixedSize(750, 300)  # 3x the previous size (250x100)
        start_button.move((middle_container.width() - start_button.width()) // 2, (middle_container.height() - start_button.height()) // 2)  # Center within the container

        # Adding image placeholder - Adjusted size and position
        logo_container = QLabel(self)
        logo_pixmap = QPixmap('images/v20_308.png')  # Updated path for the provided image
        logo_container.setPixmap(logo_pixmap)
        logo_container.setScaledContents(True)  # Ensure the image scales correctly
        logo_container.setFixedSize(100, 100)  # Adjusted size for better proportion
        logo_container.move(50, 150)  # Adjusted position for better alignment

    def create_top_button(self, text, x, y, width, height):
        button = QPushButton(text, self)
        button.setFixedSize(width, height)
        button.move(x, y)
        button.setFont(QFont('Josefin Sans', 16, QFont.Bold))
        button.setStyleSheet("""
            QPushButton {
                background-color: rgba(113,184,154,1);
                color: rgba(255,255,255,1);
                border: 1px solid rgba(35,70,90,1);
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: rgba(143,204,174,1);
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = CustomPage()
    ex.show()
    sys.exit(app.exec_())
