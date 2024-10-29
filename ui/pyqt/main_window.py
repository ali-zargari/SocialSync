from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QStackedWidget

from ui.pyqt.P1_U1_user_login import LoginPage
from ui.pyqt.p3_first_register import RegistrationForm
from ui.pyqt.u4_home import MainWindow as U4_PreSession
from ui.pyqt.u7_camera_working_session_dashboard import MainWindow as U7_SessionDashboard
from ui.pyqt.u2_profile_init import ProfileSetup as U2_ProfileSetup
from ui.pyqt.p10_session_history import HistoryPage as P10_HistoryPage
from ui.pyqt.u_vocal_and_visual_setting import MainWindow as U_VocalVisualSetting
from ui.pyqt.p6_care_profile_settings import MainWindow as P6_CareProfileSettings
from ui.pyqt.p5_session_overview import OverviewScreen as P5_SessionOverview

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.navigation_stack = []  # Track page history for Back navigation

        self.setWindowTitle("SocialSync")
        self.setGeometry(100, 100, 1200, 800)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.setStyleSheet("background-color: #71B89A;")
        self.setFont(QFont("Josefin Sans", 12))

        # Initialize and add the login page to the stack
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.setCurrentWidget(self.login_page)

    def navigate_to(self, page):
        """Navigate to the specified page and add the current page to history."""
        current_page = self.stacked_widget.currentWidget()
        if current_page != page:
            self.navigation_stack.append(current_page)  # Save current page
            self.stacked_widget.setCurrentWidget(page)

    def go_back(self):
        """Go back to the previous page in the navigation stack."""
        if self.navigation_stack:
            previous_page = self.navigation_stack.pop()  # Get last visited page
            self.stacked_widget.setCurrentWidget(previous_page)

    @property
    def login_page(self):
        if not hasattr(self, '_login_page'):
            self._login_page = LoginPage(self)
            self.stacked_widget.addWidget(self._login_page)
        return self._login_page

    @property
    def register_page(self):
        if not hasattr(self, '_register_page'):
            self._register_page = RegistrationForm(self)
            self.stacked_widget.addWidget(self._register_page)
        return self._register_page

    @property
    def presesh_page(self):
        if not hasattr(self, '_presesh_page'):
            self._presesh_page = U4_PreSession(self)
            self.stacked_widget.addWidget(self._presesh_page)
        return self._presesh_page

    @property
    def profile_page(self):
        if not hasattr(self, '_profile_page'):
            self._profile_page = U2_ProfileSetup(self)
            self.stacked_widget.addWidget(self._profile_page)
        return self._profile_page

    @property
    def history_page(self):
        if not hasattr(self, '_history_page'):
            self._history_page = P10_HistoryPage(self)
            self.stacked_widget.addWidget(self._history_page)
        return self._history_page

    @property
    def video_window(self):
        if not hasattr(self, '_video_window'):
            self._video_window = U7_SessionDashboard(self)
            self.stacked_widget.addWidget(self._video_window)
        return self._video_window

    @property
    def vocal_visual_setting_page(self):
        if not hasattr(self, '_vocal_visual_setting_page'):
            self._vocal_visual_setting_page = U_VocalVisualSetting(self)
            self.stacked_widget.addWidget(self._vocal_visual_setting_page)
        return self._vocal_visual_setting_page

    @property
    def care_profile_settings(self):
        if not hasattr(self, '_care_profile_settings'):
            self._care_profile_settings = P6_CareProfileSettings(self)
            self.stacked_widget.addWidget(self._care_profile_settings)
        return self._care_profile_settings

    @property
    def register_patient(self):
        if not hasattr(self, '_register_patient'):
            from ui.pyqt.p4_register_patient import RegisterPatient
            self._register_patient = RegisterPatient(self)
            self.stacked_widget.addWidget(self._register_patient)
        return self._register_patient

    # Show methods using navigate_to to add pages to the history stack
    def show_register_patient(self):
        self.navigate_to(self.register_patient)

    def show_login_page(self):
        self.navigate_to(self.login_page)

    def show_register_page(self):
        self.navigate_to(self.register_page)

    def show_presesh_page(self):
        self.navigate_to(self.presesh_page)

    def show_profile_page(self):
        self.navigate_to(self.profile_page)

    def show_history_page(self):
        self.navigate_to(self.history_page)

    def show_video_window(self):
        self.navigate_to(self.video_window)

    def show_vocal_visual_setting_page(self):
        self.navigate_to(self.vocal_visual_setting_page)

    def show_care_profile_settings(self):
        self.navigate_to(self.care_profile_settings)
