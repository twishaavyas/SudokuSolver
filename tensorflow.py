try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = 'E:\\python\\Tesseract-OCR\\tesseract.exe'
tessdata_dir_config = '--tessdata-dir "E:\\python\\python\\Lib\\site-packages\\pytesseract"'

for x in range(81):
    x = pytesseract.image_to_string(Image.open(os.path.abspath('8.jpg')), config= '-psm 10')
print(x)

