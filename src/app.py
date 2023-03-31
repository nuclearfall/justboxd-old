import sys
import os
import justboxd
import pycountry
from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QApplication,
    QCompleter,
    QComboBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QButtonGroup
)


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        service_names = [val for val in justboxd.subscription_services.values()]
        country_code_list = [c.alpha_2 for c in pycountry.countries]
        self.my_services = justboxd.free_services
        
        self.setWindowTitle("JustBoxd")
        self.layout = QVBoxLayout()

        usernameLabel = QLabel("Letterboxd Username")
        self.usernameWidget = QLineEdit()
        self.layout.addWidget(usernameLabel)
        self.layout.addWidget(self.usernameWidget)

        listLabel = QLabel("Letterboxd List")
        self.listWidget = QLineEdit()
        self.layout.addWidget(listLabel)
        self.layout.addWidget(self.listWidget)
        self.listWidget.setText('watchlist')

        alpha2Label = QLabel("Country Code")
        self.country_codes = QComboBox()
        self.country_codes.addItems(country_code_list)
        self.country_codes.setCurrentIndex(country_code_list.index('US'))
        self.layout.addWidget(alpha2Label)
        self.layout.addWidget(self.country_codes)


        servicesLabel = QLabel("Select Services")
        self.lineEdit = QLineEdit()
        self.completer = QCompleter(service_names)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.InlineCompletion)
        # self.completer.highlighted.connect(self.add_service)
        self.completer.activated.connect(self.add_service)
        self.lineEdit.setCompleter(self.completer)
        self.lineEdit.returnPressed.connect(self.add_service)
        self.layout.addWidget(servicesLabel)
        self.layout.addWidget(self.lineEdit)

        self.box_layout = QVBoxLayout()
        self.box = QWidget()
        self.group = QButtonGroup()
        self.group.buttonClicked.connect(self.remove_service)
        removeServiceLabel = QLabel("Remove a Service Below")
        self.box.setLayout(self.box_layout)
        self.layout.addWidget(removeServiceLabel)
        self.layout.addWidget(self.box)

        self.searchButton = QPushButton("Search", self)
        self.searchButton.pressed.connect(self.submitSearch)
        self.layout.addWidget(self.searchButton)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def submitSearch(self):
        alpha2 = self.country_codes.currentText()
        username = self.usernameWidget.text()
        lbxd_list = self.listWidget.text()
        titles = justboxd.get_watchlist_titles(username, lbxd_list)
        services_short = [k for k in self.my_services.keys()]
        streaming_from = justboxd.get_streamers(titles,
                                services_short, country=alpha2)
        local_html = justboxd.save_json_to_html(streaming_from, 'streaming.html')
        local_html = 'file:///' + os.getcwd() + "/" + local_html
        QDesktopServices.openUrl(QUrl(local_html))


    def add_service(self):
        for k, v in justboxd.service_codes.items():
            if self.lineEdit.text() == v and v not in self.my_services.values():
                self.my_services[k] = v
                button = QPushButton(self.lineEdit.text())
                self.box_layout.addWidget(button)
                self.group.addButton(button)
        QTimer.singleShot(0, self.lineEdit.clear)

    def remove_service(self, button):
        for k, v in self.my_services.items():
            mark_for_deletion_key = None
            if v == button.text():
                mark_for_deletion_key = k
                button.setParent(None)
                self.group.removeButton(button)
                self.box_layout.removeWidget(button)
                self.layout.update()
        if mark_for_deletion_key:
            del(self.my_services[k])
            del(button)

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec_()
