import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QRadioButton,
                             QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QGraphicsDropShadowEffect, QTableWidget, QTableWidgetItem,
                             QHeaderView)
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
        self.main_window = main_window  # Store reference to the main window
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
        container.setFixedSize(1120, 680)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 10)
        container.setGraphicsEffect(shadow)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(40, 30, 40, 30)
        container_layout.setSpacing(20)

        title = QLabel("Registration")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #71B89A; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(title)

        form_layout = QGridLayout()
        form_layout.setVerticalSpacing(15)
        form_layout.setHorizontalSpacing(10)

        # Form fields setup
        fields = [
            ("First Name:", 0, 0, 1), ("Address:", 0, 3, 4),
            ("Middle Name:", 1, 0, 1), ("City:", 1, 3, 4),
            ("Last Name:", 2, 0, 1), ("Zip:", 2, 3, 4),
            ("Date of Birth:", 3, 0, 1), ("State:", 3, 3, 4),
            ("Email Address:", 4, 0, 1), ("Country:", 4, 3, 4),
            ("Phone Number:", 5, 0, 1), ("Gender:", 5, 3, 4),
        ]

        for label_text, row, col, input_col in fields:
            label = QLabel(label_text)
            label.setStyleSheet("color: #23465A; font-size: 14px; padding-right: 10px;")
            label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            form_layout.addWidget(label, row, col)

            if label_text == "Gender:":
                gender_layout = QHBoxLayout()
                female_radio = QRadioButton("Female")
                male_radio = QRadioButton("Male")
                female_radio.setStyleSheet("color: #23465A; font-size: 14px;")
                male_radio.setStyleSheet("color: #23465A; font-size: 14px;")
                gender_layout.addWidget(female_radio)
                gender_layout.addWidget(male_radio)
                gender_layout.addStretch()
                form_layout.addLayout(gender_layout, row, input_col)
            else:
                input_field = QLineEdit()
                input_field.setStyleSheet("""
                    background-color: #F0F0F0;
                    border: none;
                    border-radius: 20px;
                    padding: 10px 15px;
                    font-size: 14px;
                    color: #555;
                """)
                input_field.setFixedHeight(40)
                form_layout.addWidget(input_field, row, input_col)

        container_layout.addLayout(form_layout)

        # User table setup
        user_table = QTableWidget()
        user_table.setColumnCount(3)
        user_table.setHorizontalHeaderLabels(["Name", "Password", "Email"])
        user_table.setStyleSheet("""
            QTableWidget {
                background-color: #F0F0F0;
                border: none;
                border-radius: 10px;
            }
            QHeaderView::section {
                background-color: #71B89A;
                color: white;
                font-weight: bold;
                border: none;
                padding: 8px;
            }
            QTableWidget::item {
                color: black;
            }
        """)
        user_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        user_table.verticalHeader().setVisible(False)
        user_table.setFixedHeight(200)

        sample_data = [
            ("John Doe", "Password123", "johndoe@gmail.com"),
            ("Jane Smith", "SecurePass456", "janesmith@gmail.com"),
            ("Bob Johnson", "BobPass789", "bob.johnson@gmail.com"),
        ]

        for row, (name, password, email) in enumerate(sample_data):
            user_table.insertRow(row)
            user_table.setItem(row, 0, QTableWidgetItem(name))
            user_table.setItem(row, 1, QTableWidgetItem(password))
            user_table.setItem(row, 2, QTableWidgetItem(email))

        container_layout.addWidget(user_table)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        add_user_btn = AnimatedButton("Add User")
        cancel_btn = AnimatedButton("Cancel")
        submit_btn = AnimatedButton("Submit")

        for btn in [add_user_btn, cancel_btn, submit_btn]:
            btn.setFixedSize(200, 50)
            if btn == submit_btn:
                btn.clicked.connect(self.submit_form)
            elif btn == cancel_btn:
                btn.clicked.connect(self.cancel_form)
            else:
                btn.clicked.connect(self.button_clicked)
            button_layout.addWidget(btn)

        container_layout.addLayout(button_layout)
        main_layout.addWidget(container, alignment=Qt.AlignCenter)

    def submit_form(self):
        """Submit the form and navigate to the profile page in the main window."""
        self.main_window.show_profile_page()

    def cancel_form(self):
        """Cancel the form and navigate back to the login page in the main window."""
        if self.main_window:
            self.main_window.show_login_page()

    def button_clicked(self):
        sender = self.sender()
        if sender.text() == "Add User" and self.main_window:
            self.main_window.show_register_patient()  # Navigate to P5 page
        else:
            print(f"{sender.text()} button clicked")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = QWidget()  # Placeholder for the actual MainWindow instance with show_profile_page
    registration_form = RegistrationForm(main_window)
    registration_form.show()
    sys.exit(app.exec_())
