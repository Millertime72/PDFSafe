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
        return [file for file in os.listdir(path) if file.endswith('.pdf')]
    return [path]

parser = ArgumentParser(
    prog = "pdfsafe",
    description = "Converts pdfs to safe, image-based versions",
    epilog = "Not liable if your computer go boom."
)

parser.add_argument("path", help="path to pdf / directory containg pdf[s]")

if __name__ == "__main__":
    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        parser.error("connot convert '%s': does not exist" % args.path)
    
    for pdf in _get_pdf_paths(args.path):
        convert_to_safe(pdf)