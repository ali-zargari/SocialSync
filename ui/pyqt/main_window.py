from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from ui.pyqt.guardian_login import LoginPage
from ui.pyqt.register import RegistrationForm
#from ui.pyqt.dashboard_ui import CustomPage  # Your dashboard page

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("SocialSync")
        self.setGeometry(100, 100, 1200, 800)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Add the login, register, and dashboard pages to the stack
        self.login_page = LoginPage(self)  # Pass MainWindow as reference
        self.setStyleSheet("background-color: #71B89A;")
        self.setFont(QFont("Josefin Sans", 12))


        self.register_page = RegistrationForm(self)
        #self.dashboard_page = CustomPage(self)

        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.register_page)
        #self.stacked_widget.addWidget(self.dashboard_page)

        self.stacked_widget.setCurrentWidget(self.login_page)

    def show_login_page(self):
        self.stacked_widget.setCurrentWidget(self.login_page)

    def show_register_page(self):
        self.stacked_widget.setCurrentWidget(self.register_page)

    def show_dashboard_page(self):
        self.stacked_widget.setCurrentWidget(self.dashboard_page)
