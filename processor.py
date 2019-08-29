"""Module for processing the data"""
from pathlib import Path
from pyffi.formats.nif import NifFormat


class Processor:
    """Initializing th msg_handler"""
    def __init__(self, msg_handler):
        self.msg_handler = msg_handler

    def process_dir(self, directory, is_dryrun):
        """Main processing class"""
        file_changed = False
        for stream, data in NifFormat.walkData(directory):
            try:
                filename = Path(stream.name)
                self.msg_handler("reading %s" % filename)
                data.read(stream)
                for block in data.blocks:
                    # Remove NiTexture effect blocks
                    if isinstance(block, NifFormat.NiTextureEffect):
                        self.msg_handler('\tremoving NiTextureEffect block')
                        data.replace_global_node(block, None)
                        file_changed = True

                    # Remove NiSourceTextures for bump maps
                    elif (isinstance(block, NifFormat.NiTexturingProperty)
                          and block.has_bump_map_texture):
                        source_block = block.bump_map_texture.source
                        bump_map_file = str(source_block.file_name)
                        self.msg_handler('\tremoving NiSourceTexture block with file name %s' % bump_map_file)
                        data.replace_global_node(source_block, None)
                        # Remove reference
                        block.has_bump_map_texture = False
                        file_changed = True

                stream.close()

                # Output
                if file_changed and not is_dryrun:
                    self.msg_handler('\twriting to %s' % filename)
                    output = open(filename, 'wb')
                    data.write(output)
                    output.close()

            except Exception as e:
                self.msg_handler('Error reading file %s' % e)
