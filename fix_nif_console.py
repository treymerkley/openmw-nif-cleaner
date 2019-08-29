"""The console dialog for the program"""
import argparse
from processor import Processor

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
    processor = Processor(print)
    processor.process_dir(args.dir, args.dryrun)
