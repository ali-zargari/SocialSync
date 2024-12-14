from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QStackedWidget

# Import all the necessary pages
from ui.pyqt.P1_U1_user_login import LoginPage
from ui.pyqt.p3_first_register import RegistrationForm
from ui.pyqt.p4_register_patient import RegisterPatient
from ui.pyqt.p5_session_overview import OverviewScreen as SessionOverview
from ui.pyqt.p6_care_profile_settings import MainWindow as CareProfileSettings
from ui.pyqt.p6_selected_user_session_overview import OverviewScreen as SelectedUserSessionOverview
from ui.pyqt.p10_session_history import HistoryPage
from ui.pyqt.u2_profile_init import ProfileSetup
from ui.pyqt.u3_vocal_and_visual_setting import VocalVisualSettingsScreen
from ui.pyqt.u4_home import MainWindow as Home
from ui.pyqt.u5_Emotion_session_happy import MainWindow as EmotionSessionHappy
from ui.pyqt.u6_Emotion_session_sad import MainWindow as EmotionSessionSad
from ui.pyqt.u7_camera_working_session_dashboard import MainWindow as CameraWorkingSessionDashboard
from ui.pyqt.u8_Emotion_session_annoyed import MainWindow as EmotionSessionAnnoyed
from ui.pyqt.u9_profile_setting_gui import MainWindow as ProfileSettingGUI
from ui.pyqt.u_vocal_and_visual_setting import MainWindow as VocalAndVisualSetting
from ui.pyqt.u11_session_over_view import OverviewScreen as User_SessionOverview
from ui.pyqt.new_user_flow import LoginPage as NewUserLoginPage
from ui.pyqt.new_asd_practioner_register import RegistrationForm as ASDPractitionerRegistration
from ui.pyqt.practioner_landing_page import LoginPage as PractitionerLandingPage
from ui.pyqt.new_asd_patient_register import RegistrationForm as ASDPatientRegistration

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.navigation_stack = []  # Track page history for Back navigation

        self.setWindowTitle("SocialSync")
        self.setGeometry(100, 100, 1200, 700)

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

    # Define properties for each page
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
    def register_patient(self):
        if not hasattr(self, '_register_patient'):
            self._register_patient = RegisterPatient(self)
            self.stacked_widget.addWidget(self._register_patient)
        return self._register_patient

    @property
    def session_overview(self):
        if not hasattr(self, '_session_overview'):
            self._session_overview = SessionOverview(self)
            self.stacked_widget.addWidget(self._session_overview)
        return self._session_overview

    @property
    def care_profile_settings(self):
        if not hasattr(self, '_care_profile_settings'):
            self._care_profile_settings = CareProfileSettings(self)
            self.stacked_widget.addWidget(self._care_profile_settings)
        return self._care_profile_settings

    @property
    def selected_user_session_overview(self):
        if not hasattr(self, '_selected_user_session_overview'):
            self._selected_user_session_overview = SelectedUserSessionOverview(self)
            self.stacked_widget.addWidget(self._selected_user_session_overview)
        return self._selected_user_session_overview

    @property
    def history_page(self):
        if not hasattr(self, '_history_page'):
            self._history_page = HistoryPage(self)
            self.stacked_widget.addWidget(self._history_page)
        return self._history_page

    @property
    def profile_page(self):
        if not hasattr(self, '_profile_page'):
            self._profile_page = ProfileSetup(self)
            self.stacked_widget.addWidget(self._profile_page)
        return self._profile_page

    @property
    def vocal_visual_setting_page(self):
        if not hasattr(self, '_vocal_visual_setting_page'):
            self._vocal_visual_setting_page = VocalVisualSettingsScreen(self)
            self.stacked_widget.addWidget(self._vocal_visual_setting_page)
        return self._vocal_visual_setting_page

    @property
    def home_page(self):
        if not hasattr(self, '_home_page'):
            self._home_page = Home(self)
            self.stacked_widget.addWidget(self._home_page)
        return self._home_page

    @property
    def emotion_session_happy(self):
        if not hasattr(self, '_emotion_session_happy'):
            self._emotion_session_happy = EmotionSessionHappy(self)
            self.stacked_widget.addWidget(self._emotion_session_happy)
        return self._emotion_session_happy

    @property
    def emotion_session_sad(self):
        if not hasattr(self, '_emotion_session_sad'):
            self._emotion_session_sad = EmotionSessionSad(self)
            self.stacked_widget.addWidget(self._emotion_session_sad)
        return self._emotion_session_sad

    @property
    def video_window(self):
        if not hasattr(self, '_video_window'):
            self._video_window = CameraWorkingSessionDashboard(self)
            self.stacked_widget.addWidget(self._video_window)
        return self._video_window

    @property
    def emotion_session_annoyed(self):
        if not hasattr(self, '_emotion_session_annoyed'):
            self._emotion_session_annoyed = EmotionSessionAnnoyed(self)
            self.stacked_widget.addWidget(self._emotion_session_annoyed)
        return self._emotion_session_annoyed

    @property
    def profile_setting_gui(self):
        if not hasattr(self, '_profile_setting_gui'):
            self._profile_setting_gui = ProfileSettingGUI(self)
            self.stacked_widget.addWidget(self._profile_setting_gui)
        return self._profile_setting_gui

    @property
    def vocal_and_visual_setting(self):
        if not hasattr(self, '_vocal_and_visual_setting'):
            self._vocal_and_visual_setting = VocalAndVisualSetting(self)
            self.stacked_widget.addWidget(self._vocal_and_visual_setting)
        return self._vocal_and_visual_setting

    @property
    def user_session_overview(self):
        if not hasattr(self, '_user_session_overview'):
            self._user_session_overview = User_SessionOverview(self)
            self.stacked_widget.addWidget(self._user_session_overview)
        return self._user_session_overview

    @property
    def new_user_flow(self):
        if not hasattr(self, '_new_user_flow'):
            self._new_user_flow = NewUserLoginPage(self)
            self.stacked_widget.addWidget(self._new_user_flow)
        return self._new_user_flow

    @property
    def asd_practitioner_registration(self):
        if not hasattr(self, '_asd_practitioner_registration'):
            self._asd_practitioner_registration = ASDPractitionerRegistration(self)
            self.stacked_widget.addWidget(self._asd_practitioner_registration)
        return self._asd_practitioner_registration

    @property
    def practitioner_landing_page(self):
        if not hasattr(self, '_practitioner_landing_page'):
            self._practitioner_landing_page = PractitionerLandingPage(self)
            self.stacked_widget.addWidget(self._practitioner_landing_page)
        return self._practitioner_landing_page

    @property
    def asd_patient_registration(self):
        if not hasattr(self, '_asd_patient_registration'):
            self._asd_patient_registration = ASDPatientRegistration(self)
            self.stacked_widget.addWidget(self._asd_patient_registration)
        return self._asd_patient_registration

    # Show methods using navigate_to to add pages to the history stack
    def show_login_page(self):
        self.navigate_to(self.login_page)

    def show_register_page(self):
        self.navigate_to(self.register_page)

    def show_second_register_user(self):
        self.navigate_to(self.second_register_user)

    def show_register_patient(self):
        self.navigate_to(self.register_patient)

    def show_session_overview(self):
        self.navigate_to(self.session_overview)

    def show_care_profile_settings(self):
        self.navigate_to(self.care_profile_settings)

    def show_selected_user_session_overview(self):
        self.navigate_to(self.selected_user_session_overview)

    def show_history_page(self):
        self.navigate_to(self.history_page)

    def show_profile_page(self):
        self.navigate_to(self.profile_page)

    def show_vocal_visual_setting_page(self):
        self.navigate_to(self.vocal_visual_setting_page)

    def show_home_page(self):
        self.navigate_to(self.home_page)

    def show_emotion_session_happy(self):
        self.navigate_to(self.emotion_session_happy)

    def show_emotion_session_sad(self):
        self.navigate_to(self.emotion_session_sad)

    def show_video_window(self):
        self.navigate_to(self.video_window)

    def show_emotion_session_annoyed(self):
        self.navigate_to(self.emotion_session_annoyed)

    def show_profile_setting_gui(self):
        self.navigate_to(self.profile_setting_gui)

    def show_vocal_and_visual_setting(self):
        self.navigate_to(self.vocal_and_visual_setting)

    def show_user_session_overview(self):
        self.navigate_to(self.user_session_overview)

    def show_new_user_flow(self):
        self.navigate_to(self.new_user_flow)

    def show_asd_practitioner_registration(self):
        self.navigate_to(self.asd_practitioner_registration)

    def show_practitioner_landing_page(self):
        self.navigate_to(self.practitioner_landing_page)

    def show_asd_patient_registration(self):
        self.navigate_to(self.asd_patient_registration)

