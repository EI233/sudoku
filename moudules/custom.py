from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *



class ok(QPushButton):
    def __init__(self, parent=None):
        super(QPushButton, self).__init__(parent)

    def paintEvent(self, event):
        pat2 = QPainter(self)
        pat2.setRenderHint(pat2.RenderHint.Antialiasing)  # 抗锯齿
        pat2.setBrush(QColor(52, 59, 72, 255))
        pat2.setPen(QColor(0, 0, 0, 0))
        rect = self.rect()
        rect.setLeft(9)
        rect.setTop(9)
        rect.setWidth(rect.width() - 9)
        rect.setHeight(rect.height() - 9)
        pat2.drawRoundedRect(rect, 4, 4)
        pat2.setPen(QColor(255, 255, 255, 255))
        pat2.setFont(QFont("Microsoft YaHei", 10))
        pat2.drawText(rect, Qt.AlignmentFlag.AlignCenter, "确定")


class Myexit(QPushButton):
    def __init__(self, parent=None):
        super(QPushButton, self).__init__(parent)

    def paintEvent(self, event):
        pat2 = QPainter(self)
        pat2.setRenderHint(pat2.RenderHint.Antialiasing)  # 抗锯齿
        pat2.setBrush(QColor(52, 59, 72, 255))
        pat2.setPen(QColor(0, 0, 0, 0))
        rect = self.rect()
        rect.setLeft(9)
        rect.setTop(9)
        rect.setWidth(rect.width() - 9)
        rect.setHeight(rect.height() - 9)
        pat2.drawRoundedRect(rect, 4, 4)
        pat2.drawImage(rect, QImage("images/icons/icon_close.png"))


class MessageBox(QDialog):
    def __init__(self, msg, parent=None, ):
        super(MessageBox, self).__init__(parent)
        self.msg = msg
        self.border_width = 8
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.resize(QSize(300, 200))
        self.ok = ok(self)
        self.ok.move(115, 140)
        self.ok.resize(75, 45)
        self.exit = Myexit(self)
        self.exit.move(255, 0)
        self.exit.resize(45, 45)

    def paintEvent(self, event):
        path = QPainterPath()
        path.setFillRule(Qt.FillRule.WindingFill)
        pat = QPainter(self)
        pat.setRenderHint(pat.RenderHint.Antialiasing)
        pat.fillPath(path, QBrush(QColor(33, 37, 43,255)))
        color = QColor(192, 192, 192, 50)
        for i in range(5):
            i_path = QPainterPath()
            i_path.setFillRule(Qt.FillRule.WindingFill)
            ref = QRectF(5 - i, 5 - i, self.width() - (5 - i) * 2, self.height() - (5 - i) * 2)
            i_path.addRoundedRect(ref, self.border_width, self.border_width)
            color.setAlpha(150 - int(i ** 0.5) * 50)
            pat.setPen(color)
            pat.drawPath(i_path)
        pat2 = QPainter(self)
        pat2.setRenderHint(pat2.RenderHint.Antialiasing)  # 抗锯齿
        pat2.setBrush(QColor(44, 49, 60, 255))
        pat2.setPen(QColor(0, 0, 0, 0))
        rect = self.rect()
        rect.setLeft(9)
        rect.setTop(9)
        rect.setWidth(rect.width() - 9)
        rect.setHeight(rect.height() - 9)
        pat2.drawRoundedRect(rect, 4, 4)
        pat2.setPen(QColor(255, 255, 255, 255))
        pat2.setFont(QFont("Microsoft YaHei", 15))
        pat2.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.msg)


class CustomGrip(QWidget):
    def __init__(self, parent, position, disable_color=False):

        # SETUP UI
        QWidget.__init__(self)
        self.parent = parent
        self.setParent(parent)
        self.wi = Widgets()

        # SHOW TOP GRIP
        if position == Qt.Edge.TopEdge:
            self.wi.top(self)
            self.setGeometry(0, 0, self.parent.width(), 10)
            self.setMaximumHeight(10)

            # GRIPS
            top_left = QSizeGrip(self.wi.top_left)
            top_right = QSizeGrip(self.wi.top_right)

            # RESIZE TOP
            def resize_top(event):
                delta = event.pos()
                height = max(self.parent.minimumHeight(), self.parent.height() - delta.y())
                geo = self.parent.geometry()
                geo.setTop(geo.bottom() - height)
                self.parent.setGeometry(geo)
                event.accept()

            self.wi.top.mouseMoveEvent = resize_top

            # ENABLE COLOR
            if disable_color:
                self.wi.top_left.setStyleSheet("background: transparent")
                self.wi.top_right.setStyleSheet("background: transparent")
                self.wi.top.setStyleSheet("background: transparent")

        # SHOW BOTTOM GRIP
        elif position == Qt.Edge.BottomEdge:
            self.wi.bottom(self)
            self.setGeometry(0, self.parent.height() - 10, self.parent.width(), 10)
            self.setMaximumHeight(10)

            # GRIPS
            self.bottom_left = QSizeGrip(self.wi.bottom_left)
            self.bottom_right = QSizeGrip(self.wi.bottom_right)

            # RESIZE BOTTOM
            def resize_bottom(event):
                delta = event.pos()
                height = max(self.parent.minimumHeight(), self.parent.height() + delta.y())
                self.parent.resize(self.parent.width(), height)
                event.accept()

            self.wi.bottom.mouseMoveEvent = resize_bottom

            # ENABLE COLOR
            if disable_color:
                self.wi.bottom_left.setStyleSheet("background: transparent")
                self.wi.bottom_right.setStyleSheet("background: transparent")
                self.wi.bottom.setStyleSheet("background: transparent")

        # SHOW LEFT GRIP
        elif position == Qt.Edge.LeftEdge:
            self.wi.left(self)
            self.setGeometry(0, 10, 10, self.parent.height())
            self.setMaximumWidth(10)

            # RESIZE LEFT
            def resize_left(event):
                delta = event.pos()
                width = max(self.parent.minimumWidth(), self.parent.width() - delta.x())
                geo = self.parent.geometry()
                geo.setLeft(geo.right() - width)
                self.parent.setGeometry(geo)
                event.accept()

            self.wi.leftgrip.mouseMoveEvent = resize_left

            # ENABLE COLOR
            if disable_color:
                self.wi.leftgrip.setStyleSheet("background: transparent")

        # RESIZE RIGHT
        elif position == Qt.Edge.RightEdge:
            self.wi.right(self)
            self.setGeometry(self.parent.width() - 10, 10, 10, self.parent.height())
            self.setMaximumWidth(10)

            def resize_right(event):
                delta = event.pos()
                width = max(self.parent.minimumWidth(), self.parent.width() + delta.x())
                self.parent.resize(width, self.parent.height())
                event.accept()

            self.wi.rightgrip.mouseMoveEvent = resize_right

            # ENABLE COLOR
            if disable_color:
                self.wi.rightgrip.setStyleSheet("background: transparent")

    def mouseReleaseEvent(self, event):
        self.mousePos = None

    def resizeEvent(self, event):
        if hasattr(self.wi, 'container_top'):
            self.wi.container_top.setGeometry(0, 0, self.width(), 10)

        elif hasattr(self.wi, 'container_bottom'):
            self.wi.container_bottom.setGeometry(0, 0, self.width(), 10)

        elif hasattr(self.wi, 'leftgrip'):
            self.wi.leftgrip.setGeometry(0, 0, 10, self.height() - 20)

        elif hasattr(self.wi, 'rightgrip'):
            self.wi.rightgrip.setGeometry(0, 0, 10, self.height() - 20)


class Widgets(object):
    def top(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        self.container_top = QFrame(Form)
        self.container_top.setObjectName(u"container_top")
        self.container_top.setGeometry(QRect(0, 0, 500, 10))
        self.container_top.setMinimumSize(QSize(0, 10))
        self.container_top.setMaximumSize(QSize(16777215, 10))
        self.container_top.setFrameShape(QFrame.frameShape(self.container_top).NoFrame)
        self.container_top.setFrameShadow(QFrame.frameShadow(self.container_top).Raised)
        self.top_layout = QHBoxLayout(self.container_top)
        self.top_layout.setSpacing(0)
        self.top_layout.setObjectName(u"top_layout")
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_left = QFrame(self.container_top)
        self.top_left.setObjectName(u"top_left")
        self.top_left.setMinimumSize(QSize(10, 10))
        self.top_left.setMaximumSize(QSize(10, 10))
        self.top_left.setCursor(QCursor(Qt.CursorShape.SizeFDiagCursor))
        self.top_left.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.top_left.setFrameShape(QFrame.frameShape(self.top_left).NoFrame)
        self.top_left.setFrameShadow(QFrame.frameShadow(self.top_left).Raised)
        self.top_layout.addWidget(self.top_left)
        self.top = QFrame(self.container_top)
        self.top.setObjectName(u"top")
        self.top.setCursor(QCursor(Qt.CursorShape.SizeVerCursor))
        self.top.setStyleSheet(u"background-color: rgb(85, 255, 255);")
        self.top.setFrameShape(QFrame.frameShape(self.top).NoFrame)
        self.top.setFrameShadow(QFrame.frameShadow(self.top).Raised)
        self.top_layout.addWidget(self.top)
        self.top_right = QFrame(self.container_top)
        self.top_right.setObjectName(u"top_right")
        self.top_right.setMinimumSize(QSize(10, 10))
        self.top_right.setMaximumSize(QSize(10, 10))
        self.top_right.setCursor(QCursor(Qt.CursorShape.SizeBDiagCursor))
        self.top_right.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.top_right.setFrameShape(QFrame.frameShape(self.top_right).NoFrame)
        self.top_right.setFrameShadow(QFrame.frameShadow(self.top_right).Raised)
        self.top_layout.addWidget(self.top_right)

    def bottom(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        self.container_bottom = QFrame(Form)
        self.container_bottom.setObjectName(u"container_bottom")
        self.container_bottom.setGeometry(QRect(0, 0, 500, 10))
        self.container_bottom.setMinimumSize(QSize(0, 10))
        self.container_bottom.setMaximumSize(QSize(16777215, 10))
        self.container_bottom.setFrameShape(QFrame.frameShape(self.container_bottom).NoFrame)
        self.container_bottom.setFrameShadow(QFrame.frameShadow(self.container_bottom).Raised)
        self.bottom_layout = QHBoxLayout(self.container_bottom)
        self.bottom_layout.setSpacing(0)
        self.bottom_layout.setObjectName(u"bottom_layout")
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_left = QFrame(self.container_bottom)
        self.bottom_left.setObjectName(u"bottom_left")
        self.bottom_left.setMinimumSize(QSize(10, 10))
        self.bottom_left.setMaximumSize(QSize(10, 10))
        self.bottom_left.setCursor(QCursor(Qt.CursorShape.SizeBDiagCursor))
        self.bottom_left.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.bottom_left.setFrameShape(QFrame.frameShape(self.bottom_left).NoFrame)
        self.bottom_left.setFrameShadow(QFrame.frameShadow(self.bottom_left).Raised)
        self.bottom_layout.addWidget(self.bottom_left)
        self.bottom = QFrame(self.container_bottom)
        self.bottom.setObjectName(u"bottom")
        self.bottom.setCursor(QCursor(Qt.CursorShape.SizeVerCursor))
        self.bottom.setStyleSheet(u"background-color: rgb(85, 170, 0);")
        self.bottom.setFrameShape(QFrame.frameShape(self.bottom).NoFrame)
        self.bottom.setFrameShadow(QFrame.frameShadow(self.bottom).Raised)
        self.bottom_layout.addWidget(self.bottom)
        self.bottom_right = QFrame(self.container_bottom)
        self.bottom_right.setObjectName(u"bottom_right")
        self.bottom_right.setMinimumSize(QSize(10, 10))
        self.bottom_right.setMaximumSize(QSize(10, 10))
        self.bottom_right.setCursor(QCursor(Qt.CursorShape.SizeFDiagCursor))
        self.bottom_right.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.bottom_right.setFrameShape(QFrame.frameShape(self.bottom_right).NoFrame)
        self.bottom_right.setFrameShadow(QFrame.frameShadow(self.bottom_right).Raised)
        self.bottom_layout.addWidget(self.bottom_right)

    def left(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        self.leftgrip = QFrame(Form)
        self.leftgrip.setObjectName(u"left")
        self.leftgrip.setGeometry(QRect(0, 10, 10, 480))
        self.leftgrip.setMinimumSize(QSize(10, 0))
        self.leftgrip.setCursor(QCursor(Qt.CursorShape.SizeHorCursor))
        self.leftgrip.setStyleSheet(u"background-color: rgb(255, 121, 198);")
        self.leftgrip.setFrameShape(QFrame.frameShape(self.leftgrip).NoFrame)
        self.leftgrip.setFrameShadow(QFrame.frameShadow(self.leftgrip).Raised)

    def right(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(500, 500)
        self.rightgrip = QFrame(Form)
        self.rightgrip.setObjectName(u"right")
        self.rightgrip.setGeometry(QRect(0, 0, 10, 500))
        self.rightgrip.setMinimumSize(QSize(10, 0))
        self.rightgrip.setCursor(QCursor(Qt.CursorShape.SizeHorCursor))
        self.rightgrip.setStyleSheet(u"background-color: rgb(255, 0, 127);")
        self.rightgrip.setFrameShape(QFrame.frameShape(self.rightgrip).NoFrame)
        self.rightgrip.setFrameShadow(QFrame.frameShadow(self.rightgrip).Raised)
