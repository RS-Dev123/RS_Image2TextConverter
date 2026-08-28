import cv2
import numpy as np
import pytesseract

from text_cleaner import clean_text
from json_saver import save_to_json
from document_processor import process_document
from ocr_confidence import get_ocr_confidence


# ============================================================
# TESSERACT CONFIGURATION
# ============================================================

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# ============================================================
# ORDER DOCUMENT CORNER POINTS
# ============================================================

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


# ============================================================
# PERSPECTIVE TRANSFORMATION
# ============================================================

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


# ============================================================
# GET IMAGE PATH
# ============================================================

image_path = input(
    "Enter image path: "
)


# ============================================================
# READ IMAGE
# ============================================================

image = cv2.imread(
    image_path
)

if image is None:

    print(
        "\nError: Could not open image."
    )

    exit()


print(
    "\nImage loaded successfully."
)


# ============================================================
# RESIZE IMAGE
# ============================================================

original_height, original_width = image.shape[:2]

new_width = 1000

scale = new_width / original_width

resized = cv2.resize(
    image,
    (
        new_width,
        int(original_height * scale)
    ),
    interpolation=cv2.INTER_CUBIC
)


# ============================================================
# GRAYSCALE
# ============================================================

gray = cv2.cvtColor(
    resized,
    cv2.COLOR_BGR2GRAY
)


# ============================================================
# BLUR / NOISE REDUCTION
# ============================================================

blurred = cv2.GaussianBlur(
    gray,
    (5, 5),
    0
)


# ============================================================
# EDGE DETECTION
# ============================================================

edges = cv2.Canny(
    blurred,
    50,
    150
)


# Save edge image
cv2.imwrite(
    "debug_edges.png",
    edges
)


# ============================================================
# FIND CONTOURS
# ============================================================

contours, _ = cv2.findContours(
    edges,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)


# Sort contours by area
contours = sorted(
    contours,
    key=cv2.contourArea,
    reverse=True
)


document = None


# ============================================================
# FIND DOCUMENT
# ============================================================

for contour in contours:

    area = cv2.contourArea(
        contour
    )

    if area < 10000:
        continue

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

        document = approximation.reshape(
            4,
            2
        )

        break


# ============================================================
# DOCUMENT DETECTION
# ============================================================

if document is not None:

    print(
        "Document detected."
    )

    corrected_document = perspective_transform(
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

    corrected_document = resized


# ============================================================
# SAVE CORRECTED DOCUMENT
# ============================================================

cv2.imwrite(
    "corrected_document.png",
    corrected_document
)


# ============================================================
# OCR PREPROCESSING
# ============================================================

gray_document = cv2.cvtColor(
    corrected_document,
    cv2.COLOR_BGR2GRAY
)


# ============================================================
# RESIZE FOR OCR
# ============================================================

gray_document = cv2.resize(
    gray_document,
    None,
    fx=2,
    fy=2,
    interpolation=cv2.INTER_CUBIC
)


# ============================================================
# NOISE REDUCTION
# ============================================================

gray_document = cv2.GaussianBlur(
    gray_document,
    (3, 3),
    0
)


# ============================================================
# ADAPTIVE THRESHOLD
# ============================================================

processed = cv2.adaptiveThreshold(
    gray_document,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    21,
    10
)


# ============================================================
# SAVE PROCESSED IMAGE
# ============================================================

cv2.imwrite(
    "final_processed.png",
    processed
)


# ============================================================
# TESSERACT OCR
# ============================================================

raw_text = pytesseract.image_to_string(
    processed,
    config="--psm 6"
)


# ============================================================
# OCR CONFIDENCE
# ============================================================

ocr_confidence = get_ocr_confidence(
    processed
)


# ============================================================
# CLEAN OCR TEXT
# ============================================================

text = clean_text(
    raw_text
)


# ============================================================
# DISPLAY RAW OCR TEXT
# ============================================================

print(
    "\n========================================"
)

print(
    "             RAW OCR TEXT"
)

print(
    "========================================\n"
)

print(
    raw_text
)


# ============================================================
# DISPLAY CLEANED TEXT
# ============================================================

print(
    "\n========================================"
)

print(
    "             CLEANED TEXT"
)

print(
    "========================================\n"
)

print(
    text
)


# ============================================================
# DOCUMENT CLASSIFICATION + EXTRACTION
# ============================================================

extracted_data = process_document(
    text
)


# ============================================================
# CREATE FINAL STRUCTURED DATA
# ============================================================

structured_data = {

    "processing": {

        "status": "success",

        "ocr_engine": "Tesseract",

        "confidence": ocr_confidence

    },

    "data": extracted_data

}


# ============================================================
# DISPLAY OCR CONFIDENCE
# ============================================================

print(
    "\n========================================"
)

print(
    "             OCR INFORMATION"
)

print(
    "========================================\n"
)

print(
    f"OCR Confidence: {ocr_confidence}%"
)

print(
    "OCR Engine: Tesseract"
)

print(
    "Processing Status: success"
)


# ============================================================
# DISPLAY STRUCTURED DATA
# ============================================================

print(
    "\n========================================"
)

print(
    "          STRUCTURED DATA"
)

print(
    "========================================\n"
)

for key, value in extracted_data.items():

    print(
        f"{key}: {value}"
    )


# ============================================================
# SAVE CLEANED TEXT
# ============================================================

with open(
    "output.txt",
    "w",
    encoding="utf-8"
) as file:

    file.write(
        text
    )


# ============================================================
# SAVE STRUCTURED JSON
# ============================================================

save_to_json(
    structured_data
)


# ============================================================
# FINISHED
# ============================================================

print(
    "\n========================================"
)

print(
    "          OCR COMPLETED"
)

print(
    "========================================"
)

print(
    "\nText saved to: output.txt"
)

print(
    "JSON saved to: document.json"
)

print(
    "Corrected document: corrected_document.png"
)

print(
    "Processed image: final_processed.png"
)

print(
    "========================================"
)