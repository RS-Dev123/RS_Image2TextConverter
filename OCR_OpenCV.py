import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = (
    r"C:/Program Files/Tesseract-OCR/tesseract.exe"
)
image_path = input("Enter image path: ")
try:
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not open image.")
        exit()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )
    blurred = cv2.GaussianBlur(resized,(3, 3),0)
    processed = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )
    cv2.imwrite(
        "processed_image.png",
        processed
    )
    text = pytesseract.image_to_string(
        processed
    )
    print("\n========== EXTRACTED TEXT ==========\n")
    print(text)
    with open("output.txt","w",encoding="utf-8") as file:
        file.write(text)
    print("Text saved to output.txt")
    print("Processed image saved to processed_image.png")
except Exception as e:
    print("Error:", e)