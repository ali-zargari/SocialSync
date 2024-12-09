import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QRadioButton,
                             QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QGraphicsDropShadowEffect, QMessageBox)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #71B89A;
                color: white;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #5A9A7F;
            }
        """)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.shadow.setOffset(0, 5)
        self.setGraphicsEffect(self.shadow)

class RegistrationForm(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Registration')
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #71B89A;")

        main_layout = QVBoxLayout(self)

        container = QWidget(self)
        container.setStyleSheet("""
            background-color: white;
            border-radius: 40px;
        """)
        container.setFixedSize(1120, 620)  # Reduced height since table is removed
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 10)
        container.setGraphicsEffect(shadow)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(40, 30, 40, 30)
        container_layout.setSpacing(20)

        # Header Section
        title = QLabel("ASD Practitioner Registration")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #71B89A;")
        title.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(title)

        # Form Section
        form_layout = QGridLayout()
        form_layout.setVerticalSpacing(20)
        form_layout.setHorizontalSpacing(15)

        fields = [
            ("First Name:", 0, 0, 1), ("Address:", 0, 3, 4),
            ("Middle Name:", 1, 0, 1), ("City:", 1, 3, 4),
            ("Last Name:", 2, 0, 1), ("Zip:", 2, 3, 4),
            ("Date of Birth:", 3, 0, 1), ("State:", 3, 3, 4),
            ("Email Address:", 4, 0, 1), ("Country:", 4, 3, 4),
            ("Password:", 5, 0, 1),
            ("Phone Number:", 6, 0, 1), ("Gender:", 6, 3, 4),
        ]

        self.input_fields = {}

        for label_text, row, col, input_col in fields:
            label = QLabel(label_text)
            label.setStyleSheet("""
                color: #23465A;
                font-size: 14px;
                padding-right: 10px;
                font-weight: bold;
            """)
            label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            form_layout.addWidget(label, row, col)

            if label_text == "Gender:":
                gender_layout = QHBoxLayout()
                self.female_radio = QRadioButton("Female")
                self.male_radio = QRadioButton("Male")
                self.female_radio.setStyleSheet("""
                    QRadioButton {
                        color: #23465A;
                        font-size: 14px;
                        spacing: 8px;
                    }
                    QRadioButton::indicator {
                        width: 18px;
                        height: 18px;
                    }
                    QRadioButton::indicator:checked {
                        background-color: #71B89A;
                        border: 2px solid #71B89A;
                        border-radius: 9px;
                    }
                """)
                self.male_radio.setStyleSheet(self.female_radio.styleSheet())
                gender_layout.addWidget(self.female_radio)
                gender_layout.addWidget(self.male_radio)
                gender_layout.addStretch()
                form_layout.addLayout(gender_layout, row, input_col)
            else:
                input_field = QLineEdit()
                input_field.setStyleSheet("""
                    QLineEdit {
                        background-color: #F0F0F0;
                        border: 2px solid transparent;
                        border-radius: 20px;
                        padding: 10px 15px;
                        font-size: 14px;
                        color: #23465A;
                    }
                    QLineEdit:focus {
                        border: 2px solid #71B89A;
                        background-color: white;
                    }
                """)
                input_field.setFixedHeight(40)
                form_layout.addWidget(input_field, row, input_col)
                self.input_fields[label_text.replace(":", "").lower().replace(" ", "_")] = input_field

        container_layout.addLayout(form_layout)

        # Button Section
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addStretch(1)

        cancel_btn = AnimatedButton("Cancel")
        submit_btn = AnimatedButton("Submit")

        for btn in [cancel_btn, submit_btn]:
            btn.setFixedSize(200, 50)
            if btn == submit_btn:
                btn.clicked.connect(self.submit_form)
            elif btn == cancel_btn:
                btn.clicked.connect(self.cancel_form)
            button_layout.addWidget(btn)

        button_layout.addStretch(1)
        container_layout.addLayout(button_layout)
        main_layout.addWidget(container, alignment=Qt.AlignCenter)

    def submit_form(self):
        # Get input from the fields
        data = {
            "first_name": self.input_fields['first_name'].text(),
            "middle_name": self.input_fields['middle_name'].text(),
            "last_name": self.input_fields['last_name'].text(),
            "date_of_birth": self.input_fields['date_of_birth'].text(),
            "email": self.input_fields['email_address'].text(),
            "password": self.input_fields['password'].text(),
            "phone_number": self.input_fields['phone_number'].text(),
            "address": self.input_fields['address'].text(),
            "city": self.input_fields['city'].text(),
            "zip_code": self.input_fields['zip'].text(),
            "state": self.input_fields['state'].text(),
            "country": self.input_fields['country'].text(),
            "gender": 'Female' if self.female_radio.isChecked() else 'Male' if self.male_radio.isChecked() else ''
        }

        try:
            response = requests.post("http://127.0.0.1:8081/register", json=data)
            response.raise_for_status()

            if response.status_code == 201:
                QMessageBox.information(self, "Success", "User registered successfully!")
                self.main_window.show_practitioner_landing_page()
            else:
                QMessageBox.warning(self, "Registration Failed", "Invalid data or server error.")

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def cancel_form(self):
        if self.main_window:
            self.main_window.show_new_user_flow()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = QWidget()
    registration_form = RegistrationForm(main_window)
    registration_form.show()
    sys.exit(app.exec_())

