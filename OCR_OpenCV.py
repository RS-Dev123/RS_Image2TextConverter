import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:/Program Files/Tesseract-OCR/tesseract.exe"
)

image_path = input("Enter image path: ")

try:
    # Read image using OpenCV
    image = cv2.imread(image_path)

    if image is None:
        print("Error: Could not open image.")
        exit()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    _, threshold = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    cv2.imwrite("processed_image.png", threshold)

    text = pytesseract.image_to_string(threshold)

    print("\n========== EXTRACTED TEXT ==========\n")
    print(text)

    with open("output.txt", "w", encoding="utf-8") as file:
        file.write(text)

    print("Text saved to output.txt")
    print("Processed image saved to processed_image.png")

except Exception as e:
    print("Error:", e)