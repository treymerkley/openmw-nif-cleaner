#!/usr/bin/env python
import argparse, re, os
from pathlib import Path
from pyffi.formats.nif import NifFormat

def process_dir(dir, is_dryrun):
    file_changed = False
    for stream, data in NifFormat.walkData(args.dir):
        try:
            # the replace call makes the doctest also pass on windows
            filename = Path(stream.name)
            print("reading %s" % filename)
            data.read(stream)
            for block in data.blocks:
                # Remove NiTexture effect blocks
                if isinstance(block, NifFormat.NiTextureEffect):
                    print('\tremoving NiTextureEffect block')
                    data.replace_global_node(block, None)
                    file_changed = True

                # Remove NiSourceTextures for bump maps
                elif (isinstance(block, NifFormat.NiTexturingProperty)
                        and block.has_bump_map_texture):
                    source_block = block.bump_map_texture.source
                    bump_map_file = str(source_block.file_name)
                    print('\tremoving NiSourceTexture block with file name %s' % bump_map_file)
                    data.replace_global_node(source_block, None)
                    # Remove reference
                    block.has_bump_map_texture = False
                    file_changed = True

            stream.close()

            # Output
            if file_changed and not is_dryrun:
                print('\twriting to %s' % filename)
                output = open(filename, 'wb')
                data.write(output)
                output.close()

        except Exception as e:
            print('Error reading file %s' % e)

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--dryrun', action='store_true',
                help='Print out node deletions and then exit without replacing files')
        parser.add_argument('dir', help='The root directory to scan for .nif files.')
        args = parser.parse_args()
    except Exception:
        parser.print_help()
        raise SystemExit()
process_dir(args.dir, args.dryrun)
