import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton)
from PyQt5.QtGui import QFont, QColor, QPainter
from PyQt5.QtCore import Qt

class RegisterPatient(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        # Main window setup
        self.setWindowTitle('Adding User')
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #71B89A;")

        # Main layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # White rounded rectangle container
        container = QWidget(self)
        container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 40px;
            }
        """)
        container.setFixedSize(500, 600)
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(20)
        container_layout.setContentsMargins(50, 50, 50, 50)

        # Title
        title = QLabel("Adding User")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 36))
        title.setStyleSheet("color: #4A90A4;")
        container_layout.addWidget(title)

        # Spacer for vertical centering
        container_layout.addStretch()

        # Input fields
        fields = ["First Name", "Last Name", "Email Address", "Password"]
        self.inputs = {}

        for field in fields:
            input_field = QLineEdit()
            input_field.setPlaceholderText(field)
            input_field.setStyleSheet("""
                QLineEdit {
                    background-color: #E0E0E0;
                    border-radius: 25px;
                    padding: 15px;
                    font-size: 18px;
                    color: #2B4865;
                    margin: 10px;
                }
                QLineEdit:focus {
                    border: 2px solid #71B89A;
                }
            """)
            input_field.setFixedSize(300, 75)
            container_layout.addWidget(input_field, alignment=Qt.AlignCenter)
            self.inputs[field] = input_field

        # Make password field secure
        self.inputs["Password"].setEchoMode(QLineEdit.Password)

        # Submit button
        submit_btn = QPushButton("Submit")
        submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #71B89A;
                color: white;
                border-radius: 25px;
                padding: 15px;
                font-size: 20px;
                font-weight: bold;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #5A9A7F;
            }
        """)
        submit_btn.setFixedSize(200, 50)
        submit_btn.clicked.connect(self.submit_form)
        container_layout.addWidget(submit_btn, alignment=Qt.AlignCenter)

        # Cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: black;
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                color: #666;
            }
        """)
        cancel_btn.clicked.connect(self.cancel_form)
        container_layout.addWidget(cancel_btn, alignment=Qt.AlignCenter)

        # Spacer for vertical centering
        container_layout.addStretch()

        # Center the container in the main window
        layout.addWidget(container, alignment=Qt.AlignCenter)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # Fill background with solid color
        painter.fillRect(self.rect(), QColor("#71B89A"))

    def submit_form(self):
        # Get form data
        form_data = {
            field: input_field.text()
            for field, input_field in self.inputs.items()
        }
        # Print form data (for debugging)
        print("Form submitted:", form_data)
        # Navigate back to register_page
        if self.parent:
            self.parent.show_register_page()
        self.close()

    def cancel_form(self):
        # Navigate back to register_page
        if self.parent:
            self.parent.show_register_page()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RegisterPatient()
    ex.show()
    sys.exit(app.exec_())