# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'justboxd.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QScrollArea, QSizePolicy, QStackedWidget, QWidget)

class Ui_justboxdWindow(QWidget):
    def setupUi(self, justboxdWindow):
        if not justboxdWindow.objectName():
            justboxdWindow.setObjectName(u"justboxdWindow")
        justboxdWindow.resize(503, 567)
        justboxdWindow.setAutoFillBackground(True)
        self.stackedWidget = QStackedWidget(justboxdWindow)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(0, 0, 501, 561))
        self.stackedWidget.setMouseTracking(True)
        self.serviceSelectionPage = QWidget()
        self.serviceSelectionPage.setObjectName(u"serviceSelectionPage")
        self.gridLayoutWidget_2 = QWidget(self.serviceSelectionPage)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(30, 120, 441, 181))
        self.availableServicesLayout = QGridLayout(self.gridLayoutWidget_2)
        self.availableServicesLayout.setObjectName(u"availableServicesLayout")
        self.availableServicesLayout.setContentsMargins(0, 0, 0, 0)
        self.availableServicesScrollArea = QScrollArea(self.gridLayoutWidget_2)
        self.availableServicesScrollArea.setObjectName(u"availableServicesScrollArea")
        self.availableServicesScrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 437, 177))
        self.availableServicesScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.availableServicesLayout.addWidget(self.availableServicesScrollArea, 0, 0, 1, 1)

        self.gridLayoutWidget_3 = QWidget(self.serviceSelectionPage)
        self.gridLayoutWidget_3.setObjectName(u"gridLayoutWidget_3")
        self.gridLayoutWidget_3.setGeometry(QRect(30, 330, 441, 181))
        self.userServicesLayout = QGridLayout(self.gridLayoutWidget_3)
        self.userServicesLayout.setObjectName(u"userServicesLayout")
        self.userServicesLayout.setContentsMargins(0, 0, 0, 0)
        self.userServicesScrollArea = QScrollArea(self.gridLayoutWidget_3)
        self.userServicesScrollArea.setObjectName(u"userServicesScrollArea")
        self.userServicesScrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 437, 177))
        self.userServicesScrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.userServicesLayout.addWidget(self.userServicesScrollArea, 0, 0, 1, 1)

        self.serviceLookupLine = QLineEdit(self.serviceSelectionPage)
        self.serviceLookupLine.setObjectName(u"serviceLookupLine")
        self.serviceLookupLine.setGeometry(QRect(130, 80, 341, 21))
        self.serviceLookupLable = QLabel(self.serviceSelectionPage)
        self.serviceLookupLable.setObjectName(u"serviceLookupLable")
        self.serviceLookupLable.setGeometry(QRect(50, 80, 71, 20))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setBold(True)
        self.serviceLookupLable.setFont(font)
        self.serviceLookupLable.setLayoutDirection(Qt.LeftToRight)
        self.label_2 = QLabel(self.serviceSelectionPage)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(130, 20, 261, 31))
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(18)
        font1.setBold(True)
        self.label_2.setFont(font1)
        self.stackedWidget.addWidget(self.serviceSelectionPage)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.stack2HeaderLabel = QLabel(self.page_3)
        self.stack2HeaderLabel.setObjectName(u"stack2HeaderLabel")
        self.stack2HeaderLabel.setGeometry(QRect(130, 20, 621, 31))
        self.stack2HeaderLabel.setFont(font1)
        self.addressEntryLineEdit = QLineEdit(self.page_3)
        self.addressEntryLineEdit.setObjectName(u"addressEntryLineEdit")
        self.addressEntryLineEdit.setGeometry(QRect(180, 91, 221, 21))
        self.addressEntryLineEdit.setAcceptDrops(True)
        self.addressEntryLineEdit.setDragEnabled(True)
        self.dropBox = QWidget(self.page_3)
        self.dropBox.setObjectName(u"dropBox")
        self.dropBox.setGeometry(QRect(0, 150, 501, 411))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.dropBox.sizePolicy().hasHeightForWidth())
        self.dropBox.setSizePolicy(sizePolicy)
        self.dropBox.setMouseTracking(True)
        self.dropBox.setFocusPolicy(Qt.NoFocus)
        self.dropBox.setAutoFillBackground(True)
        self.dropBoxLabel = QLabel(self.dropBox)
        self.dropBoxLabel.setObjectName(u"dropBoxLabel")
        self.dropBoxLabel.setGeometry(QRect(170, 170, 171, 31))
        self.dropBoxLabel.setFont(font1)
        self.dropBoxLabel.setTextInteractionFlags(Qt.NoTextInteraction)
        self.addressEntryLabel = QLabel(self.page_3)
        self.addressEntryLabel.setObjectName(u"addressEntryLabel")
        self.addressEntryLabel.setGeometry(QRect(80, 91, 70, 20))
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.addressEntryLabel.sizePolicy().hasHeightForWidth())
        self.addressEntryLabel.setSizePolicy(sizePolicy1)
        self.stackedWidget.addWidget(self.page_3)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.stackedWidget.addWidget(self.page_2)

        self.retranslateUi(justboxdWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(justboxdWindow)
    # setupUi

    def retranslateUi(self, justboxdWindow):
        justboxdWindow.setWindowTitle(QCoreApplication.translate("justboxdWindow", u"Form", None))
        self.serviceLookupLable.setText(QCoreApplication.translate("justboxdWindow", u"Lookup", None))
        self.label_2.setText(QCoreApplication.translate("justboxdWindow", u"JustBoxd: Service Selection", None))
        self.stack2HeaderLabel.setText(QCoreApplication.translate("justboxdWindow", u"Select Letterboxd Content", None))
        self.dropBoxLabel.setText(QCoreApplication.translate("justboxdWindow", u"Drag URL Here", None))
        self.addressEntryLabel.setText(QCoreApplication.translate("justboxdWindow", u"Address", None))
    # retranslateUi

