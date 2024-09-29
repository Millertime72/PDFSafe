from pdf2image import convert_from_path


def convert_to_safe(path: str) -> None:
    print('Converting images')
    images = convert_from_path(path)
    print('Saving')
    images[0].save(path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:])
    print('Done')