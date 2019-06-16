#!/usr/bin/env python
import sys, traceback
from processor import Processor
from PyQt5.QtWidgets import(QHBoxLayout, QVBoxLayout,
                            QComboBox, QCheckBox, QLabel,
                            QPushButton, QTextEdit, QScrollArea,
                            QFileDialog, QLineEdit, QApplication,
                            QWidget, QInputDialog)


class App(QWidget):
    def __init__(self, parent = None):
        super(App, self).__init__(parent)

        self.layout = QVBoxLayout()

        self.TopLayout = QHBoxLayout()
        self.OpenButton = QPushButton("Open")
        self.OpenButton.clicked.connect(self.getfile)
        self.TopLayout.addWidget(self.OpenButton)
        self.FilePath = QLineEdit()
        self.TopLayout.addWidget(self.FilePath)
        self.DryRunCheckbox = QCheckBox("Dryrun")
        self.DryRunCheckbox.setChecked(False)
        self.DryRunCheckbox.toggled.connect(
            lambda: self.setDryRun())
        self.is_dryrun = False
        self.TopLayout.addWidget(self.DryRunCheckbox)

        self.layout.addLayout(self.TopLayout)

        self.contents = QTextEdit()
        self.layout.addWidget(self.contents)

        self.help = "help"
        self.BottomLayout = QHBoxLayout()
        self.HelpButton = QPushButton("Help")
        self.HelpButton.clicked.connect(lambda: self.setInfo(self.help))
        self.BottomLayout.addWidget(self.HelpButton)
        self.BottomLayout.addStretch(1)
        self.RunButton = QPushButton("Run")
        self.RunButton.clicked.connect(self.fix_and_clean)
        self.BottomLayout.addWidget(self.RunButton)

        self.layout.addLayout(self.BottomLayout)

        self.setLayout(self.layout)
        self.setWindowTitle("OpenMW NIF Converter")

        self.processor = Processor(self.contents.append)

    def getfile(self):
        dir = QFileDialog.getExistingDirectory(self, 'Open directory')
        self.dir = str(dir)
        self.FilePath.setText(self.dir)

    def setInfo(self, info):
        self.contents.setText(self.help)

    def fix_and_clean(self):
        self.processor.process_dir(self.dir, self.is_dryrun)

    def setDryRun(self):
        if self.DryRunCheckbox.isChecked():
            self.is_dryrun = True
        else:
            self.is_dryrun = False

def run_app():
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run_app()
