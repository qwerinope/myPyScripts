import sys
import noordhoff
from PySide6.QtWidgets import QMainWindow, QWidget, QGridLayout, QLineEdit, QPushButton, QLabel, QFileDialog, QMessageBox, QApplication
from PySide6.QtGui import QAction, QDesktopServices
from PySide6.QtCore import QRunnable, Signal, QObject, QThreadPool, Slot, QUrl

class Signals(QObject):
    completed = Signal()
    started = Signal()
    
class Runnable(QRunnable):
    def __init__(self, url:str, out:str):
        super().__init__()
        self.url = url
        self.out = out
        self.signals = Signals()

    @Slot()
    def run(self):
        self.signals.started.emit()
        noordhoff.main(self.url, self.out, True)
        self.signals.completed.emit()
    

class mainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.savePath = ''
        self.bookLink = ''

        self.setWindowTitle('Noordhoff Book Downloader')
        self.setGeometry(0,0,1000,150)
        self.setFixedHeight(150)

        container = QWidget(self)
        container.setLayout(QGridLayout())
        # container.layout().addWidget(self.text_edit)
        self.setCentralWidget(container)

        self.downloadLink = QLineEdit()
        self.downloadLink.setPlaceholderText("https://apps.noordhoff.nl/se/content/book/...")
        container.layout().addWidget(self.downloadLink, 0, 0, 1, 1)
        
        self.pasteButton = QPushButton("Paste")
        self.pasteButton.clicked.connect(self.pastething)
        container.layout().addWidget(self.pasteButton, 0, 1, 1, 1)

        self.saveLocation = QLineEdit()
        self.saveLocation.setReadOnly(True)
        self.saveLocation.setPlaceholderText("output.pdf")
        container.layout().addWidget(self.saveLocation, 1, 0, 1, 1)

        self.fileChooserButton = QPushButton("Save as")
        self.fileChooserButton.clicked.connect(self.open_file_dialog)
        container.layout().addWidget(self.fileChooserButton, 1, 1, 1, 1)

        self.downloadButton = QPushButton("Download")
        self.downloadButton.clicked.connect(self.startDownload)
        container.layout().addWidget(self.downloadButton, 2, 1, 1, 1)

        self.statusLabel = QLabel()
        self.statusLabel.setText("Ready")
        container.layout().addWidget(self.statusLabel, 2, 0, 1, 1)

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('&File')
        exit_action = QAction('&Exit', self)
        exit_action.setStatusTip('Exit')
        exit_action.setShortcut('Alt+F4')
        exit_action.triggered.connect(self.destroy)
        file_menu.addAction(exit_action)

        help_menu = menu_bar.addMenu('&Help')
        githubaction = QAction('&Github', self)
        githubaction.setStatusTip('Open Github')
        githubaction.setShortcut('F1')
        githubaction.triggered.connect(self.opengithub)
        help_menu.addAction(githubaction)

        self.show()
        
    def pastething(self):
        self.downloadLink.clear()
        self.downloadLink.paste()
        
        
    def opengithub(self):
        QDesktopServices.openUrl(QUrl("https://github.com/qwerinope/myPyScripts/tree/main/noordhoffPDFCreator"))

    def open_file_dialog(self):
        response = QFileDialog.getSaveFileName(
            caption="Name the output",
            filter="PDF Document (*.pdf)"
        )
        path = response[0]
        if path == '':
            return
        path = path.removesuffix('.pdf')
        self.savePath=path
        self.saveLocation.setText(path + '.pdf')
        
    def startDownload(self):
        self.bookLink = self.downloadLink.text()
        if self.bookLink == '':
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Warning: No URL set")
            dlg.setText("Please paste the URL of the book into the program.")
            dlg.exec()
            return
        elif self.savePath == '':
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Warning: No save path set")
            dlg.setText("Please select a place to save the downloaded PDF.")
            dlg.exec()
            return
        
        pool = QThreadPool.globalInstance()
        worker = Runnable(self.bookLink, self.savePath)
        worker.signals.completed.connect(self.disableGUI)
        worker.signals.started.connect(self.enableGUI)
        pool.start(worker)
        
            
    def enableGUI(self):
        self.downloadLink.setVisible(False)
        self.downloadButton.setVisible(False)
        self.pasteButton.setVisible(False)
        self.saveLocation.setVisible(False)
        self.fileChooserButton.setVisible(False) 
        self.statusLabel.setText("Downloading...")
        
    def disableGUI(self):
        self.downloadLink.setVisible(True)
        self.downloadButton.setVisible(True)
        self.pasteButton.setVisible(True)
        self.saveLocation.setVisible(True)
        self.fileChooserButton.setVisible(True) 
        self.statusLabel.setText("Done.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainWindow()
    sys.exit(app.exec())
    

