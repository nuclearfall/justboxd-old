import sys
import os
import justboxd
import pycountry
import time
import traceback
import justbox_ui
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import (
    Qt, 
    QObject,
    QTimer, 
    QUrl, 
    QRunnable, 
    Slot, 
    Signal,
    QThreadPool
)
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


# retranslateUi
class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    '''
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)




class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @Slot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit() 

# Subclass QMainWindow to customize your application's main window
# class MainWindow(justboxdWindow):
#     def __init__(self):
#         super().__init__()

#         service_names = [val for val in justboxd.subscription_services.values()]
#         country_code_list = [c.alpha_2 for c in pycountry.countries]
#         self.my_services = justboxd.get_user_services()
#         self.threadpool = QThreadPool()

        # self.setWindowTitle("JustBoxd")
        # self.layout = QVBoxLayout()

        # urlLabel = QLabel("Letterboxd Url")
        # self.urlWidget = QLineEdit()
        # self.layout.addWidget(urlLabel)
        # self.layout.addWidget(self.urlWidget)

        # usernameLabel = QLabel("Letterboxd Username")
        # self.usernameWidget = QLineEdit()
        # self.layout.addWidget(usernameLabel)
        # self.layout.addWidget(self.usernameWidget)

        # listLabel = QLabel("Letterboxd List")
        # self.listWidget = QLineEdit()
        # self.layout.addWidget(listLabel)
        # self.layout.addWidget(self.listWidget)
        # self.listWidget.setText('watchlist')

        # alpha2Label = QLabel("Country Code")
        # self.country_codes = QComboBox()
        # self.country_codes.addItems(country_code_list)
        # self.country_codes.setCurrentIndex(country_code_list.index('US'))
        # self.layout.addWidget(alpha2Label)
        # self.layout.addWidget(self.country_codes)

        # servicesLabel = QLabel("Select Services")
        # self.lineEdit = QLineEdit()
        # completer = QCompleter(service_names)
        # completer.setCaseSensitivity(Qt.CaseInsensitive)
        # completer.setCompletionMode(QCompleter.InlineCompletion)
        # completer.activated.connect(self.addService)
        # self.lineEdit.setCompleter(completer)
        # self.lineEdit.returnPressed.connect(self.addService)
        # self.layout.addWidget(servicesLabel)
        # self.layout.addWidget(self.lineEdit)

        # self.box_layout = QVBoxLayout()
        # self.box = QWidget()
        # self.group = QButtonGroup()
        # self.group.buttonClicked.connect(self.remove_service)
        # removeServiceLabel = QLabel("Remove a Service Below")
        # self.box.setLayout(self.box_layout)
        # self.layout.addWidget(removeServiceLabel)
        # self.layout.addWidget(self.box)


        # self.saveServicesButton = QPushButton("Save Services", self)
        # self.saveServicesButton.pressed.connect(self.saveUserServices)
        # self.layout.addWidget(self.saveServicesButton)

        # self.searchButton = QPushButton("Search", self)
        # self.searchButton.pressed.connect(self.submitSearch)
        # self.layout.addWidget(self.searchButton)

        # self.widget = QWidget()
        # self.widget.setLayout(self.layout)
        # self.setCentralWidget(self.widget)

    # def saveUserServices(self):
    #     justboxd.save_user_services(self.my_services)

    # def submitSearch(self):
    #     self.searchButton.setEnabled(False)
    #     worker = Worker(self.serviceSearch) # Any other args, kwargs are passed to the run function
    #     worker.signals.result.connect(self.print_output)
    #     worker.signals.finished.connect(self.thread_complete)
    #     worker.signals.progress.connect(self.progress_fn)

    #     self.threadpool.start(worker)

    # def serviceSearch(self, progress_callback):
    #     alpha2 = self.country_codes.currentText()
    #     username = self.usernameWidget.text()
    #     list_name = self.listWidget.text()
    #     url_string = self.urlWidget.text()
    #     titles = justboxd.get_watchlist_titles(username=username, 
    #                                             url_string=url_string, list_name=list_name)
    #     services_short = [k for k in self.my_services.keys()]
    #     free_services_short = [k for k in justboxd.free_services.keys()]
    #     services_short = services_short + free_services_short
    #     streaming_from = justboxd.get_streamers(titles,
    #                             services_short, country=alpha2)
    #     local_html = justboxd.save_json_to_html(streaming_from)
    #     justboxd.save_to_csv(streaming_from) 
    #     QDesktopServices.openUrl(QUrl.fromLocalFile(local_html))
    #     self.searchButton.setEnabled(True)
    #     return "Done."

    # def print_output(self, s):
    #     print(s)

    # def thread_complete(self):
    #     print("THREAD COMPLETE!")

    # def progress_fn(self, n):
    #     print("%d%% done" % n)

    # def initUserServices(self):
    #     if self.my_services is None:
    #         self.my_services = {}
    #     else:
    #         for v in self.my_services.values():
    #             button = QPushButton(v)
    #             self.box_layout.addWidget(button)
    #             self.group.addButton(button)
    #         self.layout.update()

    # def addService(self):
    #     for k, v in justboxd.service_codes.items():
    #         if self.lineEdit.text() == v and v not in self.my_services.values():
    #             self.my_services[k] = v
    #             button = QPushButton(self.lineEdit.text())
    #             self.box_layout.addWidget(button)
    #             self.group.addButton(button)
    #     QTimer.singleShot(0, self.lineEdit.clear)

    # def remove_service(self, button):
    #     for k, v in self.my_services.items():
    #         mark_for_deletion_key = None
    #         if v == button.text():
    #             mark_for_deletion_key = k
    #             button.setParent(None)
    #             self.group.removeButton(button)
    #             self.box_layout.removeWidget(button)
    #             self.layout.update()
    #     if mark_for_deletion_key:
    #         del(self.my_services[k])
    #         del(button)

app = QApplication(sys.argv)
window = UIjustboxdWindow()
window.show()
window.initUserServices()

app.exec_()
