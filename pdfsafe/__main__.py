from typing import List

import os
from argparse import ArgumentParser, Namespace

from pdfsafe._pdfsafe import convert_to_safe


def _normalize_path(path: str) -> str:
    path = os.path.expanduser(path)
    path = os.path.abspath(path)
    path = os.path.normpath(path)
    
    return path

def _get_pdf_paths(path: str) -> List[str]:
    if os.path.isdir(path):
        return [os.path.join(root, file) for root, _, files in os.walk(path) for file in files if file.endswith('.pdf')]
    return [path]

parser = ArgumentParser(
    prog = "pdfsafe",
    description = "Converts pdfs to safe, image-based versions",
    epilog = "Not liable if your computer go boom."
)

parser.add_argument("path", help="path to pdf/directory containg pdf[s]")
parser.add_argument("-r", "--recursive", action="store_true", help="convert all files under directory")

if __name__ == "__main__":
    args = parser.parse_args()
    
    if not args.recursive and os.path.isdir(args.path):
        parser.error("cannot convert '%s': is a directory" % args.path)
    elif not os.path.exists(args.path):
        parser.error("connot convert '%s': does not exist" % args.path)
    
    for pdf in _get_pdf_paths(args.path):
        print("Converting '%s'..." % pdf, end='')
        
        convert_to_safe(pdf)
        
        print(" done.")