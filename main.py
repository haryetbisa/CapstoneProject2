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

#Voice Screen Pantig
from features.pantig_screen_vr.A import PantigA
from features.pantig_screen_vr.Ba import PantigBa
from features.pantig_screen_vr.Ka import PantigKa
from features.pantig_screen_vr.Da import PantigDa
from features.pantig_screen_vr.E import PantigE

#VS BilangK
from features.bilang_module.isa import Bilang1
from features.bilang_module.dalawa import Bilang2
from features.bilang_module.tatlo import Bilang3
from features.bilang_module.apat import Bilang4
from features.bilang_module.lima import Bilang5

#VS Hugis
from features.hugis_module.bilog.bilog_vs import BilogVS
from features.hugis_module.tatsulok.tatsulok_vs import TatsulokVS
from features.hugis_module.parisukat.parisukat_vs import ParisukatVS
from features.hugis_module.puso.puso_vs import PusoVS
from features.hugis_module.oblong.oblong_vs import OblongVS

#VS Hayop
from features.hayop_module.aso.aso_vs import AsoVS
from features.hayop_module.baboy.baboy_vs import BaboyVS
from features.hayop_module.bibe.bibe_vs import BibeVS
from features.hayop_module.isda.isda_vs import IsdaVS
from features.hayop_module.kabayo.kabayo_vs import KabayoVS

#VS PNK
from features.pnk_module.mata.mata_vs import MataVS
from features.pnk_module.labi.labi_vs import LabiVS
from features.pnk_module.ilong.ilong_vs import IlongVS
from features.pnk_module.tainga.tenga_vs import TengaVS
from features.pnk_module.buhok.buhok_vs import BuhokVS

#LessonSCreen Hayop
from features.hayop_module.aso.aso import LessonScreenAso
from features.hayop_module.baboy.baboy import LessonScreenBaboy
from features.hayop_module.bibe.bibe import LessonScreenBibe
from features.hayop_module.isda.isda import LessonScreenIsda
from features.hayop_module.kabayo.kabayo import LessonScreenKabayo
from features.hayop_module.kalabaw.kalabaw import LessonScreenKalabaw
from features.hayop_module.kambing.kambing import LessonScreenKambing
from features.hayop_module.kuneho.kuneho import LessonScreenKuneho
from features.hayop_module.manok.manok import LessonScreenManok
from features.hayop_module.pagong.pagong import LessonScreenPagong
from features.hayop_module.palaka.palaka import LessonScreenPalaka
from features.hayop_module.pusa.pusa import LessonScreenPusa
from features.hayop_module.unggoy.unggoy import LessonScreenUnggoy

#hugislesson screen
from features.hugis_module.bilog.bilog import LessonScreenBilog
from features.hugis_module.tatsulok.tatsulok import LessonScreenTatsu
from features.hugis_module.parisukat.parisukat import LessonScreenParisukat
from features.hugis_module.parihaba.parihaba import LessonScreenParihaba
from features.hugis_module.oblong.oblong import LessonScreenOblong
from features.hugis_module.puso.puso import LessonScreenPuso
from features.hugis_module.star.star import LessonScreenStar
from features.hugis_module.diamond.diamond import LessonScreenDiamond

#pnk lesson
from features.pnk_module.mata.mata import LessonScreenMata
from features.pnk_module.ilong.ilong import LessonScreenIlong
from features.pnk_module.labi.labi import LessonScreenLabi
from features.pnk_module.tainga.tainga import LessonScreenTaingaa
from features.pnk_module.buhok.buhok import LessonScreenBuhok
from features.pnk_module.leeg.leeg import LessonScreenLeeg
from features.pnk_module.balikat.balikat import LessonScreenBalikat
from features.pnk_module.tiyan.tiyan import LessonScreenTiyan
from features.pnk_module.braso.braso import LessonScreenBraso
from features.pnk_module.kamay.kamay import LessonScreenKamay
from features.pnk_module.binti.binti import LessonScreenBinti
from features.pnk_module.paa.paa import LessonScreenPaa

#kulay lesson
from features.kulay_module.pula.pula import Pula
from features.kulay_module.kahel.kahel import Kahel
from features.kulay_module.dilaw.dilaw import Dilaw
from features.kulay_module.berde.berde import Berde
from features.kulay_module.asul.asul import Asul

#kulay game
from features.kulay_module.pula.pula_game import DragDropRed
from features.kulay_module.kahel.kahel_game import DragDropOrange
from features.kulay_module.dilaw.dilaw_game import DragDropYellow
from features.kulay_module.berde.berde_game import DragDropGreen
from features.kulay_module.asul.asul_game import DragDropBlue

#pantig game
from features.pantig_screen_vr.A_game import MatchingGame
from features.pantig_screen_vr.B_game import MatchingBa

#hayop game 
from features.hayop_module.aso.aso_game import AsoGame
from features.hayop_module.baboy.baboy_game import BaboyGame

#hugis game 
from features.hugis_module.bilog.bilog_game import BilogGame
from features.hugis_module.tatsulok.tatsulok_game import TatsulokGame
from features.hugis_module.parisukat.parisukat_game import ParisukatGame
from features.hugis_module.puso.puso_game import PusoGame
from features.hugis_module.oblong.oblong_game import OblongGame

#kuwento screen
from features.kuwento.level1 import Kuwento1
from features.kuwento.level2 import Kuwento2

#kuwento question
from features.kuwento.level1_quest import Kuwento1Question


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("BasaMatika")
        self.setWindowIcon(QIcon("giraffe.png"))
        self.resize(500, 550)
        self.setStyleSheet(f"background-color: {LIGHT};")

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

#Main Screen ngani

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

#VR Pantig
        self.router.register("a", PantigA(self.router))
        self.router.register("ba", PantigBa(self.router))
        self.router.register("ka", PantigKa(self.router))
        self.router.register("da", PantigDa(self.router))
        self.router.register("e", PantigE(self.router))

#VR Bilang
        self.router.register("1", Bilang1(self.router))
        self.router.register("2", Bilang2(self.router))
        self.router.register("3", Bilang3(self.router))
        self.router.register("4", Bilang4(self.router))
        self.router.register("5", Bilang5(self.router))

#VR Hugis
        self.router.register("bilogvs", BilogVS(self.router))
        self.router.register("tatsulokvs", TatsulokVS(self.router))
        self.router.register("parisukatvs", ParisukatVS(self.router))
        self.router.register("pusovs", PusoVS(self.router))
        self.router.register("oblongvs", OblongVS(self.router))

#VR Hayop
        self.router.register("asovs", AsoVS(self.router))
        self.router.register("baboyvs", BaboyVS(self.router))
        self.router.register("bibevs", BibeVS(self.router))
        self.router.register("isdavs", IsdaVS(self.router))
        self.router.register("kabayovs", KabayoVS(self.router))

#VR PNK
        self.router.register("matavs", MataVS(self.router))
        self.router.register("labivs", LabiVS(self.router))
        self.router.register("ilongvs", IlongVS(self.router))
        self.router.register("tengavs", TengaVS(self.router))
        self.router.register("buhokvs", BuhokVS(self.router))


#HAYOP LessonSCreen
        self.router.register("aso_lesson", LessonScreenAso(self.router))
        self.router.register("baboy_lesson", LessonScreenBaboy(self.router))
        self.router.register("bibe_lesson", LessonScreenBibe(self.router))
        self.router.register("isda_lesson", LessonScreenIsda(self.router))
        self.router.register("kabayo_lesson", LessonScreenKabayo(self.router))
        self.router.register("kalabaw_lesson", LessonScreenKalabaw(self.router))
        self.router.register("kambing_lesson", LessonScreenKambing(self.router))
        self.router.register("kuneho_lesson", LessonScreenKuneho(self.router))
        self.router.register("manok_lesson", LessonScreenManok(self.router))
        self.router.register("pagong_lesson", LessonScreenPagong(self.router))
        self.router.register("palaka_lesson", LessonScreenPalaka(self.router))
        self.router.register("pusa_lesson", LessonScreenPusa(self.router))
        self.router.register("unggoy_lesson", LessonScreenUnggoy(self.router))
        
#HUGIS LS
        self.router.register("bilog", LessonScreenBilog(self.router))
        self.router.register("tatsu", LessonScreenTatsu(self.router))
        self.router.register("oblong", LessonScreenOblong(self.router))
        self.router.register("parisukat", LessonScreenParisukat(self.router))
        self.router.register("parihaba", LessonScreenParihaba(self.router))
        self.router.register("star", LessonScreenStar(self.router))       
        self.router.register("puso", LessonScreenPuso(self.router))
        self.router.register("diamond", LessonScreenDiamond(self.router))

#PNK LS
        self.router.register("mata", LessonScreenMata(self.router))
        self.router.register("ilong", LessonScreenIlong(self.router))
        self.router.register("labi", LessonScreenLabi(self.router))
        self.router.register("tenga", LessonScreenTaingaa(self.router))
        self.router.register("buhok", LessonScreenBuhok(self.router))
        self.router.register("leeg", LessonScreenLeeg(self.router))       
        self.router.register("balikat", LessonScreenBalikat(self.router))
        self.router.register("tiyan", LessonScreenTiyan(self.router)) 
        self.router.register("braso", LessonScreenBraso(self.router))
        self.router.register("kamay", LessonScreenKamay(self.router))       
        self.router.register("binti", LessonScreenBinti(self.router))

        self.router.register("paa", LessonScreenPaa(self.router))

#Kulay LS
        self.router.register("pula", Pula(self.router))
        self.router.register("kahel", Kahel(self.router))
        self.router.register("dilaw", Dilaw(self.router))
        self.router.register("berde", Berde(self.router))
        self.router.register("asul", Asul(self.router))

#KulayGame
        self.router.register("pula_game", DragDropRed(self.router))
        self.router.register("kahel_game", DragDropOrange(self.router))
        self.router.register("dilaw_game", DragDropYellow(self.router))
        self.router.register("berde_game", DragDropGreen(self.router))
        self.router.register("asul_game", DragDropBlue(self.router))

#Pantig Game
        self.router.register("A_game", MatchingGame(self.router))
        self.router.register("Ba_game", MatchingBa(self.router))

#Hayop Game
        self.router.register("aso_game", AsoGame(self.router))
        self.router.register("baboy_game", BaboyGame(self.router))

#Hugis Game
        self.router.register("bilog_game", BilogGame(self.router))
        self.router.register("tatsulok_game", TatsulokGame(self.router))
        self.router.register("parisukat_game", ParisukatGame(self.router))
        self.router.register("puso_game", PusoGame(self.router))
        self.router.register("oblong_game", OblongGame(self.router))

#Kuwento Screen
        self.router.register("level1", Kuwento1(self.router))
        self.router.register("level2", Kuwento2(self.router))

#Kuwento Question
        self.router.register("quest1", Kuwento1Question(self.router))

        self.router.navigate("loading_screen")

       

if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_fonts()
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())