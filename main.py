import re
import sys
from ctypes import cdll
from random import choice

from PyQt6.QtCore import QCoreApplication, QRect, QEasingCurve, QMetaObject, pyqtSignal, QUrl,Qt,QSize
from PyQt6.QtGui import QFont, QMouseEvent, QCursor, QIcon, QDesktopServices
from PyQt6.QtWidgets import QWidget, QFrame, QStackedWidget, QMainWindow, QVBoxLayout, QSizePolicy, QGridLayout, \
    QTextEdit, QApplication, QHBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit, QListView, QListWidget, \
    QListWidgetItem,QSizeGrip
from Qss.Home import *
from moudules import *

widgets = None

name = None
First = False
Ans = []
Origin = []
Users = []
s1 = "color: rgb(255, 255, 255);" \
     "font-size: 15px;" \
     "font-weight:bold;"
s2 = "color: rgb(255, 255, 255);" \
     "font-size: 12px;" \
     "font-weight:bold;"
s3 = "color: rgb(255, 255, 255);" \
     "font-size: 10px;" \
     "font-weight:bold;"
Sudoku = cdll.LoadLibrary("./Lib/libSudoku.dll")
themeFile = ""


class SudokuComboBox(QComboBox):
    def __init__(self, parent=None):
        super(QComboBox, self).__init__(parent)
        self.ListView = QListWidget()
        # self.ListView.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.ListView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ListView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setModel(self.ListView.model())
        self.setView(self.ListView)
        self.setMaxVisibleItems(6)
        self.setEditable(True)
        self.view().window().setWindowFlags(
            Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint | Qt.WindowType.NoDropShadowWindowHint)
        self.view().window().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.LineEdit = QLineEdit()
        self.LineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.LineEdit.setReadOnly(True)
        self.setLineEdit(self.LineEdit)
        self.LineEdit.setMaxLength(15)
        self.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)
        QApplication.setEffectEnabled(Qt.UIEffect.UI_AnimateCombo, False)
        self.add(["Easy:20", "Middle:40", "Hard:60", "Difficult:80", "Hell:100", "Personalize"])

    popupAboutToBeShown = pyqtSignal()

    def showPopup(self):
        QComboBox.showPopup(self)
        Widget = self.findChild(QFrame)
        Widget.move(Widget.x(), Widget.y() + 4)
        self.popupAboutToBeShown.emit()

    def add(self, s: list):
        for i in s:
            item = QListWidgetItem(i)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ListView.addItem(item)
        item = QListWidgetItem("Personalize:")
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)


class Timer(QLabel):
    def __init__(self, parent=None):
        super(QLabel, self).__init__(parent)
        self.a = 0
        self.timer = None
        self.Check = True
        clock = QPushButton()
        self.setMinimumSize(QSize(80, 20))
        clock.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        clock.setStyleSheet("background-color: transparent;"
                            "border: 1px solid transparent;")
        clock.setIcon(QIcon("icons/clock.svg"))
        HLayout = QHBoxLayout()
        HLayout.setContentsMargins(0, 0, 0, 0)
        HLayout.addSpacing(0)
        HLayout.addWidget(clock, 0, Qt.AlignmentFlag.AlignLeft)
        self.setText("      %02d : %02d" % (0, 0))
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setLayout(HLayout)

    def timerEvent(self, a):
        s = "      %02d : %02d" % (self.a / 6000, self.a % 6000 / 100)
        self.setText(str(s))
        self.a += 1

    def start(self):
        if self.a != 0:
            self.a = 0
            self.killTimer(self.timer)
        self.timer = self.startTimer(10)

    def stop(self):
        if self.Check:
            self.killTimer(self.timer)
            self.Check = False
        else:
            self.timer = self.startTimer(10)
            self.Check = True

    def end(self):
        if self.a != 0:
            self.a = 0
            self.killTimer(self.timer)

    def restart(self):
        if self.a != 0:
            self.a = 0
            self.killTimer(self.timer)
        self.timer = self.startTimer(10)


# os.environ["QT_FONT_DPI"] = "96"

class MainWindow(QMainWindow):
    _startPos = None
    _endPos = None
    _isTracking = False
    _O = None

    def __init__(self):
        QMainWindow.__init__(self)
        self.initUI()
        Settings.ENABLE_CUSTOM_TITLE_BAR = True
        title = "Sudoku-Potato"
        description = "Based on DPLL"
        # APPLY TEXTS
        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        self.toggleMenuCheck = True
        self.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, self.toggleMenuCheck))
        self.setWindowTitle(title)
        self.titleRightInfo.setText(description)
        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)
        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        self.btn_home.clicked.connect(self.buttonClick)
        self.Game_Sudoku.clicked.connect(self.buttonClick)

        # widgets.Link.clicked.connect(self.buttonClick)
        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)

        self.toggleLeftBox.clicked.connect(openCloseLeftBox)
        self.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)

        self.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()
        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = True
        global themeFile
        themeFile = "Qss/py_dracula_light.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        self.stackedWidget.setCurrentWidget(self.home)
        self.btn_home.setStyleSheet(UIFunctions.selectMenu(self.btn_home.styleSheet()))

    def initUI(self):
        self.setFixedSize(QSize(1250, 825))
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.styleSheet = QWidget(self)
        self.styleSheet.setObjectName(u"styleSheet")
        self.styleSheet.setMouseTracking(True)
        font = QFont()
        font.setFamily(u"Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.styleSheet.setFont(font)
        self.appMargins = QVBoxLayout(self.styleSheet)
        self.appMargins.setSpacing(0)
        self.appMargins.setObjectName(u"appMargins")
        self.appMargins.setContentsMargins(10, 10, 10, 10)
        self.bgApp = QFrame(self.styleSheet)
        self.bgApp.setObjectName(u"bgApp")
        self.bgApp.setStyleSheet(u"")
        self.bgApp.setFrameShape(QFrame.frameShape(self.bgApp).NoFrame)
        self.bgApp.setFrameShadow(QFrame.frameShadow(self.bgApp).Raised)
        self.appLayout = QHBoxLayout(self.bgApp)
        self.appLayout.setSpacing(0)
        self.appLayout.setObjectName(u"appLayout")
        self.appLayout.setContentsMargins(0, 0, 0, 0)
        self.leftMenuBg = QFrame(self.bgApp)
        self.leftMenuBg.setObjectName(u"leftMenuBg")
        self.leftMenuBg.setMinimumSize(QSize(60, 0))
        self.leftMenuBg.setMaximumSize(QSize(60, 16777215))
        self.leftMenuBg.setFrameShape(QFrame.frameShape(self.leftMenuBg).NoFrame)
        self.leftMenuBg.setFrameShadow(QFrame.frameShadow(self.leftMenuBg).Raised)
        self.verticalLayout_3 = QVBoxLayout(self.leftMenuBg)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.topLogoInfo = QFrame(self.leftMenuBg)
        self.topLogoInfo.setObjectName(u"topLogoInfo")
        self.topLogoInfo.setMinimumSize(QSize(0, 50))
        self.topLogoInfo.setMaximumSize(QSize(16777215, 50))
        self.topLogoInfo.setFrameShape(QFrame.frameShape(self.topLogoInfo).NoFrame)
        self.topLogoInfo.setFrameShadow(QFrame.frameShadow(self.topLogoInfo).Raised)
        self.topLogo = QPushButton(self.topLogoInfo)
        self.topLogo.setObjectName(u"topLogo")
        self.topLogo.setGeometry(QRect(10, 5, 42, 42))
        self.topLogo.setMinimumSize(QSize(42, 42))
        self.topLogo.setIcon(QIcon("images/watermelon_outline.svg"))
        self.topLogo.setIconSize(QSize(42, 42))
        self.topLogo.setMaximumSize(QSize(42, 42))
        self.topLogo.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.titleLeftApp = QLabel(self.topLogoInfo)
        self.titleLeftApp.setObjectName(u"titleLeftApp")
        self.titleLeftApp.setGeometry(QRect(70, 8, 160, 20))
        font1 = QFont()
        font1.setFamily(u"Segoe UI Semibold")
        font1.setPointSize(12)
        font1.setBold(False)
        font1.setItalic(False)
        self.titleLeftApp.setFont(font1)
        self.titleLeftApp.setAlignment(
            Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.titleLeftDescription = QLabel(self.topLogoInfo)
        self.titleLeftDescription.setObjectName(u"titleLeftDescription")
        self.titleLeftDescription.setGeometry(QRect(70, 27, 160, 16))
        self.titleLeftDescription.setMaximumSize(QSize(16777215, 16))
        font2 = QFont()
        font2.setFamily(u"Segoe UI")
        font2.setPointSize(8)
        font2.setBold(False)
        font2.setItalic(False)
        self.titleLeftDescription.setFont(font2)
        self.titleLeftDescription.setAlignment(
            Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.verticalLayout_3.addWidget(self.topLogoInfo)

        self.leftMenuFrame = QFrame(self.leftMenuBg)
        self.leftMenuFrame.setObjectName(u"leftMenuFrame")
        self.leftMenuFrame.setFrameShape(QFrame.frameShape(self.leftMenuFrame).NoFrame)
        self.leftMenuFrame.setFrameShadow(QFrame.frameShadow(self.leftMenuFrame).Raised)
        self.verticalMenuLayout = QVBoxLayout(self.leftMenuFrame)
        self.verticalMenuLayout.setSpacing(0)
        self.verticalMenuLayout.setObjectName(u"verticalMenuLayout")
        self.verticalMenuLayout.setContentsMargins(0, 0, 0, 0)
        self.toggleBox = QFrame(self.leftMenuFrame)
        self.toggleBox.setObjectName(u"toggleBox")
        self.toggleBox.setMaximumSize(QSize(16777215, 45))
        self.toggleBox.setFrameShape(QFrame.frameShape(self.toggleBox).NoFrame)
        self.toggleBox.setFrameShadow(QFrame.frameShadow(self.toggleBox).Raised)
        self.verticalLayout_4 = QVBoxLayout(self.toggleBox)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.toggleButton = QPushButton(self.toggleBox)
        self.toggleButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.toggleButton.setObjectName(u"toggleButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toggleButton.sizePolicy().hasHeightForWidth())
        self.toggleButton.setSizePolicy(sizePolicy)
        self.toggleButton.setMinimumSize(QSize(0, 45))
        self.toggleButton.setFont(font)
        self.toggleButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.toggleButton.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.toggleButton.setIcon(QIcon("icons/bars.svg"))
        self.toggleButton.setIconSize(QSize(20, 20))
        self.verticalLayout_4.addWidget(self.toggleButton)

        self.verticalMenuLayout.addWidget(self.toggleBox)

        self.topMenu = QFrame(self.leftMenuFrame)
        self.topMenu.setObjectName(u"topMenu")
        self.topMenu.setFrameShape(QFrame.frameShape(self.topMenu).NoFrame)
        self.topMenu.setFrameShadow(QFrame.frameShadow(self.topMenu).Raised)
        self.verticalLayout_8 = QVBoxLayout(self.topMenu)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.btn_home = QPushButton(self.topMenu)
        self.btn_home.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_home.setObjectName(u"btn_home")
        sizePolicy.setHeightForWidth(self.btn_home.sizePolicy().hasHeightForWidth())
        self.btn_home.setSizePolicy(sizePolicy)
        self.btn_home.setMinimumSize(QSize(0, 45))
        self.btn_home.setFont(font)
        self.btn_home.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_home.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.btn_home.setIcon(QIcon("icons/house.svg"))
        self.btn_home.setIconSize(QSize(20, 20))
        self.verticalLayout_8.addWidget(self.btn_home)
        self.Game_Sudoku = QPushButton(self.topMenu)
        self.Game_Sudoku.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.Game_Sudoku.setObjectName(u"Game_Sudoku")
        sizePolicy.setHeightForWidth(self.Game_Sudoku.sizePolicy().hasHeightForWidth())
        self.Game_Sudoku.setSizePolicy(sizePolicy)
        self.Game_Sudoku.setMinimumSize(QSize(0, 45))
        self.Game_Sudoku.setFont(font)
        self.Game_Sudoku.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Game_Sudoku.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.Game_Sudoku.setIcon(QIcon("icons/gamepad.svg"))
        self.Game_Sudoku.setIconSize(QSize(20, 20))
        self.verticalLayout_8.addWidget(self.Game_Sudoku)
        self.verticalMenuLayout.addWidget(self.topMenu, 0, Qt.AlignmentFlag.AlignTop)
        self.bottomMenu = QFrame(self.leftMenuFrame)
        self.bottomMenu.setObjectName(u"bottomMenu")
        self.bottomMenu.setFrameShape(QFrame.frameShape(self.bottomMenu).NoFrame)
        self.bottomMenu.setFrameShadow(QFrame.frameShadow(self.bottomMenu).Raised)
        self.verticalLayout_9 = QVBoxLayout(self.bottomMenu)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.toggleLeftBox = QPushButton(self.bottomMenu)
        self.toggleLeftBox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.toggleLeftBox.setObjectName(u"toggleLeftBox")
        sizePolicy.setHeightForWidth(self.toggleLeftBox.sizePolicy().hasHeightForWidth())
        self.toggleLeftBox.setSizePolicy(sizePolicy)
        self.toggleLeftBox.setMinimumSize(QSize(0, 45))
        self.toggleLeftBox.setFont(font)
        self.toggleLeftBox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.toggleLeftBox.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.toggleLeftBox.setIcon(QIcon("icons/gears.svg"))
        self.toggleLeftBox.setIconSize(QSize(20, 20))

        self.verticalLayout_9.addWidget(self.toggleLeftBox)

        self.verticalMenuLayout.addWidget(self.bottomMenu, 0, Qt.AlignmentFlag.AlignBottom)

        self.verticalLayout_3.addWidget(self.leftMenuFrame)
        self.appLayout.addWidget(self.leftMenuBg)
        self.extraLeftBox = QFrame(self.bgApp)
        self.extraLeftBox.setObjectName(u"extraLeftBox")
        self.extraLeftBox.setMinimumSize(QSize(0, 0))
        self.extraLeftBox.setMaximumSize(QSize(0, 16777215))
        self.extraLeftBox.setFrameShape(QFrame.frameShape(self.extraLeftBox).NoFrame)
        self.extraLeftBox.setFrameShadow(QFrame.frameShadow(self.extraLeftBox).Raised)
        self.extraColumLayout = QVBoxLayout(self.extraLeftBox)
        self.extraColumLayout.setSpacing(0)
        self.extraColumLayout.setObjectName(u"extraColumLayout")
        self.extraColumLayout.setContentsMargins(0, 0, 0, 0)
        self.extraTopBg = QFrame(self.extraLeftBox)
        self.extraTopBg.setObjectName(u"extraTopBg")
        self.extraTopBg.setMinimumSize(QSize(0, 50))
        self.extraTopBg.setMaximumSize(QSize(16777215, 50))
        self.extraTopBg.setFrameShape(QFrame.frameShape(self.extraTopBg).NoFrame)
        self.extraTopBg.setFrameShadow(QFrame.frameShadow(self.extraTopBg).Raised)
        self.verticalLayout_5 = QVBoxLayout(self.extraTopBg)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.extraTopLayout = QGridLayout()
        self.extraTopLayout.setObjectName(u"extraTopLayout")
        self.extraTopLayout.setHorizontalSpacing(10)
        self.extraTopLayout.setVerticalSpacing(0)
        self.extraTopLayout.setContentsMargins(10, -1, 10, -1)
        self.extraIcon = QFrame(self.extraTopBg)
        self.extraIcon.setObjectName(u"extraIcon")
        self.extraIcon.setMinimumSize(QSize(20, 0))
        self.extraIcon.setMaximumSize(QSize(20, 20))
        self.extraIcon.setFrameShape(QFrame.frameShape(self.extraIcon).NoFrame)
        self.extraIcon.setFrameShadow(QFrame.frameShadow(self.extraIcon).Raised)

        self.extraTopLayout.addWidget(self.extraIcon, 0, 0, 1, 1)

        self.extraLabel = QLabel(self.extraTopBg)
        self.extraLabel.setObjectName(u"extraLabel")
        self.extraLabel.setMinimumSize(QSize(150, 0))

        self.extraTopLayout.addWidget(self.extraLabel, 0, 1, 1, 1)

        self.extraCloseColumnBtn = QPushButton(self.extraTopBg)
        self.extraCloseColumnBtn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.extraCloseColumnBtn.setObjectName(u"extraCloseColumnBtn")
        self.extraCloseColumnBtn.setMinimumSize(QSize(28, 28))
        self.extraCloseColumnBtn.setMaximumSize(QSize(28, 28))
        self.extraCloseColumnBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon = QIcon('icons/xmark.svg')
        self.extraCloseColumnBtn.setIcon(icon)
        self.extraCloseColumnBtn.setIconSize(QSize(20, 20))

        self.extraTopLayout.addWidget(self.extraCloseColumnBtn, 0, 2, 1, 1)

        self.verticalLayout_5.addLayout(self.extraTopLayout)

        self.extraColumLayout.addWidget(self.extraTopBg)

        self.extraContent = QFrame(self.extraLeftBox)
        self.extraContent.setObjectName(u"extraContent")
        self.extraContent.setFrameShape(QFrame.frameShape(self.extraContent).NoFrame)
        self.extraContent.setFrameShadow(QFrame.frameShadow(self.extraContent).Raised)
        self.verticalLayout_12 = QVBoxLayout(self.extraContent)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.extraTopMenu = QFrame(self.extraContent)
        self.extraTopMenu.setObjectName(u"extraTopMenu")
        self.extraTopMenu.setFrameShape(QFrame.frameShape(self.extraTopMenu).NoFrame)
        self.extraTopMenu.setFrameShadow(QFrame.frameShadow(self.extraTopMenu).Raised)
        self.verticalLayout_11 = QVBoxLayout(self.extraTopMenu)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.btn_share = QPushButton(self.extraTopMenu)
        self.btn_share.setObjectName(u"share")
        self.btn_share.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        sizePolicy.setHeightForWidth(self.btn_share.sizePolicy().hasHeightForWidth())
        self.btn_share.setSizePolicy(sizePolicy)
        self.btn_share.setMinimumSize(QSize(0, 45))
        self.btn_share.setFont(font)
        self.btn_share.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_share.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.btn_share.setIcon(QIcon("icons/square-share-nodes.svg"))
        self.btn_share.clicked.connect(self.buttonClick)
        self.verticalLayout_11.addWidget(self.btn_share)

        self.Adjustments_Button = QPushButton(self.extraTopMenu)
        self.Adjustments_Button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.Adjustments_Button.setObjectName(u"Adjustments")
        sizePolicy.setHeightForWidth(self.Adjustments_Button.sizePolicy().hasHeightForWidth())
        self.Adjustments_Button.setSizePolicy(sizePolicy)
        self.Adjustments_Button.setMinimumSize(QSize(0, 45))
        self.Adjustments_Button.setFont(font)
        self.Adjustments_Button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.Adjustments_Button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.Adjustments_Button.setIcon(QIcon("icons/sliders.svg"))
        self.Adjustments_Button.clicked.connect(self.buttonClick)

        self.verticalLayout_11.addWidget(self.Adjustments_Button)

        self.btn_more = QPushButton(self.extraTopMenu)
        self.btn_more.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_more.setObjectName(u"more")
        sizePolicy.setHeightForWidth(self.btn_more.sizePolicy().hasHeightForWidth())
        self.btn_more.setSizePolicy(sizePolicy)
        self.btn_more.setMinimumSize(QSize(0, 45))
        self.btn_more.setFont(font)
        self.btn_more.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_more.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.btn_more.setIcon(QIcon("icons/layer-group.svg"))
        self.btn_more.clicked.connect(self.buttonClick)

        self.verticalLayout_11.addWidget(self.btn_more)

        self.verticalLayout_12.addWidget(self.extraTopMenu, 0, Qt.AlignmentFlag.AlignTop)

        self.extraCenter = QFrame(self.extraContent)
        self.extraCenter.setObjectName(u"extraCenter")
        self.extraCenter.setFrameShape(QFrame.frameShape(self.extraCenter).NoFrame)
        self.extraCenter.setFrameShadow(QFrame.frameShadow(self.extraCenter).Raised)
        self.verticalLayout_10 = QVBoxLayout(self.extraCenter)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.textEdit = QTextEdit(self.extraCenter)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setMinimumSize(QSize(222, 0))
        self.textEdit.setStyleSheet(u"background: transparent;")
        self.textEdit.setFrameShape(QFrame.frameShape(self.textEdit).NoFrame)
        self.textEdit.setReadOnly(True)

        self.verticalLayout_10.addWidget(self.textEdit)

        self.verticalLayout_12.addWidget(self.extraCenter)

        self.extraBottom = QFrame(self.extraContent)
        self.extraBottom.setObjectName(u"extraBottom")
        self.extraBottom.setFrameShape(QFrame.frameShape(self.extraBottom).NoFrame)
        self.extraBottom.setFrameShadow(QFrame.frameShadow(self.extraBottom).Raised)

        self.verticalLayout_12.addWidget(self.extraBottom)

        self.extraColumLayout.addWidget(self.extraContent)

        self.appLayout.addWidget(self.extraLeftBox)
        # others
        self.contentBox = QFrame(self.bgApp)
        self.contentBox.setObjectName(u"contentBox")
        self.contentBox.setFrameShape(QFrame.frameShape(self.contentBox).NoFrame)
        self.contentBox.setFrameShadow(QFrame.frameShadow(self.contentBox).Raised)
        self.verticalLayout_2 = QVBoxLayout(self.contentBox)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.contentTopBg = QFrame(self.contentBox)
        self.contentTopBg.setObjectName(u"contentTopBg")
        self.contentTopBg.setMinimumSize(QSize(0, 50))
        self.contentTopBg.setMaximumSize(QSize(16777215, 50))
        self.contentTopBg.setFrameShape(QFrame.frameShape(self.contentTopBg).NoFrame)
        self.contentTopBg.setFrameShadow(QFrame.frameShadow(self.contentTopBg).Raised)
        self.horizontalLayout = QHBoxLayout(self.contentTopBg)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 10, 0)
        self.leftBox = QFrame(self.contentTopBg)
        self.leftBox.setObjectName(u"leftBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.leftBox.sizePolicy().hasHeightForWidth())
        self.leftBox.setSizePolicy(sizePolicy1)
        self.leftBox.setFrameShape(QFrame.frameShape(self.leftBox).NoFrame)
        self.leftBox.setFrameShadow(QFrame.frameShadow(self.leftBox).Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.leftBox)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.titleRightInfo = QLabel(self.leftBox)
        self.titleRightInfo.setObjectName(u"titleRightInfo")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.titleRightInfo.sizePolicy().hasHeightForWidth())
        self.titleRightInfo.setSizePolicy(sizePolicy2)
        self.titleRightInfo.setMaximumSize(QSize(16777215, 45))
        self.titleRightInfo.setFont(font)
        self.titleRightInfo.setAlignment(
            Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.titleRightInfo)

        self.horizontalLayout.addWidget(self.leftBox)

        self.rightButtons = QFrame(self.contentTopBg)
        self.rightButtons.setObjectName(u"rightButtons")
        self.rightButtons.setMinimumSize(QSize(0, 28))
        self.rightButtons.setFrameShape(QFrame.frameShape(self.rightButtons).NoFrame)
        self.rightButtons.setFrameShadow(QFrame.frameShadow(self.rightButtons).Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.rightButtons)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.settingsTopBtn = QPushButton(self.rightButtons)
        self.settingsTopBtn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.settingsTopBtn.setObjectName(u"settingsTopBtn")
        self.settingsTopBtn.setMinimumSize(QSize(28, 28))
        self.settingsTopBtn.setMaximumSize(QSize(28, 28))
        self.settingsTopBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.settingsTopBtn.setIcon(QIcon("icons/gear.svg"))
        self.settingsTopBtn.setIconSize(QSize(20, 20))
        self.settingsTopBtn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.horizontalLayout_2.addWidget(self.settingsTopBtn)

        self.minimizeAppBtn = QPushButton(self.rightButtons)
        self.minimizeAppBtn.setObjectName(u"minimizeAppBtn")
        self.minimizeAppBtn.setMinimumSize(QSize(28, 28))
        self.minimizeAppBtn.setMaximumSize(QSize(28, 28))
        self.minimizeAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.minimizeAppBtn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.minimizeAppBtn.setIcon(QIcon('icons/window-minimize.svg'))
        self.minimizeAppBtn.setIconSize(QSize(20, 20))
        self.horizontalLayout_2.addWidget(self.minimizeAppBtn)
        self.maximizeRestoreAppBtn = QPushButton(self.rightButtons)
        self.maximizeRestoreAppBtn.setObjectName(u"maximizeRestoreAppBtn")
        self.maximizeRestoreAppBtn.setMinimumSize(QSize(30, 30))
        self.maximizeRestoreAppBtn.setMaximumSize(QSize(30, 30))
        self.maximizeRestoreAppBtn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        font3 = QFont()
        font3.setFamily(u"Segoe UI")
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        font3.setStyleStrategy(QFont.StyleStrategy.PreferDefault)
        self.maximizeRestoreAppBtn.setFont(font3)
        self.maximizeRestoreAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.maximizeRestoreAppBtn.setIcon(QIcon("icons/window-maximize.svg"))
        self.maximizeRestoreAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.maximizeRestoreAppBtn)

        self.closeAppBtn = QPushButton(self.rightButtons)
        self.closeAppBtn.setObjectName(u"closeAppBtn")
        self.closeAppBtn.setMinimumSize(QSize(28, 28))
        self.closeAppBtn.setMaximumSize(QSize(28, 28))
        self.closeAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.closeAppBtn.setIcon(icon)
        self.closeAppBtn.setIconSize(QSize(20, 20))
        self.closeAppBtn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.horizontalLayout_2.addWidget(self.closeAppBtn)

        self.horizontalLayout.addWidget(self.rightButtons, 0, Qt.AlignmentFlag.AlignRight)

        self.verticalLayout_2.addWidget(self.contentTopBg)

        self.contentBottom = QFrame(self.contentBox)
        self.contentBottom.setObjectName(u"contentBottom")
        self.contentBottom.setFrameShape(QFrame.frameShape(self.contentBottom).NoFrame)
        self.contentBottom.setFrameShadow(QFrame.frameShadow(self.contentBottom).Raised)
        self.verticalLayout_6 = QVBoxLayout(self.contentBottom)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.content = QFrame(self.contentBottom)
        self.content.setObjectName(u"content")
        self.content.setFrameShape(QFrame.frameShape(self.content).NoFrame)
        self.content.setFrameShadow(QFrame.frameShadow(self.content).Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.content)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pagesContainer = QFrame(self.content)
        self.pagesContainer.setObjectName(u"pagesContainer")
        self.pagesContainer.setStyleSheet(u"")
        self.pagesContainer.setFrameShape(QFrame.frameShape(self.pagesContainer).NoFrame)
        self.pagesContainer.setFrameShadow(QFrame.frameShadow(self.pagesContainer).Raised)
        self.verticalLayout_15 = QVBoxLayout(self.pagesContainer)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(10, 10, 10, 10)
        self.stackedWidget = QStackedWidget(self.pagesContainer)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"background: transparent;")
        self.home = QWidget()
        HomeHLayout = QHBoxLayout(self.home)
        self.home.setObjectName(u"home")
        self.HomeDecription = QTextEdit(self.home)
        self.HomeDecription.setObjectName(u"HomeDecription")
        self.HomeDecription.setMinimumSize(QSize(222, 600))
        self.HomeDecription.setStyleSheet(u"background: transparent;")
        self.HomeDecription.setFrameShape(QFrame.frameShape(self.HomeDecription).NoFrame)
        self.HomeDecription.setReadOnly(True)
        self.HomeDecription.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        HomeHLayout.addWidget(self.HomeDecription)
        self.home.setLayout(HomeHLayout)
        self.stackedWidget.addWidget(self.home)
        self.new = QWidget()
        self.new.setObjectName("new")
        self.new.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        data = open("Qss/Sudoku.qss").read()
        self.new.setStyleSheet(data)
        VLayout = QVBoxLayout()
        self.HLayout = QHBoxLayout()
        self.HLayout.setContentsMargins(0, 0, 0, 0)
        self.HLayout.setSpacing(1)
        self.HLayout.addLayout(VLayout)
        SudokuGrid = QGridLayout()
        VLayout.addLayout(SudokuGrid)
        SudokuGrid.setSpacing(1)
        positions = [(i, j) for i in range(15) for j in range(15)]
        for position in positions:
            if not ((position[0] >= 9 and position[1] < 6) or (position[0] < 6 and position[1] >= 9)):
                Frame = QFrame(self.new)
                Frame.setFrameShape(QFrame.frameShape(Frame).Box)
                Frame.setFixedSize(45, 45)
                Frame.setStyleSheet("border:1px solid rgb(0,0,0)")
                DigitButton = QPushButton(Frame)
                ButtonName = "%02d %02d" % (position[0] + 1, position[1] + 1)
                DigitButton.setObjectName(ButtonName)
                DigitButton.clicked.connect(self.ButtonClick)
                DigitButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
                DigitButton.setFixedSize(45, 45)
                SudokuGrid.addWidget(Frame, *position)
        self.RightMenu = QFrame(self.new)
        self.RightMenu.setFrameShape(QFrame.frameShape(self.RightMenu).NoFrame)
        self.RightMenu.setMaximumSize(225, 700)
        self.RightMenu.setMinimumSize(225, 600)
        self.RightMenu.setObjectName(u"RightMenu")
        RightMenuVBox = QVBoxLayout(self.RightMenu)
        RightMenuTop = QFrame(self.RightMenu)
        RightMenuTop.setMaximumSize(QSize(16777215, 3))
        RightMenuTop.setFrameShape(QFrame.frameShape(RightMenuTop).NoFrame)
        RightMenuTop.setFrameShadow(QFrame.frameShadow(RightMenuTop).Raised)
        RightMenuTop.setObjectName(u"RightMenuTop")
        RightMenuVBox.addWidget(RightMenuTop)
        RightMenuContainers = QFrame(self.RightMenu)
        RightMenuContainers.setObjectName(u"RightMenuContainers")
        RightMenuVLayout = QVBoxLayout(RightMenuContainers)
        RightMenuVLayout.setObjectName(u"RightMenuVLayout")
        RightMenuButtons = QFrame(RightMenuContainers)
        RightMenuButtons.setObjectName(u"RightMenuButtons")
        RightMenuButtonsLayout = QVBoxLayout(RightMenuButtons)
        RightMenuButtonsLayout.setObjectName("RightMenuButtonsLayout")
        SudokuStartButton = QPushButton(self.RightMenu)
        SudokuRestartButton = QPushButton(self.RightMenu)
        SudokuStopButton = QPushButton(self.RightMenu)
        SudokuInfoButton = QPushButton(self.RightMenu)
        SudokuSubmitButton = QPushButton(self.RightMenu)
        SudokuSubmitButton.setIcon(QIcon("icons/paper-plane.svg"))
        SudokuStartButton.setIcon(QIcon("icons/circle-play.svg"))
        SudokuRestartButton.setIcon(QIcon("icons/arrow-rotate-right.svg"))
        SudokuStopButton.setIcon(QIcon("icons/circle-pause.svg"))
        SudokuInfoButton.setIcon(QIcon("icons/circle-info.svg"))
        SudokuInfoButton.setText("Tip")
        SudokuStartButton.setText("Start")
        SudokuStopButton.setText("Stop")
        SudokuRestartButton.setText("Restart")
        SudokuSubmitButton.setText("Submit")
        SudokuSubmitButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        SudokuInfoButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        SudokuStartButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        SudokuStopButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        SudokuRestartButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        SudokuStartButton.setObjectName("Start")
        SudokuStopButton.setObjectName("Stop")
        SudokuRestartButton.setObjectName("Restart")
        SudokuInfoButton.setObjectName("Tip")
        SudokuSubmitButton.setObjectName("Submit")
        SudokuStartButton.setMinimumSize(100, 25)
        SudokuStopButton.setMinimumSize(100, 25)
        SudokuRestartButton.setMinimumSize(100, 25)
        SudokuInfoButton.setMinimumSize(100, 25)
        SudokuSubmitButton.setMinimumSize(100, 30)
        SudokuInfoButton.clicked.connect(self.buttonClick)
        SudokuStartButton.clicked.connect(self.buttonClick)
        SudokuStopButton.clicked.connect(self.buttonClick)
        SudokuRestartButton.clicked.connect(self.buttonClick)
        SudokuSubmitButton.clicked.connect(self.buttonClick)
        self.SudokuLevel = SudokuComboBox(self.new)
        self.SudokuLevel.setMinimumSize(100, 30)
        self.SudokuLevel.setObjectName("combo")
        self.SudokuLevel.setToolTip("This is used to choose the level")
        self.TimerLabel = Timer(self.RightMenu)
        self.TipLabel = QLabel(self.RightMenu)
        self.TipLabel.setObjectName("TipLabel")
        self.RecordLabel = QLabel(self.RightMenu)
        self.RecordLabel.setObjectName("RecordLabel")
        self.RecordLabel.setMinimumSize(QSize(10, 20))
        self.SudokuLevel.currentIndexChanged.connect(self.Edit)
        self.SudokuLevel.currentTextChanged.connect(self.TextChanged)
        with open("record/record.info", "rb") as f:
            data = f.readlines()
            a = int(data[19].decode(encoding="utf-8"))
            if a == 99999999:
                s = "No record yet"
            else:
                s = "Best record:%02d : %02d" % (
                    a / 6000, a % 6000 / 100)
            self.RecordLabel.setText(s)
        self.TipBox = QTextEdit(self.RightMenu)
        self.TipBox.setCursor(Qt.CursorShape.PointingHandCursor)
        self.TipBox.setMinimumSize(10, 100)
        self.TipBox.setObjectName("TipBox")
        self.TipBox.setReadOnly(True)
        self.TipBox.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        RightMenuButtonsLayout.addWidget(self.TimerLabel, 0, Qt.AlignmentFlag.AlignHCenter)
        RightMenuButtonsLayout.addWidget(SudokuStartButton)
        RightMenuButtonsLayout.addWidget(SudokuRestartButton)
        RightMenuButtonsLayout.addWidget(SudokuStopButton)
        RightMenuButtonsLayout.addWidget(SudokuInfoButton)
        RightMenuButtonsLayout.addWidget(self.SudokuLevel)
        RightMenuButtonsLayout.addWidget(self.TipLabel)
        RightMenuButtonsLayout.addWidget(self.RecordLabel, 0, Qt.AlignmentFlag.AlignHCenter)
        RightMenuButtonsLayout.addWidget(self.TipBox)
        Space = QFrame()
        Space.setStyleSheet("background-color: transparent;")
        Space.setMinimumSize(100, 1000)
        RightMenuButtonsLayout.addWidget(Space)
        RightMenuButtonsLayout.addWidget(SudokuSubmitButton)
        RightMenuVLayout.addWidget(RightMenuButtons, 0, Qt.AlignmentFlag.AlignTop)
        RightMenuVBox.addWidget(RightMenuContainers)
        self.HLayout.addWidget(self.RightMenu)
        self.new.setLayout(self.HLayout)
        self.stackedWidget.addWidget(self.new)
        self.verticalLayout_15.addWidget(self.stackedWidget)
        self.horizontalLayout_4.addWidget(self.pagesContainer)
        #####
        self.RightBox = QFrame(self.content)
        self.RightBox.setObjectName(u"RightBox")
        self.RightBox.setMinimumSize(QSize(0, 0))
        self.RightBox.setMaximumSize(QSize(0, 16777215))
        self.RightBox.setFrameShape(QFrame.frameShape(self.RightBox).NoFrame)
        self.RightBox.setFrameShadow(QFrame.frameShadow(self.RightBox).Raised)
        self.RightVBox = QVBoxLayout(self.RightBox)
        self.RightVBox.setSpacing(0)
        self.RightVBox.setObjectName(u"RightVBox")
        self.RightVBox.setContentsMargins(0, 0, 0, 0)
        self.RightBoxTop = QFrame(self.RightBox)
        self.RightBoxTop.setObjectName(u"RightBoxTop")
        self.RightBoxTop.setMaximumSize(QSize(16777215, 3))
        self.RightBoxTop.setFrameShape(QFrame.frameShape(self.RightBoxTop).NoFrame)
        self.RightBoxTop.setFrameShadow(QFrame.frameShadow(self.RightBoxTop).Raised)
        self.RightVBox.addWidget(self.RightBoxTop)
        self.RightBoxContainers = QFrame(self.RightBox)
        self.RightBoxContainers.setObjectName(u"RightBoxContainers")
        self.RightBoxContainers.setFrameShape(QFrame.frameShape(self.RightBoxContainers).NoFrame)
        self.RightBoxContainers.setFrameShadow(QFrame.frameShadow(self.RightBoxContainers).Raised)
        self.RightBoxVlayout = QVBoxLayout(self.RightBoxContainers)
        self.RightBoxVlayout.setSpacing(0)
        self.RightBoxVlayout.setObjectName(u"RightBoxVlayout")
        self.RightBoxVlayout.setContentsMargins(0, 0, 0, 0)
        self.RightBoxButtons = QFrame(self.RightBoxContainers)
        self.RightBoxButtons.setObjectName(u"RightBoxButtons")
        self.RightBoxButtons.setFrameShape(QFrame.frameShape(self.RightBoxButtons).NoFrame)
        self.RightBoxButtons.setFrameShadow(QFrame.frameShadow(self.RightBoxButtons).Raised)
        self.RightBoxButtonsLayout = QVBoxLayout(self.RightBoxButtons)
        self.RightBoxButtonsLayout.setSpacing(0)
        self.RightBoxButtonsLayout.setObjectName(u"RightBoxButtonsLayout")
        self.RightBoxButtonsLayout.setContentsMargins(0, 0, 0, 0)
        Message_Button = QPushButton(self.RightBoxButtons)
        Message_Button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        Message_Button.setObjectName(u"message")
        Message_Button.setMinimumSize(QSize(240, 45))
        Message_Button.setFont(font)
        Message_Button.setText("  Message")
        Message_Button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        Message_Button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        Message_Button.setIcon(QIcon("icons/square-envelope.svg"))
        Message_Button.setIconSize(QSize(30, 30))
        Message_Button.clicked.connect(self.buttonClick)
        self.RightBoxButtonsLayout.addWidget(Message_Button, 0, Qt.AlignmentFlag.AlignLeft)
        self.RightBoxVlayout.addWidget(self.RightBoxButtons, 0, Qt.AlignmentFlag.AlignTop)

        self.RightVBox.addWidget(self.RightBoxContainers)

        self.horizontalLayout_4.addWidget(self.RightBox)

        self.verticalLayout_6.addWidget(self.content)

        self.bottomBar = QFrame(self.contentBottom)
        self.bottomBar.setObjectName(u"bottomBar")
        self.bottomBar.setMinimumSize(QSize(0, 22))
        self.bottomBar.setMaximumSize(QSize(16777215, 22))
        self.bottomBar.setFrameShape(QFrame.frameShape(self.bottomBar).NoFrame)
        self.bottomBar.setFrameShadow(QFrame.frameShadow(self.bottomBar).Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.bottomBar)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.creditsLabel = QLabel(self.bottomBar)
        self.creditsLabel.setObjectName(u"creditsLabel")
        self.creditsLabel.setMaximumSize(QSize(16777215, 16))
        font5 = QFont()
        font5.setFamily(u"Segoe UI")
        font5.setBold(False)
        font5.setItalic(False)
        self.creditsLabel.setFont(font5)
        self.creditsLabel.setAlignment(
            Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.horizontalLayout_5.addWidget(self.creditsLabel)

        self.version = QLabel(self.bottomBar)
        self.version.setObjectName(u"version")
        self.version.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.version)
        self.verticalLayout_6.addWidget(self.bottomBar)

        self.verticalLayout_2.addWidget(self.contentBottom)

        self.appLayout.addWidget(self.contentBox)

        self.appMargins.addWidget(self.bgApp)
        self.setCentralWidget(self.styleSheet)

        self.retranslateUi()

        self.stackedWidget.setCurrentIndex(2)

        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.titleLeftApp.setText(QCoreApplication.translate("MainWindow", u"Sudoku", None))
        self.titleLeftDescription.setText(
            QCoreApplication.translate("MainWindow", u"Hello World", None))
        self.toggleButton.setText(QCoreApplication.translate("MainWindow", u"        Hide", None))
        self.btn_home.setText(QCoreApplication.translate("MainWindow", u"      Home", None))
        self.Game_Sudoku.setText(QCoreApplication.translate("MainWindow", u"      Sudoku", None))
        self.toggleLeftBox.setText(QCoreApplication.translate("MainWindow", u"      Left Box", None))
        self.extraLabel.setText(QCoreApplication.translate("MainWindow", u"      Left Box", None))
        self.extraCloseColumnBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close left box", None))
        self.extraCloseColumnBtn.setText("")
        self.btn_share.setText(QCoreApplication.translate("MainWindow", u"Share", None))
        self.Adjustments_Button.setText(QCoreApplication.translate("MainWindow", u"Adjustments", None))
        self.btn_more.setText(QCoreApplication.translate("MainWindow", u"More", None))
        self.HomeDecription.setHtml(QCoreApplication.translate("MainWindow", Light_Home, None))
        self.titleRightInfo.setText(QCoreApplication.translate("MainWindow",
                                                               u"PyDracula APP - Theme with colors based on Dracula "
                                                               u"for Python.",
                                                               None))
        self.settingsTopBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.settingsTopBtn.setText("")
        self.minimizeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Minimize", None))
        self.minimizeAppBtn.setText("")
        self.maximizeRestoreAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Maximize", None))
        self.maximizeRestoreAppBtn.setText("")
        self.closeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close", None))
        self.closeAppBtn.setText("")
        self.creditsLabel.setText(QCoreApplication.translate("MainWindow", u"By: Potato", None))
        self.version.setText(QCoreApplication.translate("MainWindow", u"v1.0.0", None))

    def SudokuInit(self):
        global First, Ans, Origin, Users
        L1 = []
        L2 = []
        n = int(1)
        with open("sudoku/sudoku.txt", "r") as f:
            List = f.readlines()
            for i in List:
                if n > 9:
                    i = i.replace("  ", "", 6)
                n += 1
                num = i.split(" ")
                L1.append(num)
        n = int(1)
        with open("sudoku/sudoku.ans", "r") as f:
            List = f.readlines()
            if len(List) > 15:
                string = List[15]
            else:
                string = ""
            for i in List:
                if n > 9:
                    i = i.replace("  ", "", 6)
                n += 1
                num = i.split(" ")
                L2.append(num)

        positions = [(i, j) for i in range(15) for j in range(15)]
        if not First:
            First = True
        else:
            Origin = []
            Ans = []
            for position in positions:
                if not ((position[0] >= 9 and position[1] < 6) or (position[0] < 6 and position[1] >= 9)):
                    ButtonName = "%02d %02d" % (position[0] + 1, position[1] + 1)
                    Button = self.new.findChild(QPushButton, ButtonName)
                    Button.setText("")
        for position in positions:
            if not ((position[0] >= 9 and position[1] < 6) or (position[0] < 6 and position[1] >= 9)):
                ButtonName = "%02d %02d" % (position[0] + 1, position[1] + 1)
                Button = self.new.findChild(QPushButton, ButtonName)
                if L1[position[0]][position[1]] != '0':
                    Button.setText(L1[position[0]][position[1]])
                    Button.setStyleSheet("")
                    Origin.append(ButtonName)
                if L2[position[0]][position[1]] != '0' and L1[position[0]][position[1]] == '0':
                    Ans.append([position[0] + 1, position[1] + 1, L2[position[0]][position[1]]])
        return string

    def buttonClick(self):
        global First, Ans, Origin, Sudoku, themeFile
        btn = self.sender()
        btnName = btn.objectName()
        if btnName == "Start":
            string = self.SudokuLevel.currentText()
            holes = int(re.findall("\d+\.?\d*", string)[0])
            with open("record/record.info", "rb") as f:
                data = f.read().decode("utf-8")
                data = data.split("\n")
                a = int(data[holes - 1])
                if a == 99999999:
                    s = "No record yet"
                else:
                    s = "Best record: %02d : %02d" % (
                        a / 6000, a % 6000 / 100)
                self.RecordLabel.setText(s)
            Sudoku.Sudoku(holes)
            if self.SudokuInit() != "":
                self.TipLabel.setStyleSheet("font-size: 12px;padding-left: 5px;")
                self.TipLabel.setText("Sudoku has no unique ans")
            else:
                self.TipLabel.setStyleSheet("background-color:transparent;")
                self.TipLabel.setText("")
            self.TimerLabel.start()
        elif btnName == "Stop":
            self.TimerLabel.stop()
        elif btnName == "Restart":
            self.SudokuInit()
            self.TimerLabel.restart()
        elif btnName == "Tip":
            if len(Ans) != 0:
                tip = choice(Ans)
                position = Ans.index(tip)
                Ans.pop(position)
                ButtonName = "%02d %02d" % (tip[0], tip[1])
                Origin.append(ButtonName)
                Button = self.new.findChild(QPushButton, ButtonName)
                Button.setText(tip[2])
                Button.setStyleSheet("")
            else:
                print("Finished")
        if btnName == "Submit":
            time = self.TimerLabel.a
            self.TimerLabel.end()
            with open("sudoku/sudoku.res", "w") as f:
                for i in range(15):
                    for j in range(15):
                        if not ((i >= 9 and j < 6) or (i < 6 and j >= 9)):
                            ButtonName = "%02d %02d" % (i + 1, j + 1)
                            Button = self.new.findChild(QPushButton, ButtonName)
                            if Button.text() == "":
                                self.Tip("You did not finish yet!")
                                return
                            f.write("{} ".format(Button.text()))
                    f.write("\n")
            res = Sudoku.SudokuDPLL()
            if res == 0:
                self.Tip("The ans is wrong")
            else:
                string = self.SudokuLevel.currentText()
                holes = int(re.findall("\d+\.?\d*", string)[0]) - 1
                t = self.TimerLabel.text().strip(" ")
                with open("record/record.info", "rb") as f:
                    data = f.read().decode("utf-8")
                    data = data.split("\n")
                    if time <= int(data[holes]):
                        data[holes] = str(time)
                        with open("record/record.info", "wb") as fp:
                            for i in data:
                                i += "\n"
                                i = i.encode("utf-8")
                                fp.write(i)
                        t = "New record:" + t
                        self.RecordLabel.setText("Best record: " + t)
                    self.Tip(t)
        if btnName == "btn_home":
            self.stackedWidget.setCurrentWidget(self.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
            self.animation = QPropertyAnimation(self.leftMenuBg, b"minimumWidth")
            a = self.leftMenuBg.width()
            width = a if a == Settings.MENU_WIDTH else 60

            self.animation.setDuration(Settings.TIME_ANIMATION)
            self.animation.setStartValue(width)
            self.animation.setEndValue(Settings.MENU_WIDTH)
            self.animation.setEasingCurve(QEasingCurve.Type.InOutQuart)
            self.animation.start()
        if btnName == "Game_Sudoku":
            self.stackedWidget.setCurrentWidget(self.new)  # SET PAGE
            UIFunctions.resetStyle(self, btnName)  # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))  # SELECT MENU
            self.animation = QPropertyAnimation(self.leftMenuBg, b"minimumWidth")
            a = self.leftMenuBg.width()
            width = a if a == Settings.MENU_WIDTH else 60

            self.animation.setDuration(Settings.TIME_ANIMATION)
            self.animation.setStartValue(width)
            self.animation.setEndValue(Settings.MENU_WIDTH)
            self.animation.setEasingCurve(QEasingCurve.Type.InOutQuart)
            self.animation.start()
        if btnName == "more":
            QDesktopServices.openUrl(QUrl("https://github.com/EI233"))
        if btnName == "Adjustments":
            if themeFile == "Qss/py_dracula_light.qss":
                themeFile = "Qss/py_dracula_dark.qss"
                self.HomeDecription.setHtml(Dark_Home)
            else:
                themeFile = "Qss/py_dracula_light.qss"
                self.HomeDecription.setHtml(Light_Home)
            UIFunctions.theme(self, themeFile, True)
        if btnName=="share":
            QDesktopServices.openUrl(QUrl("https://github.com/EI233/sudoku"))
    def ButtonClick(self):
        btn = self.sender()
        btnName = btn.objectName()
        if self.SudokuLevel.hasFocus():
            self.SudokuLevel.clearFocus()
        self.ButtonStyle(btn, btnName)

    def ButtonStyle(self, btn: QPushButton, btnName: str):
        global name, s2, Ans, Origin
        if len(btn.text()) > 6:
            btn.setStyleSheet("	background-color: rgb(153,204,255); color:rgb(255,255,102);" + s2)
        else:
            if btnName not in Origin:
                btn.setStyleSheet("	background-color: rgb(153,204,255);color:rgb(255,255,102);")
            else:
                btn.setStyleSheet("	background-color: rgb(153,204,255);")
        if name != btnName and name is not None:
            Button = self.new.findChild(QPushButton, name)
            if name in Origin:
                Button.setStyleSheet("")
            else:
                if len(Button.text()) > 6:
                    Button.setStyleSheet(s2 + "color:rgb(255,255,102);")
                else:
                    Button.setStyleSheet("color:rgb(255,255,102);")
        name = btnName

    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

        # MOUSE CLICK EVENTS
        # ///////////////////////////////////////////////////////////////

    def max2normal(self):
        # IF MAXIMIZED CHANGE TO NORMAL
        if UIFunctions.returStatus(self):
            UIFunctions.maximize_restore(self)

    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        if self._isTracking:
            self._endPos = e.globalPosition().toPoint() - self._startPos
            self.move(self._O + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.pos().x() <= 50:
            UIFunctions.toggleMenu(self, True)
        if e.button() == Qt.MouseButton.LeftButton:
            self._isTracking = True
            self._O = e.globalPosition().toPoint() - e.pos()
            self._startPos = e.globalPosition().toPoint()

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.MouseButton.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

    def keyPressEvent(self, event):
        global name, Origin, s1, s2
        if event.key() == Qt.Key.Key_Down:
            if not (int(name.split(" ")[0]) == 15 or (int(name.split(" ")[0]) == 9 and int(name.split(" ")[1]) <= 6)):
                ButtonName = "%02d %02d" % (int(name.split(" ")[0]) + 1, int(name.split(" ")[1]))
                Button = self.new.findChild(QPushButton, ButtonName)
                self.ButtonStyle(Button, ButtonName)
        if event.key() == Qt.Key.Key_Up:
            if not (int(name.split(" ")[0]) == 1 or (int(name.split(" ")[0]) == 7 and int(name.split(" ")[1]) > 9)):
                ButtonName = "%02d %02d" % (int(name.split(" ")[0]) - 1, int(name.split(" ")[1]))
                Button = self.new.findChild(QPushButton, ButtonName)
                self.ButtonStyle(Button, ButtonName)
        if event.key() == Qt.Key.Key_Right:
            if not (int(name.split(" ")[1]) == 15 or (int(name.split(" ")[1]) == 9 and int(name.split(" ")[0]) <= 6)):
                ButtonName = "%02d %02d" % (int(name.split(" ")[0]), int(name.split(" ")[1]) + 1)
                Button = self.new.findChild(QPushButton, ButtonName)
                self.ButtonStyle(Button, ButtonName)
        if event.key() == Qt.Key.Key_Left:
            if not (int(name.split(" ")[1]) == 1 or (int(name.split(" ")[1]) == 7 and int(name.split(" ")[0]) > 9)):
                ButtonName = "%02d %02d" % (int(name.split(" ")[0]), int(name.split(" ")[1]) - 1)
                Button = self.new.findChild(QPushButton, ButtonName)
                self.ButtonStyle(Button, ButtonName)
        if name not in Origin and name is not None:
            Button = self.new.findChild(QPushButton, name=name)
            if Qt.Key.Key_9 >= event.key() >= Qt.Key.Key_1:
                val = str(event.key() - Qt.Key.Key_0)
                if Button.text() != "":
                    if val not in Button.text():
                        s = Button.text().replace("\n", "")
                        val = val + ",%s" % s
                        if 12 >= len(val) >= 6:
                            val = val[0:6] + "\n" + val[6:]
                            Button.setStyleSheet(s2 + "	background-color: rgb(153,204,255); color:rgb(255,255,102);")
                        elif len(val) > 12:
                            Button.setStyleSheet(s2 + "	background-color: rgb(153,204,255); color:rgb(255,255,102);")
                            val = val[0:6] + "\n" + val[6:12] + "\n" + val[12:]
                    else:
                        val = Button.text()
                Button.setText(val)
            if event.key() == Qt.Key.Key_Backspace:
                if 0 >= len(Button.text()) <= 1:
                    Button.setText("")
                else:
                    val = Button.text()
                    if len(val) == 8:
                        Button.setStyleSheet(s1 + "	background-color: rgb(153,204,255); color:rgb(255,255,102);")
                        val = val[:-3]
                    elif len(val) == 15:
                        Button.setStyleSheet(s2 + "	background-color: rgb(153,204,255); color:rgb(255,255,102);")
                        val = val[:-3]
                    else:
                        val = val[:-2]
                    Button.setText(val)

    def TextChanged(self):
        text = self.SudokuLevel.currentText()
        if text == "Personalize":
            self.SudokuLevel.setCurrentText("Personalize:")
            self.SudokuLevel.LineEdit.setReadOnly(False)
        elif text == "Personalize:":
            pass
        else:
            with open("record/record.info", "rb") as f:
                string = self.SudokuLevel.currentText()
                holes = int(re.findall("\d+\.?\d*", string)[0])
                if holes > 153:
                    self.Tip("       too many holes")
                    return
                data = f.read().decode("utf-8")
                data = data.split("\n")
                a = int(data[holes - 1])
                if a == 99999999:
                    s = "No record yet"
                else:
                    s = "Best record: %02d : %02d" % (
                        a / 6000, a % 6000 / 100)
                self.RecordLabel.setText(s)

    def Edit(self):
        text = self.SudokuLevel.currentText()
        if text == "Personalize":
            self.SudokuLevel.setCurrentText("Personalize:")
            self.SudokuLevel.LineEdit.setReadOnly(False)
        elif text == "Personalize:":
            self.SudokuLevel.LineEdit.setReadOnly(False)
        else:
            with open("record/record.info", "rb") as f:
                string = self.SudokuLevel.currentText()
                holes = int(re.findall("\d+\.?\d*", string)[0]) - 1
                data = f.read().decode("utf-8")
                data = data.split("\n")
                a = int(data[holes - 1])
                if a == 99999999:
                    s = "No record yet"
                else:
                    s = "Best record: %02d : %02d" % (
                        a / 6000, a % 6000 / 100)
                self.RecordLabel.setText(s)
            self.SudokuLevel.LineEdit.setReadOnly(True)

    def Tip(self, param: str):
        self.TipBox.setText(param)


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    ex = MainWindow()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
