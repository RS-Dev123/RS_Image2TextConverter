import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

def order_points(points):
    points = np.array(points, dtype="float32")
    ordered = np.zeros((4, 2), dtype="float32")
    sums = points.sum(axis=1)
    ordered[0] = points[np.argmin(sums)]
    ordered[2] = points[np.argmax(sums)]
    differences = np.diff(points, axis=1)
    ordered[1] = points[np.argmin(differences)]
    ordered[3] = points[np.argmax(differences)]
    return ordered

def perspective_transform(image, points):
    rect = order_points(points)
    top_left, top_right, bottom_right, bottom_left = rect

    width1 = np.linalg.norm(
        bottom_right - bottom_left
    )

    width2 = np.linalg.norm(
        top_right - top_left
    )

    max_width = int(
        max(width1, width2)
    )

    height1 = np.linalg.norm(
        top_right - bottom_right
    )

    height2 = np.linalg.norm(
        top_left - bottom_left
    )

    max_height = int(
        max(height1, height2)
    )

    destination = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]
    ], dtype="float32")

    matrix = cv2.getPerspectiveTransform(
        rect,
        destination
    )

    warped = cv2.warpPerspective(
        image,
        matrix,
        (max_width, max_height)
    )

    return warped


image_path = input("Enter image path: ")

image = cv2.imread(image_path)
if image is None:
    print("Error: Could not open image.")
    exit()

original_height, original_width = image.shape[:2]
new_width = 800
scale = new_width / original_width
resized = cv2.resize(
    image,
    (
        new_width,
        int(original_height * scale)
    )
)
gray = cv2.cvtColor(
    resized,
    cv2.COLOR_BGR2GRAY
)

blurred = cv2.GaussianBlur(
    gray,
    (5, 5),
    0
)

edges = cv2.Canny(
    blurred,
    75,
    200
)

contours, _ = cv2.findContours(
    edges,
    cv2.RETR_LIST,
    cv2.CHAIN_APPROX_SIMPLE
)

contours = sorted(
    contours,
    key=cv2.contourArea,
    reverse=True
)


document = None

for contour in contours:

    perimeter = cv2.arcLength(
        contour,
        True
    )

    approximation = cv2.approxPolyDP(
        contour,
        0.02 * perimeter,
        True
    )

    if len(approximation) == 4:
        document = approximation.reshape(4, 2)
        break


if document is not None:
    print("Document detected.")
    warped = perspective_transform(
        resized,
        document
    )

else:

    print(
        "Document not detected."
    )

    print(
        "Using original image."
    )

    warped = resized
cv2.imwrite(
    "corrected_document.png",
    warped
)

gray_document = cv2.cvtColor(
    warped,
    cv2.COLOR_BGR2GRAY
)

gray_document = cv2.resize(
    gray_document,
    None,
    fx=2,
    fy=2,
    interpolation=cv2.INTER_CUBIC
)

gray_document = cv2.GaussianBlur(
    gray_document,
    (3, 3),
    0
)

processed = cv2.adaptiveThreshold(
    gray_document,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    11,
    2
)

cv2.imwrite(
    "final_processed.png",
    processed
)


text = pytesseract.image_to_string(
    processed
)

print(
    "\n========== EXTRACTED TEXT ==========\n"
)

print(text)

with open("output.txt","w",encoding="utf-8") as file:
    file.write(text)


print(
    "\nText saved to output.txt"
)

print(
    "Corrected document saved to corrected_document.png"
)

print(
    "Processed image saved to final_processed.png"
)