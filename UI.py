import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Professional PyQt5 Application'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #2c3e50;")

        # Create Layout
        layout = QVBoxLayout()

        # Add Title Label
        layout.addWidget(self.createTitleLabel(), alignment=Qt.AlignCenter)
        layout.addSpacing(20)

        # Add Form Layout
        layout.addLayout(self.createFormLayout())

        # Add Submit Button
        layout.addLayout(self.createButtonLayout())

        # Add Result Label
        layout.addSpacing(20)
        layout.addWidget(self.createResultLabel(), alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def createTitleLabel(self):
        title_label = QLabel('Professional PyQt5 Interface', self)
        title_label.setFont(QFont('Helvetica', 18, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        return title_label

    def createFormLayout(self):
        form_layout = QVBoxLayout()

        # Name Input
        name_label = QLabel('Enter your name:', self)
        name_label.setFont(QFont('Helvetica', 12))
        name_label.setStyleSheet("color: white;")
        self.name_input = QLineEdit(self)
        self.name_input.setFont(QFont('Helvetica', 12))

        form_layout.addWidget(name_label)
        form_layout.addWidget(self.name_input)
        form_layout.addSpacing(10)

        # Email Input
        email_label = QLabel('Enter your email:', self)
        email_label.setFont(QFont('Helvetica', 12))
        email_label.setStyleSheet("color: white;")
        self.email_input = QLineEdit(self)
        self.email_input.setFont(QFont('Helvetica', 12))

        form_layout.addWidget(email_label)
        form_layout.addWidget(self.email_input)
        form_layout.addSpacing(20)

        return form_layout

    def createButtonLayout(self):
        submit_button = QPushButton('Submit', self)
        submit_button.setFont(QFont('Helvetica', 14))
        submit_button.setStyleSheet("background-color: #3498db; color: white; border: none; padding: 10px;")
        submit_button.clicked.connect(self.onSubmit)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(submit_button)
        button_layout.addStretch()

        return button_layout

    def createResultLabel(self):
        self.result_label = QLabel('', self)
        self.result_label.setFont(QFont('Helvetica', 12, QFont.Bold))
        self.result_label.setStyleSheet("color: #3498db;")
        return self.result_label

    def onSubmit(self):
        name = self.name_input.text()
        email = self.email_input.text()
        if name and email:
            self.result_label.setText(f'Submitted: {name}, {email}')
        else:
            self.result_label.setText('Please fill in all fields')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
