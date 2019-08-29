"""The Qt interface"""

import sys
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout, QCheckBox,
                             QPushButton, QTextEdit, QFileDialog,
                             QLineEdit, QApplication, QWidget)
from processor import Processor


class App(QWidget):
    """The primary class"""
    def __init__(self, parent=None):
        super(App, self).__init__(parent)

        self.layout = QVBoxLayout()

        self.top_layout = QHBoxLayout()
        self.open_button = QPushButton("Open")
        self.open_button.clicked.connect(self.getfile)
        self.top_layout.addWidget(self.open_button)
        self.file_path = QLineEdit()
        self.top_layout.addWidget(self.file_path)
        self.dry_run_checkbox = QCheckBox("Dryrun")
        self.dry_run_checkbox.setChecked(False)
        self.dry_run_checkbox.toggled.connect(
            lambda: self.set_dry_run())
        self.is_dryrun = False
        self.top_layout.addWidget(self.dry_run_checkbox)

        self.layout.addLayout(self.top_layout)

        self.contents = QTextEdit()
        self.layout.addWidget(self.contents)

        self.help = "help"
        self.bottom_layout = QHBoxLayout()
        self.help_button = QPushButton("Help")
        self.help_button.clicked.connect(lambda: self.set_info(self.help))
        self.bottom_layout.addWidget(self.help_button)
        self.bottom_layout.addStretch(1)
        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.fix_and_clean)
        self.bottom_layout.addWidget(self.run_button)

        self.layout.addLayout(self.bottom_layout)

        self.setLayout(self.layout)
        self.setWindowTitle("OpenMW NIF Converter")

        self.processor = Processor(self.contents.append)

    def getfile(self):
        """function to retrieve the directory to act on"""
        acting_directory = QFileDialog.getExistingDirectory(
            self, 'Open directory')
        self.acting_directory = str(acting_directory)
        self.file_path.setText(self.acting_directory)

    def set_info(self, info):
        """Sets the contents of the notification TextEdit"""
        self.contents.setText(info)

    def fix_and_clean(self):
        """Runs the main processing script"""
        self.processor.process_dir(self.directory, self.is_dryrun)

    def set_dry_run(self):
        """Checks if the run will actually be attempted"""
        if self.dry_run_checkbox.isChecked():
            self.is_dryrun = True
        # else:
        #     self.is_dryrun = False


def run_app():
    """starts the building of the app and closes the app"""
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run_app()
