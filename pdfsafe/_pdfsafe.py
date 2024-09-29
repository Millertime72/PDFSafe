import tempfile

from pdf2image import convert_from_path
from pypdf import PdfReader, PdfWriter


def convert_to_safe(path: str) -> None:
    images = []
    num_pages = PdfReader(open(path, "rb")).get_num_pages()
    
    with tempfile.TemporaryDirectory() as temp:
        for idx in range(num_pages):
            print("[Page %d/%d] Converting '%s'..." % (idx + 1, num_pages, path), end="\r")
            
            images += convert_from_path(
                path, fmt="jpeg", dpi=100,
                first_page=idx+1, last_page=idx+1,
                output_folder=temp
            )
        
        pdf = PdfWriter()
        
        for idx, image in enumerate(images):
            print("[Page %d/%d] Saving '%s'..." % (idx + 1, num_pages, path), end="\r")
            
            with tempfile.TemporaryFile() as temp_page:
                image.save(temp_page, "PDF", resolution=100.0)

                page = PdfReader(temp_page)
                pdf.add_page(page.pages[0])
        
        open(path, 'w').close() # completely erase pdf file
        pdf.write(path) # write new data to file
        
        print() # newline