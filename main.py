# main.py
import sys
import os
from themes.colors import *


from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PySide6.QtGui import QFontDatabase, QIcon


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")

def load_fonts():
    for root, dirs, files in os.walk(FONTS_DIR):
        for filename in files:
            if filename.lower().endswith((".ttf", ".otf")):
                path = os.path.join(root, filename)
                font_id = QFontDatabase.addApplicationFont(path)
                if font_id == -1:
                    print(f"Failed to load font: {filename}")
                else:
                    families = QFontDatabase.applicationFontFamilies(font_id)
                    print(f"Loaded '{filename}' as family: {families}")
                

#wag kalimutan mag-import, mag-eerror talaga :)))
from router import Router
from screens.loading_screen import LoadingScreen
from screens.account_info import AccountInfo
from features.voice_recog import VoiceRecognitionScreen
from features.lesson_screen import LessonScreen
from screens.create_account import CreateAccount
from screens.main_dashboard import HomeScreen
from screens.kinder_dashboard import KinderDashboard
from screens.grade1_dashboard import GradeOneDashboard
from screens.pantig_screen import PantigScreen
from screens.bilang_screen import BilangScreen
from screens.hugis_screen import HugisScreen
from screens.parte_ng_katawan_screen import ParteNgKatawanScreen
from screens.kulay_screen import KulayScreen
from screens.hayop_screen import HayopScreen
from screens.kuwento_screen import KuwentoScreen
from screens.bilang_screen_g1 import BilangScreenG1
from screens.pangungusap_screen import Pangungusap
from features.pantig_screen_vr.A import PantigA

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("BasaMatika")
        self.setWindowIcon(QIcon("giraffe.png"))
        self.resize(500, 550)
        self.setStyleSheet(f"background-color: {LIGHT};")

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.router = Router(self.stack)
        self.router.register("loading_screen", LoadingScreen(self.router))
        self.router.register("createacc", CreateAccount(self.router))
        self.router.register("credentials", AccountInfo(self.router))
        self.router.register("home", HomeScreen(self.router))
        self.router.register("kindergarten", KinderDashboard(self.router))
        self.router.register("grade1_dash", GradeOneDashboard(self.router))
        self.router.register("pantig", PantigScreen(self.router))
        self.router.register("bilang", BilangScreen(self.router))
        self.router.register("hugis", HugisScreen(self.router))
        self.router.register("katawan", ParteNgKatawanScreen(self.router))
        self.router.register("kulay", KulayScreen(self.router))
        self.router.register("hayop", HayopScreen(self.router))
        self.router.register("vr", VoiceRecognitionScreen(self.router))
        self.router.register("kuwento", KuwentoScreen(self.router))
        self.router.register("bilang_g1", BilangScreenG1(self.router))
        self.router.register("pangungusap", Pangungusap(self.router))
        self.router.register("lesson", LessonScreen(self.router))

        self.router.register("a", PantigA(self.router))




        self.router.navigate("loading_screen")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_fonts()
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())