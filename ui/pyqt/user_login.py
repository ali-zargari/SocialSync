from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap



class LoginPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window  # Store reference to MainWindow
        self.initUI()

    def initUI(self):
        self.setWindowTitle('SocialSync Care')
        self.setFixedSize(1280, 720)
        self.setStyleSheet("background-color: #71B89A;")

        # Container for login elements
        container = QFrame(self)
        container.setFixedSize(700, 700)
        container.setStyleSheet("background-color: #FFFFFF; border-radius: 20px;")
        container.move(290, 10)

        layout = QVBoxLayout(container)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Logo placeholder
        logoLabel = QLabel()  # Create a QLabel without specifying 'self'
        pixmap = QPixmap("A:\\OneDrive\\Documents\\Ali's Documents\\SE_\\CMPE 195B Senior Project II\\SocialSync\\ui\\PyQt\\images\\v20_308.png")

        # Check if the image was loaded successfully
        if pixmap.isNull():
            print("Failed to load image: images/v20_308.png")

        # Scale the pixmap to a smaller size, keeping the aspect ratio
        scaled_pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        logoLabel.setPixmap(scaled_pixmap)  # Set the scaled pixmap onto the label
        logoLabel.setAlignment(Qt.AlignCenter)  # Align the label to center
        layout.addWidget(logoLabel)  # Add the label to the layout within the container


        # Title
        titleLabel = QLabel('SocialSync Care', self)
        titleLabel.setFont(QFont('Arial', 24))
        titleLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(titleLabel)

        # Username Field
        self.usernameLineEdit = QLineEdit()
        self.usernameLineEdit.setPlaceholderText("Username")
        self.setupLineEdit(self.usernameLineEdit)
        layout.addWidget(self.usernameLineEdit)

        # Password Field
        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setPlaceholderText("Password")
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        self.setupLineEdit(self.passwordLineEdit)
        layout.addWidget(self.passwordLineEdit)

        # Sign In Button
        signInButton = QPushButton("Sign In")
        self.setupButton(signInButton, "#00897B", "#00695C")
        signInButton.clicked.connect(self.go_to_dashboard)
        layout.addWidget(signInButton)

        # Forgot Password Link
        forgotPassLabel = QLabel("Forgot Password?")
        forgotPassLabel.setFont(QFont('Arial', 12))
        forgotPassLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(forgotPassLabel)

    def setupLineEdit(self, lineEdit):
        lineEdit.setFont(QFont('Arial', 16))
        lineEdit.setStyleSheet("QLineEdit { border: 2px solid #B2DFDB; border-radius: 10px; padding: 5px; background-color: #FFFFFF; }")

    def setupButton(self, button, color, hoverColor):
        button.setFont(QFont('Arial', 14))
        button.setStyleSheet(f"QPushButton {{ background-color: {color}; color: black; border-radius: 10px; padding: 10px; }}"
                             f"QPushButton:hover {{ background-color: {hoverColor}; }}")

    def go_to_dashboard(self):
        self.main_window.show_profile_page()  # Use the main_window reference

    def go_to_register(self):
        self.main_window.show_register_page()  # Use the main_window reference
