#!/usr/bin/env python
import argparse, re, os
from pyffi.formats.nif import NifFormat

def main(args):
    dryrun = args.dryrun
    regex = None
    if args.regex is not None:
        regex = re.compile(args.regex)
    file_changed = False
    for stream, data in NifFormat.walkData(args.dir):
        try:
            # the replace call makes the doctest also pass on windows
            os_path = stream.name
            split = (os_path.split(os.sep))[-5:]
            rejoin = os.path.join(*split).replace(os.sep, "/")
            print("reading %s" % rejoin)
            data.read(stream)
            for block in data.blocks:
                if is_block_to_be_removed(block, regex):
                    print('removing %s node' % type(block).__name__)
                    data.replace_global_node(block, None)
                    file_changed = True
            # Output
            if file_changed and not dryrun:
                print('writing to %s' % filename)
                stream.close()
                output = open(filename, 'wb')
                data.write(output)
                output.close()
        except Exception as e:
            print('Error reading file %s' % e)

def is_block_to_be_removed(block, regex):
    if (regex is not None 
            and isinstance(block, NifFormat.NiSourceTexture)
            and regex.search(str(block.get_attribute('file_name')))):
        return True
    if isinstance(block, NifFormat.NiTextureEffect):
        return True
    return False

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--dryrun', action='store_true',
                help='Print out node deletions and then exit without replacing files')
        parser.add_argument('--regex',
                help=(
                    'The regular expression to use to match NiSourceTextures. '
                    'If none provided then this step is skipped').format())
        parser.add_argument('dir', help='The root directory to scan for .nif files.')
        args = parser.parse_args()
    except Exception:
        parser.print_help()
        raise SystemExit()
    main(args)