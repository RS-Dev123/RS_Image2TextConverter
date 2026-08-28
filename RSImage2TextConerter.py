import pytesseract
from PIL import Image

# Tell pytesseract where Tesseract OCR is installed
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

image_path = input("Enter image path: ")

try:
    image = Image.open(image_path)

    text = pytesseract.image_to_string(image)

    print("\n========== EXTRACTED TEXT ==========\n")
    print(text)

    with open("output.txt", "w", encoding="utf-8") as file:
        file.write(text)

    print("\nText saved to output.txt")

except FileNotFoundError:
    print("Error: Image file not found.")

except Exception as e:
    print("Error:", e)