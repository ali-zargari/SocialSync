import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QRadioButton,
                             QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame)
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt

class RegistrationForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window properties
        self.setWindowTitle('Registration')
        self.setGeometry(100, 100, 1000, 800)
        self.setStyleSheet("background-color: #71B79A;")

        # Load custom font
        font_id = QFontDatabase.addApplicationFont("path/to/JosefinSans-Regular.ttf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            font_family = "Arial"

        # Create main layout
        main_layout = QVBoxLayout(self)

        # Create white background
        white_bg = QFrame(self)
        white_bg.setStyleSheet("""
            background-color: white;
            border-radius: 30px;
            padding: 20px;
        """)

        # Create grid layout for form elements
        grid = QGridLayout(white_bg)
        grid.setVerticalSpacing(10)  # Reduced vertical spacing
        grid.setHorizontalSpacing(20)

        # Add title
        title = QLabel("Registration")
        title.setFont(QFont(font_family, 36, QFont.Bold))
        title.setStyleSheet("color: #71B89A; margin-bottom: 20px;")
        grid.addWidget(title, 0, 0, 1, 4, Qt.AlignHCenter)

        # Create form fields
        fields = [
            ("First Name:", 1, 0), ("Address:", 1, 2),
            ("Middle Name:", 2, 0), ("City:", 2, 2),
            ("Last Name:", 3, 0), ("Zip:", 3, 2),
            ("Date of Birth:", 4, 0), ("State:", 4, 2),
            ("Email Address:", 5, 0), ("Country:", 5, 2),
            ("Phone Number:", 6, 0), ("Sex:", 6, 2),
            ("Password:", 7, 0), ("Confirm Password:", 7, 2),
        ]

        for label_text, row, col in fields:
            label = QLabel(label_text)
            label.setFont(QFont(font_family, 12))
            label.setStyleSheet("color: #23465A;")
            grid.addWidget(label, row, col)

            if label_text == "Sex:":
                sex_layout = QHBoxLayout()
                female_radio = QRadioButton("Female")
                male_radio = QRadioButton("Male")
                female_radio.setFont(QFont(font_family, 12))
                male_radio.setFont(QFont(font_family, 12))
                female_radio.setStyleSheet("color: black;")
                male_radio.setStyleSheet("color: black;")
                sex_layout.addWidget(female_radio)
                sex_layout.addWidget(male_radio)
                sex_layout.addStretch()
                grid.addLayout(sex_layout, row, col + 1)
            else:
                input_field = QLineEdit()
                input_field.setStyleSheet("""
                    background-color: #F0F0F0;
                    border: 1px solid #D0D0D0;
                    border-radius: 5px;
                    padding: 5px;
                    font-size: 14px;
                    color: black;
                """)
                if "Password" in label_text:
                    input_field.setEchoMode(QLineEdit.Password)
                grid.addWidget(input_field, row, col + 1)

        # Add buttons in a column
        button_layout = QVBoxLayout()
        buttons = ["Submit", "Cancel"]  # Removed "Add User" button
        for button_text in buttons:
            button = QPushButton(button_text)
            button.setFont(QFont(font_family, 14))
            button.setStyleSheet("""
                QPushButton {
                    background-color: #71B89A;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 10px;
                    min-width: 200px;
                    margin: 5px 0;
                }
                QPushButton:hover {
                    background-color: #5DA688;
                }
            """)
            button.clicked.connect(self.button_clicked)
            button_layout.addWidget(button)

        grid.addLayout(button_layout, 8, 0, 2, 4, Qt.AlignCenter)  # Adjusted row span

        # Center the white background
        main_layout.addWidget(white_bg, alignment=Qt.AlignCenter)

    def button_clicked(self):
        sender = self.sender()
        print(f"{sender.text()} button clicked")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RegistrationForm()
    ex.show()
    sys.exit(app.exec_())