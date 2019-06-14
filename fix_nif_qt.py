#!/usr/bin/env python
import argparse, re, os, sys, traceback
from pyffi.formats.nif import NifFormat
from pathlib import Path
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
        
		
    def getfile(self):
        dir = QFileDialog.getExistingDirectory(self, 'Open directory')
        self.dir = str(dir)
        self.FilePath.setText(self.dir)

    def setInfo(self, info):
        self.contents.setText(self.help)

    def fix_and_clean(self):
        self.process_dir(self.dir, self.is_dryrun)

    def setDryRun(self):
        if self.DryRunCheckbox.isChecked():
            self.is_dryrun = True
        else:
            self.is_dryrun = False

    def process_dir(self, dir, is_dryrun):
        file_changed = False
        for stream, data in NifFormat.walkData(dir):
            try:
                # the replace call makes the doctest also pass on windows
                filename = Path(stream.name)
                self.contents.append("reading %s" % filename)
                data.read(stream)
                for block in data.blocks:
                    # Remove NiTexture effect blocks
                    if isinstance(block, NifFormat.NiTextureEffect):
                        self.contents.append('\tremoving NiTextureEffect block')
                        data.replace_global_node(block, None)
                        file_changed = True

                        # Remove NiSourceTextures for bump maps
                    elif (isinstance(block, NifFormat.NiTexturingProperty)
                          and block.has_bump_map_texture):
                        source_block = block.bump_map_texture.source
                        bump_map_file = str(source_block.file_name)
                        self.contents.append('\tremoving NiSourceTexture block with file name %s' % bump_map_file)
                        data.replace_global_node(source_block, None)
                        # Remove reference
                        block.has_bump_map_texture = False
                        file_changed = True

                stream.close()

                # Output
                if file_changed and not is_dryrun:
                    self.contents.append('\twriting to %s' % filename)
                    output = open(filename, 'wb')
                    data.write(output)
                    output.close()

            except Exception as e:
                self.contents.append('Error reading file %s' % e)
				
def run_app():
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
	
if __name__ == '__main__':
    run_app()
