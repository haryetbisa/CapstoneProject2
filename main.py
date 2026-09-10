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
from features.voice_recog import OfflineVoiceWorker
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
from screens.salita_screen import SalitaScreen

#Voice Screen Pantig
from features.pantig_screen_vr.A import PantigA
from features.pantig_screen_vr.Ba import PantigBa
from features.pantig_screen_vr.Ka import PantigKa
from features.pantig_screen_vr.Da import PantigDa
from features.pantig_screen_vr.E import PantigE
from features.pantig_screen_vr.Ga import PantigGa
from features.pantig_screen_vr.Ha import PantigHa
from features.pantig_screen_vr.I import PantigI
from features.pantig_screen_vr.La import PantigLa
from features.pantig_screen_vr.Ma import PantigMa
from features.pantig_screen_vr.Na import PantigNa
from features.pantig_screen_vr.Nga import PantigNga
from features.pantig_screen_vr.O import PantigO
from features.pantig_screen_vr.Pa import PantigPa
from features.pantig_screen_vr.Ra import PantigRa
from features.pantig_screen_vr.Sa import PantigSa
from features.pantig_screen_vr.Ta import PantigTa
from features.pantig_screen_vr.U import PantigU
from features.pantig_screen_vr.Wa import PantigWa
from features.pantig_screen_vr.Ya import PantigYa


#VS BilangK
from features.bilang_module.isa import Bilang1
from features.bilang_module.dalawa import Bilang2
from features.bilang_module.tatlo import Bilang3
from features.bilang_module.apat import Bilang4
from features.bilang_module.lima import Bilang5
from features.bilang_module.anim import Bilang6
from features.bilang_module.pito import Bilang7
from features.bilang_module.walo import Bilang8
from features.bilang_module.siyam import Bilang9
from features.bilang_module.sampu import Bilang10

#GameBilangK
from features.bilang_module.isa_game import IsaGame
from features.bilang_module.dalawa_game import DalawaGame
from features.bilang_module.tatlo_game import TatloGame
from features.bilang_module.apat_game import ApatGame
from features.bilang_module.lima_game import LimaGame
from features.bilang_module.anim_game import AnimGame
from features.bilang_module.pito_game import PitoGame
from features.bilang_module.walo_game import WaloGame
from features.bilang_module.siyam_game import SiyamGame
from features.bilang_module.sampu_game import SampuGame

#VS Hugis
from features.hugis_module.bilog.bilog_vs import BilogVS
from features.hugis_module.tatsulok.tatsulok_vs import TatsulokVS
from features.hugis_module.parisukat.parisukat_vs import ParisukatVS
from features.hugis_module.puso.puso_vs import PusoVS
from features.hugis_module.oblong.oblong_vs import OblongVS
from features.hugis_module.parihaba.parihaba_vs import ParihabaVS
from features.hugis_module.diamond.diamond_vs import RombusVS
from features.hugis_module.star.star_vs import StarVS

#VS Hayop
from features.hayop_module.aso.aso_vs import AsoVS
from features.hayop_module.baboy.baboy_vs import BaboyVS
from features.hayop_module.bibe.bibe_vs import BibeVS
from features.hayop_module.isda.isda_vs import IsdaVS
from features.hayop_module.kabayo.kabayo_vs import KabayoVS
from features.hayop_module.kalabaw.kalabaw_vs import KalabawVS
from features.hayop_module.kambing.kambing_vs import KambingVS
from features.hayop_module.kuneho.kuneho_vs import KunehoVS
from features.hayop_module.manok.manok_vs import ManokVS
from features.hayop_module.pagong.pagong_vs import PagongVS
from features.hayop_module.palaka.palaka_vs import PalakaVS
from features.hayop_module.pusa.pusa_vs import PusaVS
from features.hayop_module.unggoy.unggoy_vs import UnggoyVS

#VS PNK
from features.pnk_module.mata.mata_vs import MataVS
from features.pnk_module.labi.labi_vs import LabiVS
from features.pnk_module.ilong.ilong_vs import IlongVS
from features.pnk_module.tainga.tenga_vs import TengaVS
from features.pnk_module.buhok.buhok_vs import BuhokVS
from features.pnk_module.leeg.leeg_vs import LeegVS
from features.pnk_module.balikat.balikat_vs import BalikatVS
from features.pnk_module.tiyan.tiyan_vs import TiyanVS
from features.pnk_module.braso.braso_vs import BrasoVS
from features.pnk_module.kamay.kamay_vs import KamayVS
from features.pnk_module.binti.binti_vs import BintiVS
from features.pnk_module.paa.paa_vs import PaaVS

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
from features.kulay_module.lila.lila import Lila
from features.kulay_module.kayumanggi.kayumanggi import Kayumanggi
from features.kulay_module.itim.itim import Itim

#kulay game
from features.kulay_module.pula.pula_game import DragDropRed
from features.kulay_module.kahel.kahel_game import DragDropOrange
from features.kulay_module.dilaw.dilaw_game import DragDropYellow
from features.kulay_module.berde.berde_game import DragDropGreen
from features.kulay_module.asul.asul_game import DragDropBlue
from features.kulay_module.lila.lila_game import DragDropPurple
from features.kulay_module.kayumanggi.kayumanggi_game import DragDropBrown
from features.kulay_module.itim.itim_game import DragDropBlack

#pantig game
from features.pantig_screen_vr.A_game import MatchingGame
from features.pantig_screen_vr.B_game import MatchingBa
from features.pantig_screen_vr.Ka_game import MatchingKa
from features.pantig_screen_vr.Da_game import MatchingDa
from features.pantig_screen_vr.E_game import MatchingE
from features.pantig_screen_vr.Ga_game import MatchingGa
from features.pantig_screen_vr.Ha_game import MatchingHa
from features.pantig_screen_vr.I_game import MatchingI
from features.pantig_screen_vr.La_game import MatchingLa
from features.pantig_screen_vr.Ma_game import MatchingMa
from features.pantig_screen_vr.Na_game import MatchingNa
from features.pantig_screen_vr.Nga_game import MatchingNga
from features.pantig_screen_vr.O_game import MatchingO
from features.pantig_screen_vr.Pa_game import MatchingPa
from features.pantig_screen_vr.Ra_game import MatchingRa
from features.pantig_screen_vr.Sa_game import MatchingSa
from features.pantig_screen_vr.Ta_game import MatchingTa
from features.pantig_screen_vr.U_game import MatchingU
from features.pantig_screen_vr.Wa_game import MatchingWa
from features.pantig_screen_vr.Ya_game import MatchingYa


#hayop game 
from features.hayop_module.aso.aso_game import AsoGame
from features.hayop_module.baboy.baboy_game import BaboyGame
from features.hayop_module.bibe.bibe_game import BibeGame
from features.hayop_module.isda.isda_game import IsdaGame
from features.hayop_module.kabayo.kabayo_game import KabayoGame
from features.hayop_module.kalabaw.kalabaw_game import KalabawGame
from features.hayop_module.kambing.kambing_game import KambingGame
from features.hayop_module.kuneho.kuneho_game import KunehoGame
from features.hayop_module.manok.manok_game import ManokGame
from features.hayop_module.pagong.pagong_game import PagongGame
from features.hayop_module.palaka.palaka_game import PalakaGame
from features.hayop_module.pusa.pusa_game import PusaGame
from features.hayop_module.unggoy.unggoy_game import UnggoyGame

#hugis game 
from features.hugis_module.bilog.bilog_game import BilogGame
from features.hugis_module.tatsulok.tatsulok_game import TatsulokGame
from features.hugis_module.parisukat.parisukat_game import ParisukatGame
from features.hugis_module.puso.puso_game import PusoGame
from features.hugis_module.oblong.oblong_game import OblongGame
from features.hugis_module.parihaba.parihaba_game import ParihabaGame
from features.hugis_module.diamond.diamond_game import DiamondGame
from features.hugis_module.star.star_game import StarGame

#kuwento screen
from features.kuwento.level1 import Kuwento1
from features.kuwento.level2 import Kuwento2
from features.kuwento.level3 import Kuwento3
from features.kuwento.level4 import Kuwento4
from features.kuwento.level5 import Kuwento5
from features.kuwento.level6 import Kuwento6
from features.kuwento.level7 import Kuwento7
from features.kuwento.level8 import Kuwento8
from features.kuwento.level9 import Kuwento9
from features.kuwento.level10 import Kuwento10

#kuwento question
from features.kuwento.level1_quest import Kuwento1Question
from features.kuwento.level2_quest import Kuwento2Question
from features.kuwento.level3_quest import Kuwento3Question
from features.kuwento.level4_quest import Kuwento4Question
from features.kuwento.level5_quest import Kuwento5Question
from features.kuwento.level6_quest import Kuwento6Question
from features.kuwento.level7_quest import Kuwento7Question
from features.kuwento.level8_quest import Kuwento8Question
from features.kuwento.level9_quest import Kuwento9Question
from features.kuwento.level10_quest import Kuwento10Question

#salita screen
from features.salita.salita1.salita1_lesson import Salita1
from features.salita.salita2.salita2_lesson import Salita2
from features.salita.salita3.salita3_lesson import Salita3

#salita game
from features.salita.salita1.level1_game import Salita1Game
from features.salita.salita1.level2_game import Salita2Game
from features.salita.salita1.level3_game import Salita3Game
from features.salita.salita1.level4_game import Salita4Game
from features.salita.salita2.level5_game import Salita5Game
from features.salita.salita2.level6_game import Salita6Game
from features.salita.salita2.level7_game import Salita7Game
from features.salita.salita2.level8_game import Salita8Game
from features.salita.salita3.level9_game import Salita9Game
from features.salita.salita3.level10_game import Salita10Game
from features.salita.salita3.level11_game import Salita11Game
from features.salita.salita3.level12_game import Salita12Game


#BilangG1 Screen
from features.g1_bilangmodule.bilog.bilog import LessonMath1
from features.g1_bilangmodule.parisukat.parisukat import LessonMath2
from features.g1_bilangmodule.parihaba.parihaba import LessonMath3
from features.g1_bilangmodule.tatsulok.tatsulok import LessonMath4

#BilangG1 Quest
from features.g1_bilangmodule.bilog.bilog_quest import BilangLvl1
from features.g1_bilangmodule.parisukat.parisukat_quest import BilangLvl2
from features.g1_bilangmodule.parihaba.parihaba_quest import BilangLvl3
from features.g1_bilangmodule.tatsulok.tatsulok_quest import BilangLvl4


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("BasaMatika")
        self.setWindowIcon(QIcon("logo.png"))
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
        self.router.register("kuwento", KuwentoScreen(self.router))
        self.router.register("bilang_g1", BilangScreenG1(self.router))
        self.router.register("salita", SalitaScreen(self.router))
        self.router.register("lesson", LessonScreen(self.router))

#VR Pantig
        self.router.register("a", PantigA(self.router))
        self.router.register("ba", PantigBa(self.router))
        self.router.register("ka", PantigKa(self.router))
        self.router.register("da", PantigDa(self.router))
        self.router.register("e", PantigE(self.router))
        self.router.register("ga", PantigGa(self.router))
        self.router.register("ha", PantigHa(self.router))
        self.router.register("i", PantigI(self.router))
        self.router.register("la", PantigLa(self.router))
        self.router.register("ma", PantigMa(self.router))
        self.router.register("na", PantigNa(self.router))
        self.router.register("nga", PantigNga(self.router))
        self.router.register("o", PantigO(self.router))
        self.router.register("pa", PantigPa(self.router))
        self.router.register("ra", PantigRa(self.router))
        self.router.register("sa", PantigSa(self.router))
        self.router.register("ta", PantigTa(self.router))
        self.router.register("u", PantigU(self.router))
        self.router.register("wa", PantigWa(self.router))
        self.router.register("ya", PantigYa(self.router))
        

#VR Bilang
        self.router.register("1", Bilang1(self.router))
        self.router.register("2", Bilang2(self.router))
        self.router.register("3", Bilang3(self.router))
        self.router.register("4", Bilang4(self.router))
        self.router.register("5", Bilang5(self.router))
        self.router.register("6", Bilang6(self.router))
        self.router.register("7", Bilang7(self.router))
        self.router.register("8", Bilang8(self.router))
        self.router.register("9", Bilang9(self.router))
        self.router.register("10", Bilang10(self.router))

#BilangK Game
        self.router.register("isa_game", IsaGame(self.router))
        self.router.register("dalawa_game", DalawaGame(self.router))
        self.router.register("tatlo_game", TatloGame(self.router))
        self.router.register("apat_game", ApatGame(self.router))
        self.router.register("lima_game", LimaGame(self.router))
        self.router.register("anim_game", AnimGame(self.router))
        self.router.register("pito_game", PitoGame(self.router))
        self.router.register("walo_game", WaloGame(self.router))
        self.router.register("siyam_game", SiyamGame(self.router))
        self.router.register("sampu_game", SampuGame(self.router))

#VR Hugis
        self.router.register("bilogvs", BilogVS(self.router))
        self.router.register("tatsulokvs", TatsulokVS(self.router))
        self.router.register("parisukatvs", ParisukatVS(self.router))
        self.router.register("pusovs", PusoVS(self.router))
        self.router.register("oblongvs", OblongVS(self.router))
        self.router.register("parihabavs", ParihabaVS(self.router))
        self.router.register("diamondvs", RombusVS(self.router))
        self.router.register("starvs", StarVS(self.router))

#VR Hayop
        self.router.register("asovs", AsoVS(self.router))
        self.router.register("baboyvs", BaboyVS(self.router))
        self.router.register("bibevs", BibeVS(self.router))
        self.router.register("isdavs", IsdaVS(self.router))
        self.router.register("kabayovs", KabayoVS(self.router))
        self.router.register("kalabawvs", KalabawVS(self.router))
        self.router.register("kambingvs", KambingVS(self.router))
        self.router.register("kunehovs", KunehoVS(self.router))
        self.router.register("manokvs", ManokVS(self.router))
        self.router.register("pagongvs", PagongVS(self.router))
        self.router.register("palakavs", PalakaVS(self.router))
        self.router.register("pusavs", PusaVS(self.router))
        self.router.register("unggoyvs", UnggoyVS(self.router))

#VR PNK
        self.router.register("matavs", MataVS(self.router))
        self.router.register("labivs", LabiVS(self.router))
        self.router.register("ilongvs", IlongVS(self.router))
        self.router.register("tengavs", TengaVS(self.router))
        self.router.register("buhokvs", BuhokVS(self.router))
        self.router.register("leegvs", LeegVS(self.router))
        self.router.register("balikatvs", BalikatVS(self.router))
        self.router.register("tiyanvs", TiyanVS(self.router))
        self.router.register("brasovs", BrasoVS(self.router))
        self.router.register("kamayvs", KamayVS(self.router))
        self.router.register("bintivs", BintiVS(self.router))
        self.router.register("paavs", PaaVS(self.router))


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
        self.router.register("lila", Lila(self.router))
        self.router.register("kayumanggi", Kayumanggi(self.router))
        self.router.register("itim", Itim(self.router))

#KulayGame
        self.router.register("pula_game", DragDropRed(self.router))
        self.router.register("kahel_game", DragDropOrange(self.router))
        self.router.register("dilaw_game", DragDropYellow(self.router))
        self.router.register("berde_game", DragDropGreen(self.router))
        self.router.register("asul_game", DragDropBlue(self.router))
        self.router.register("lila_game", DragDropPurple(self.router))
        self.router.register("kayumanggi_game", DragDropBrown(self.router))
        self.router.register("itim_game", DragDropBlack(self.router))

#Pantig Game
        self.router.register("A_game", MatchingGame(self.router))
        self.router.register("Ba_game", MatchingBa(self.router))
        self.router.register("Ka_game", MatchingKa(self.router))
        self.router.register("Da_game", MatchingDa(self.router))
        self.router.register("E_game", MatchingE(self.router))
        self.router.register("Ga_game", MatchingGa(self.router))
        self.router.register("Ha_game", MatchingHa(self.router))
        self.router.register("I_game", MatchingI(self.router))
        self.router.register("La_game", MatchingLa(self.router))
        self.router.register("Ma_game", MatchingMa(self.router))
        self.router.register("Na_game", MatchingNa(self.router))
        self.router.register("Nga_game", MatchingNga(self.router))
        self.router.register("O_game", MatchingO(self.router))
        self.router.register("Pa_game", MatchingPa(self.router))
        self.router.register("Ra_game", MatchingRa(self.router))
        self.router.register("Sa_game", MatchingSa(self.router))
        self.router.register("Ta_game", MatchingTa(self.router))
        self.router.register("U_game", MatchingU(self.router))
        self.router.register("Wa_game", MatchingWa(self.router))
        self.router.register("Ya_game", MatchingYa(self.router))

#Hayop Game
        self.router.register("aso_game", AsoGame(self.router))
        self.router.register("baboy_game", BaboyGame(self.router))
        self.router.register("bibe_game", BibeGame(self.router))
        self.router.register("isda_game", IsdaGame(self.router))
        self.router.register("kabayo_game", KabayoGame(self.router))
        self.router.register("kalabaw_game", KalabawGame(self.router))
        self.router.register("kambing_game", KambingGame(self.router))
        self.router.register("kuneho_game", KunehoGame(self.router))
        self.router.register("manok_game", ManokGame(self.router))
        self.router.register("pagong_game", PagongGame(self.router))
        self.router.register("palaka_game", PalakaGame(self.router))
        self.router.register("pusa_game", PusaGame(self.router))
        self.router.register("unggoy_game", UnggoyGame(self.router))

#Hugis Game
        self.router.register("bilog_game", BilogGame(self.router))
        self.router.register("tatsulok_game", TatsulokGame(self.router))
        self.router.register("parisukat_game", ParisukatGame(self.router))
        self.router.register("puso_game", PusoGame(self.router))
        self.router.register("oblong_game", OblongGame(self.router))
        self.router.register("parihaba_game", ParihabaGame(self.router))
        self.router.register("diamond_game", DiamondGame(self.router))
        self.router.register("star_game", StarGame(self.router))

#Kuwento Screen
        self.router.register("level1", Kuwento1(self.router))
        self.router.register("level2", Kuwento2(self.router))
        self.router.register("level3", Kuwento3(self.router))
        self.router.register("level4", Kuwento4(self.router))
        self.router.register("level5", Kuwento5(self.router))
        self.router.register("level6", Kuwento6(self.router))
        self.router.register("level7", Kuwento7(self.router))
        self.router.register("level8", Kuwento8(self.router))
        self.router.register("level9", Kuwento9(self.router))
        self.router.register("level10", Kuwento10(self.router))

#Kuwento Question
        self.router.register("quest1", Kuwento1Question(self.router))
        self.router.register("quest2", Kuwento2Question(self.router))
        self.router.register("quest3", Kuwento3Question(self.router))
        self.router.register("quest4", Kuwento4Question(self.router))
        self.router.register("quest5", Kuwento5Question(self.router))
        self.router.register("quest6", Kuwento6Question(self.router))
        self.router.register("quest7", Kuwento7Question(self.router))
        self.router.register("quest8", Kuwento8Question(self.router))
        self.router.register("quest9", Kuwento9Question(self.router))
        self.router.register("quest10", Kuwento10Question(self.router))


#Salita Screen
        self.router.register("salita1", Salita1(self.router))
        self.router.register("salita2", Salita2(self.router))
        self.router.register("salita3", Salita3(self.router))

#Salita Game
        self.router.register("salitaq1", Salita1Game(self.router))
        self.router.register("salitaq2", Salita2Game(self.router))
        self.router.register("salitaq3", Salita3Game(self.router))
        self.router.register("salitaq4", Salita4Game(self.router))
        self.router.register("salitaq5", Salita5Game(self.router))
        self.router.register("salitaq6", Salita6Game(self.router))
        self.router.register("salitaq7", Salita7Game(self.router))
        self.router.register("salitaq8", Salita8Game(self.router))
        self.router.register("salitaq9", Salita9Game(self.router))
        self.router.register("salitaq10", Salita10Game(self.router))
        self.router.register("salitaq11", Salita11Game(self.router))
        self.router.register("salitaq12", Salita12Game(self.router))
      

#Bilang G1 Screen
        self.router.register("g1_bilog", LessonMath1(self.router))
        self.router.register("g1_parisukat", LessonMath2(self.router))
        self.router.register("g1_parihaba", LessonMath3(self.router))
        self.router.register("g1_tatsulok", LessonMath4(self.router))

#Bilang G1 Quest
        self.router.register("bilog_quest", BilangLvl1(self.router))
        self.router.register("parisukat_quest", BilangLvl2(self.router))
        self.router.register("parihaba_quest", BilangLvl3(self.router))
        self.router.register("tatsulok_quest", BilangLvl4(self.router))


#starting screen
        self.router.navigate("loading_screen")

       

if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_fonts()
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())