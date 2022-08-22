# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# MAIN FILE
# ///////////////////////////////////////////////////////////////
from PyQt6.QtCore import QPropertyAnimation, Qt, QParallelAnimationGroup, QEvent, QTimer, QSize
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QSizeGrip, QPushButton

# GLOBALS
# ///////////////////////////////////////////////////////////////
from .custom import CustomGrip
from main import *

GLOBAL_STATE = False
GLOBAL_TITLE_BAR = True


class UIFunctions(MainWindow):
    # MAXIMIZE/RESTORE
    # ///////////////////////////////////////////////////////////////
    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == False:
            self.showFullScreen()
            GLOBAL_STATE = True
            self.appMargins.setContentsMargins(0, 0, 0, 0)
            self.maximizeRestoreAppBtn.setToolTip("Restore")
            self.maximizeRestoreAppBtn.setIcon(QIcon(u"icons/solid/window-restore.svg"))
            self.maximizeRestoreAppBtn.setMinimumSize(QSize(25, 25))
            self.maximizeRestoreAppBtn.setMaximumSize(QSize(25, 25))
            self.left_grip.hide()
            self.right_grip.hide()
            self.top_grip.hide()
            self.bottom_grip.hide()
        else:
            GLOBAL_STATE = False
            self.showNormal()
            self.appMargins.setContentsMargins(10, 10, 10, 10)
            self.maximizeRestoreAppBtn.setToolTip("Maximize")
            self.maximizeRestoreAppBtn.setIcon(QIcon("icons/solid/window-maximize.svg"))
            self.left_grip.show()
            self.right_grip.show()
            self.top_grip.show()
            self.bottom_grip.show()

    # RETURN STATUS
    # ///////////////////////////////////////////////////////////////
    def returStatus(self):
        return GLOBAL_STATE

    # SET STATUS
    # ///////////////////////////////////////////////////////////////
    def setStatus(self, status):
        global GLOBAL_STATE
        GLOBAL_STATE = status

    # TOGGLE MENU
    # ///////////////////////////////////////////////////////////////
    def toggleMenu(self, enable=True):
        Widget = self.stackedWidget.currentWidget()
        N = Widget.objectName()
        width = self.leftMenuBg.width()
        maxExtend = Settings.MENU_WIDTH
        standard = 60
        # SET MAX WIDTH
        if width == 60:
            widthExtended = maxExtend

        else:
            widthExtended = standard

        # ANIMATION

        self.animation = QPropertyAnimation(self.leftMenuBg, b"minimumWidth")
        self.animation.setDuration(Settings.TIME_ANIMATION)
        self.animation.setStartValue(width)
        self.animation.setEndValue(widthExtended)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuart)
        self.animation.start()

    # TOGGLE LEFT BOX
    # ///////////////////////////////////////////////////////////////
    def toggleLeftBox(self, enable):
        if enable:
            # GET WIDTH
            width = self.extraLeftBox.width()
            widthRightBox = self.RightBox.width()
            maxExtend = Settings.LEFT_BOX_WIDTH
            color = Settings.BTN_LEFT_BOX_COLOR
            standard = 0

            # GET BTN STYLE
            style = self.toggleLeftBox.styleSheet()

            # SET MAX WIDTH
            if width == 0:
                widthExtended = maxExtend
                # SELECT BTN
                self.toggleLeftBox.setStyleSheet(style + color)
                if widthRightBox != 0:
                    style = self.settingsTopBtn.styleSheet()
                    self.settingsTopBtn.setStyleSheet(style.replace(Settings.BTN_RIGHT_BOX_COLOR, ''))
            else:
                widthExtended = standard
                # RESET BTN
                self.toggleLeftBox.setStyleSheet(style.replace(color, ''))

            UIFunctions.start_box_animation(self, width, widthRightBox, "left")

    # TOGGLE RIGHT BOX
    # ///////////////////////////////////////////////////////////////
    def toggleRightBox(self, enable):
        if enable:
            # GET WIDTH
            width = self.RightBox.width()
            widthLeftBox = self.extraLeftBox.width()
            maxExtend = Settings.RIGHT_BOX_WIDTH
            color = Settings.BTN_RIGHT_BOX_COLOR
            standard = 0

            # GET BTN STYLE
            style = self.settingsTopBtn.styleSheet()
            # SET MAX WIDTH
            if width == 0:
                widthExtended = maxExtend
                # SELECT BTN
                self.settingsTopBtn.setStyleSheet(style + color)
                if widthLeftBox != 0:
                    style = self.toggleLeftBox.styleSheet()
                    self.toggleLeftBox.setStyleSheet(style.replace(Settings.BTN_LEFT_BOX_COLOR, ''))

            else:
                widthExtended = standard
                # RESET BTN
                self.settingsTopBtn.setStyleSheet(style.replace(color, ''))

            UIFunctions.start_box_animation(self, widthLeftBox, width, "right")

    def start_box_animation(self, left_box_width, right_box_width, direction):
        right_width = 0
        left_width = 0
        s = ""
        # Check values
        if left_box_width == 0 and direction == "left":
            left_width = 240
            s = "#Tip { padding-left: 0px;text-align:center;}" \
                "#Stop { padding-left: 0px;text-align:center;}" \
                "#Start { padding-left: 0px;text-align:center;}" \
                "#Restart {padding-left: 0px;text-align:center;}"
            self.RightFrame = QPropertyAnimation(self.RightMenu, b"minimumWidth")
            self.RightFrame.setDuration(Settings.TIME_ANIMATION)
            self.RightFrame.setStartValue(225)
            self.RightFrame.setEndValue(150)
            self.RightFrame.setEasingCurve(QEasingCurve.Type.InOutQuart)

        if left_box_width != 0 and direction == "left":
            s = "#Tip { padding-left: 50px;text-align:left;}" \
                "#Stop { padding-left: 50px;text-align:left;}" \
                "#Start { padding-left: 50px;text-align:left;}" \
                "#Restart { padding-left: 50px;text-align:left;}"
            left_width = 0
            self.RightFrame = QPropertyAnimation(self.RightMenu, b"minimumWidth")
            self.RightFrame.setDuration(Settings.TIME_ANIMATION)
            self.RightFrame.setStartValue(150)
            self.RightFrame.setEndValue(225)
            self.RightFrame.setEasingCurve(QEasingCurve.Type.InOutQuart)
        # Check values
        if right_box_width == 0 and direction == "right":
            right_width = 160
            self.RightFrame = QPropertyAnimation(self.RightMenu, b"minimumWidth")
            self.RightFrame.setDuration(Settings.TIME_ANIMATION)
            self.RightFrame.setStartValue(225)
            self.RightFrame.setEndValue(150)
            self.RightFrame.setEasingCurve(QEasingCurve.Type.InOutQuart)
        if right_box_width != 0 and direction == "right":
            right_width = 0
            self.RightFrame = QPropertyAnimation(self.RightMenu, b"minimumWidth")
            self.RightFrame.setDuration(Settings.TIME_ANIMATION)
            self.RightFrame.setStartValue(150)
            self.RightFrame.setEndValue(225)
            self.RightFrame.setEasingCurve(QEasingCurve.Type.InOutQuart)

            # ANIMATION LEFT BOX
        self.left_box = QPropertyAnimation(self.extraLeftBox, b"minimumWidth")
        self.left_box.setDuration(Settings.TIME_ANIMATION)
        self.left_box.setStartValue(left_box_width)
        self.left_box.setEndValue(left_width)
        self.left_box.setEasingCurve(QEasingCurve.Type.InOutQuart)

        # ANIMATION RIGHT BOX        
        self.right_box = QPropertyAnimation(self.RightBox, b"minimumWidth")
        self.right_box.setDuration(Settings.TIME_ANIMATION)
        self.right_box.setStartValue(right_box_width)
        self.right_box.setEndValue(right_width)
        self.right_box.setEasingCurve(QEasingCurve.Type.InOutQuart)

        # GROUP ANIMATION
        self.group = QParallelAnimationGroup()
        self.group.addAnimation(self.left_box)
        self.group.addAnimation(self.right_box)
        self.group.addAnimation(self.RightFrame)
        self.group.start()
        self.new.setStyleSheet(self.new.styleSheet() + s)

    # SELECT/DESELECT MENU
    # ///////////////////////////////////////////////////////////////
    # SELECT
    def selectMenu(getStyle):
        select = getStyle + Settings.MENU_SELECTED_STYLESHEET
        return select

    # DESELECT
    def deselectMenu(getStyle):
        deselect = getStyle.replace(Settings.MENU_SELECTED_STYLESHEET, "")
        return deselect

    # START SELECTION
    def selectStandardMenu(self, widget):
        for w in self.topMenu.findChildren(QPushButton):
            if w.objectName() == widget:
                w.setStyleSheet(UIFunctions.selectMenu(w.styleSheet()))

    # RESET SELECTION
    def resetStyle(self, widget):
        for w in self.topMenu.findChildren(QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(UIFunctions.deselectMenu(w.styleSheet()))

    # IMPORT THEMES FILES QSS/CSS
    # ///////////////////////////////////////////////////////////////
    def theme(self, file, useCustomTheme):
        if useCustomTheme:
            str = open(file, 'r').read()
            self.styleSheet.setStyleSheet(str)

    # START - GUI DEFINITIONS
    # ///////////////////////////////////////////////////////////////
    def uiDefinitions(self):
        def dobleClickMaximizeRestore(event):
            # IF DOUBLE CLICK CHANGE STATUS
            if event.type() == QEvent.Type.MouseButtonDblClick:
                QTimer.singleShot(250, lambda: UIFunctions.maximize_restore(self))

        self.titleRightInfo.mouseDoubleClickEvent = dobleClickMaximizeRestore

        if Settings.ENABLE_CUSTOM_TITLE_BAR:
            # STANDARD TITLE BAR
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

            # MOVE WINDOW / MAXIMIZE / RESTORE

            # CUSTOM GRIPS
            self.left_grip = CustomGrip(self, Qt.Edge.LeftEdge, True)
            self.right_grip = CustomGrip(self, Qt.Edge.RightEdge, True)
            self.top_grip = CustomGrip(self, Qt.Edge.TopEdge, True)
            self.bottom_grip = CustomGrip(self, Qt.Edge.BottomEdge, True)

        else:
            self.appMargins.setContentsMargins(0, 0, 0, 0)
            self.minimizeAppBtn.hide()
            self.maximizeRestoreAppBtn.hide()
            self.closeAppBtn.hide()

        # DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.bgApp.setGraphicsEffect(self.shadow)

        # RESIZE WINDOW
        # self.sizegrip = QSizeGrip(self.frame_size_grip)
        # self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

        # MINIMIZE
        self.minimizeAppBtn.clicked.connect(lambda: self.showMinimized())

        # MAXIMIZE/RESTORE
        self.maximizeRestoreAppBtn.clicked.connect(lambda: UIFunctions.maximize_restore(self))

        # CLOSE APPLICATION
        self.closeAppBtn.clicked.connect(lambda: self.close())

    def resize_grips(self):
        if Settings.ENABLE_CUSTOM_TITLE_BAR:
            self.left_grip.setGeometry(0, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 10, 10, 10, self.height())
            self.top_grip.setGeometry(0, 0, self.width(), 10)
            self.bottom_grip.setGeometry(0, self.height() - 10, self.width(), 10)

    # ///////////////////////////////////////////////////////////////
