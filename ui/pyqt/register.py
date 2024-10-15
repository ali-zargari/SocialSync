import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QLabel, QLineEdit, QFrame, QGridLayout,
                             QRadioButton, QHBoxLayout, QTableWidget, QTableWidgetItem)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt


class RegistrationForm(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #8FBC8F;")  # Sea Green color
        self.parent = parent

        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignCenter)

        # White rounded rectangle container
        container = QFrame()
        container.setStyleSheet("""
            background-color: white;
            border-radius: 40px;
        """)
        container.setFixedSize(800, 600)
        container_layout = QVBoxLayout(container)
        container_layout.setAlignment(Qt.AlignTop)
        container_layout.setSpacing(20)

        # Title
        title = QLabel("Registration")
        title.setStyleSheet("""
            color: #8FBC8F;
            font-size: 36px;
            font-weight: bold;
        """)
        title.setAlignment(Qt.AlignCenter)

        # Form layout
        form_layout = QGridLayout()
        form_layout.setColumnStretch(1, 1)
        form_layout.setColumnStretch(3, 1)

        # Form fields
        fields = [
            ("First Name:", 0, 0), ("Address:", 0, 2),
            ("Middle Name:", 1, 0), ("City:", 1, 2),
            ("Last Name:", 2, 0), ("Zip:", 2, 2),
            ("Date of Birth:", 3, 0), ("State:", 3, 2),
            ("Email Address:", 4, 0), ("Country:", 4, 2),
            ("Phone Number:", 5, 0), ("Gender:", 5, 2)
        ]

        for label_text, row, col in fields:
            label = QLabel(label_text)
            label.setStyleSheet("color: #20B2AA; font-size: 14px; font-weight: bold;")
            form_layout.addWidget(label, row, col)

            if label_text != "Gender:":
                line_edit = QLineEdit()
                line_edit.setStyleSheet("background-color: #D3D3D3; border: none; padding: 5px;")
                form_layout.addWidget(line_edit, row, col + 1)
            else:
                gender_layout = QHBoxLayout()
                male_radio = QRadioButton("Male")
                female_radio = QRadioButton("Female")
                gender_layout.addWidget(male_radio)
                gender_layout.addWidget(female_radio)
                form_layout.addLayout(gender_layout, row, col + 1)

        # User table
        user_table = QTableWidget(1, 3)
        user_table.setHorizontalHeaderLabels(["Name", "Password", "Email"])
        user_table.setItem(0, 0, QTableWidgetItem("John Doe"))
        user_table.setItem(0, 1, QTableWidgetItem("Password123"))
        user_table.setItem(0, 2, QTableWidgetItem("johndoe@gmail.com"))
        user_table.setStyleSheet("background-color: white; border: none;")
        user_table.horizontalHeader().setStyleSheet("font-weight: bold;")

        # Buttons
        add_user_button = self.create_button("Add User")
        submit_button = self.create_button("Submit")
        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet("""
            background-color: transparent;
            color: #8FBC8F;
            border: none;
            font-size: 16px;
        """)

        # Add widgets to container layout
        container_layout.addWidget(title)
        container_layout.addLayout(form_layout)
        container_layout.addWidget(user_table)
        container_layout.addWidget(add_user_button, alignment=Qt.AlignCenter)
        container_layout.addWidget(submit_button, alignment=Qt.AlignCenter)
        container_layout.addWidget(cancel_button, alignment=Qt.AlignCenter)

        # Add container to main layout
        main_layout.addWidget(container)

    def create_button(self, text):
        button = QPushButton(text)
        button.setStyleSheet("""
            background-color: #8FBC8F;
            color: white;
            border-radius: 20px;
            padding: 10px;
            font-size: 18px;
            font-weight: bold;
            width: 200px;
        """)
        button.clicked.connect(lambda: print(f"{text} clicked"))
        return button


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RegistrationForm()
    window.show()
    sys.exit(app.exec_())