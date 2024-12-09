import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
                             QGraphicsDropShadowEffect, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox)
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
        container.setFixedSize(1120, 680)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 10)
        container.setGraphicsEffect(shadow)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(40, 20, 40, 20)
        container_layout.setSpacing(20)  # Increased from 15 to 20

        title = QLabel("Patients List")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #71B89A;")
        title.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(title)
        container_layout.addSpacing(20) #Added spacing

        self.user_table = QTableWidget()
        self.user_table.setColumnCount(3)
        self.user_table.setHorizontalHeaderLabels(["Name", "Email", "User ID"])
        self.user_table.setStyleSheet("""
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
            QHeaderView::section:first {
                border-top-left-radius: 10px;
            }
            QHeaderView::section:last {
                border-top-right-radius: 10px;
            }
            QTableWidget::item {
                color: black;
            }
            QScrollBar:vertical {
                border: none;
                background: #F0F0F0;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #71B89A;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.user_table.verticalHeader().setVisible(False)
        self.user_table.setFixedHeight(500)  # Increased from 450 to 500
        container_layout.addWidget(self.user_table)
        container_layout.addSpacing(20) #Added spacing
        self.load_users()

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
        main_layout.setAlignment(Qt.AlignCenter)

    def submit_form(self):
        # This method would typically handle form submission
        # Since we've removed the input fields, we'll just show a message
        QMessageBox.information(self, "Submit", "Form submission functionality to be implemented.")

    def cancel_form(self):
        if self.main_window:
            self.main_window.show_login_page()

    def button_clicked(self):
        sender = self.sender()
        if sender.text() == "Add User" and self.main_window:
            self.main_window.show_session_overview()
        else:
            print(f"{sender.text()} button clicked")

    def load_users(self):
        try:
            response = requests.get("http://127.0.0.1:8081/getusers")
            if response.status_code == 200:
                data = response.json()
                users = data.get('users', [])
                print("Raw user data:", users)  # Debug print

                # Clear existing rows
                self.user_table.setRowCount(0)

                # Add new rows
                for user in users:
                    row_position = self.user_table.rowCount()
                    self.user_table.insertRow(row_position)

                    # Combine first and last name
                    full_name = f"{user['first_name']} {user['last_name']}"

                    # Get user ID
                    user_id = f"{user['user_id']}"

                    # Set items in the table
                    self.user_table.setItem(row_position, 0, QTableWidgetItem(full_name))
                    self.user_table.setItem(row_position, 1, QTableWidgetItem(user['email']))
                    self.user_table.setItem(row_position, 2, QTableWidgetItem(user_id))

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to load users: {str(e)}")
        except KeyError as e:
            QMessageBox.critical(self, "Error", f"Unexpected data format: {str(e)}")
            print("Error details:", str(e))  # Debug print

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = QWidget()
    registration_form = RegistrationForm(main_window)
    registration_form.show()
    sys.exit(app.exec_())

