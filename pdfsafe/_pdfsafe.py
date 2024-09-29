from typing import Optional

import tempfile

from pdf2image import convert_from_path
from pypdf import PdfReader, PdfWriter


def convert_to_safe(path: str) -> None:
    images = []
    num_pages = PdfReader(open(path, "rb")).get_num_pages()
    
    def log_action(action: str, idx: int, min_len: Optional[int] = 0) -> int:
        log = "[Page %d/%d] %s %s" % (idx + 1, num_pages, action, path)
        whitespace = ' ' * max(0, min_len - len(log))
        
        print(log + whitespace, end="\r")
        
        return len(log)
    
    with tempfile.TemporaryDirectory() as temp:
        for idx in range(num_pages):
            min_len = log_action("Converting", idx)
            
            images += convert_from_path(
                path, fmt="jpeg", dpi=100,
                first_page=idx+1, last_page=idx+1,
                output_folder=temp
            )
        
        pdf = PdfWriter()
        
        for idx, image in enumerate(images):
            log_action("Saving", idx, min_len)
            
            with tempfile.TemporaryFile() as temp_page:
                image.save(temp_page, "PDF", resolution=100.0)

                page = PdfReader(temp_page)
                pdf.add_page(page.pages[0])
        
        open(path, "w").close() # completely erase pdf file
        pdf.write(path) # write new data to file
        
        print() # newline