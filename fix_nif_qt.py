#!/usr/bin/env python
import argparse, re, os, sys, traceback
from pyffi.formats.nif import NifFormat
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
        self.args = str(dir)
        self.FilePath.setText(self.args)

    def setInfo(self, info):
        self.contents.setText(self.help)

    def fix_and_clean(self):
        self.fix_nif(self.args)
        
    def fix_nif(self, args):
    # dryrun = args.dryrun
    # regex = None
    # if args.regex is not None:
    #     regex = re.compile(args.regex)
    # file_changed = False
    # for stream, data in NifFormat.walkData(args.dir):
    #     try:
    #         # the replace call makes the doctest also pass on windows
    #         os_path = stream.name
    #         split = (os_path.split(os.sep))[-5:]
    #         rejoin = os.path.join(*split).replace(os.sep, "/")
    #         print("reading %s" % rejoin)
    #         data.read(stream)
    #         for block in data.blocks:
    #             if is_block_to_be_removed(block, regex):
    #                 print('removing %s node' % type(block).__name__)
    #                 data.replace_global_node(block, None)
    #                 file_changed = True
    #         # Output
    #         if file_changed and not dryrun:
    #             print('writing to %s' % filename)
    #             stream.close()
    #             output = open(filename, 'wb')
    #             data.write(output)
    #             output.close()
    #     except Exception as e:
    #         print('Error reading file %s' % e)

        file_changed = False
        for stream, data in NifFormat.walkData(args):
            try:
                # the replace call makes the doctest also pass on windows
                os_path = stream.name
                split = (os_path.split(os.sep))[-5:]
                filename = split[-1]
                rejoin = os.path.join(*split).replace(os.sep, "/")
                self.contents.append("reading %s" % rejoin)
                data.read(stream)
                for block in data.blocks:
                    if is_nitextureeffect_block(block):
                        self.contents.append(
                            'removing %s node' % type(block).__name__)
                        data.replace_global_node(block, None)
                        file_changed = True
                    elif is_nisourcetexture_block(block):
                        self.contents.append(
                            'removing %s node' % type(block).__name__)
                        # block.file_name = ""
                        data.replace_global_node(block, None)
                        file_changed = True
                # Output
                if file_changed:
                    self.contents.append('writing to %s' % filename)
                    stream.close()
                    output = open(os_path, 'wb')
                    data.write(output)
                    output.close()
            except Exception as e:
                self.contents.append(traceback.format_exc())
                self.contents.append('Error reading file %s' % e)

def is_nisourcetexture_block(block):
    nmdds_search = re.compile(r'[\_nm\.dds]', re.IGNORECASE)
    is_nmdds = re.search(nmdds_search, str(block))
    if is_nmdds:
        return True
    return False

def is_nitextureeffect_block(block):
    if isinstance(block, NifFormat.NiTextureEffect):
        return True
    return False

# if __name__ == '__main__':
#     try:
#         parser = argparse.ArgumentParser()
#         parser.add_argument('--dryrun', action='store_true',
#                 help='Print out node deletions and then exit without replacing files')
#         parser.add_argument('--regex',
#                 help=(
#                     'The regular expression to use to match NiSourceTextures. '
#                     'If none provided then this step is skipped').format())
#         parser.add_argument('dir', help='The root directory to scan for .nif files.')
#         args = parser.parse_args()
#     except Exception:
#         parser.print_help()
#         raise SystemExit()
#     main(args)



				
def run_app():
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
	
if __name__ == '__main__':
    run_app()
