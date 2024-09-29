import tempfile

from pdf2image import convert_from_path
from pypdf import PdfReader


def _get_num_pages(path: str) -> int:
    return PdfReader(open(path, "rb")).get_num_pages()

def convert_to_safe(path: str) -> None:
    images = []
    num_pages = _get_num_pages(path)
    
    with tempfile.TemporaryDirectory() as temp:
        for idx in range(num_pages):
            print("[Page %d/%d] Converting '%s'..." % (idx + 1, num_pages, path), end="\r")
            
            images += convert_from_path(
                path, fmt="jpeg", dpi=100,
                first_page=idx+1, last_page=idx+1,
                output_folder=temp
            )
        
        print()
        
        images[0].save(path, "PDF", resolution=100.0, save_all=True, append_images=images[1:])