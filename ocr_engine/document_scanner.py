import cv2
import numpy as np


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
    width1 = np.linalg.norm(bottom_right - bottom_left)
    width2 = np.linalg.norm(top_right - top_left)
    max_width = int(max(width1, width2))
    height1 = np.linalg.norm(top_right - bottom_right)
    height2 = np.linalg.norm(top_left - bottom_left)
    max_height = int(max(height1, height2))
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
    (new_width, int(original_height * scale))
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

if document is None:
    print("Document could not be detected.")
    cv2.imwrite(
        "edges.png",
        edges
    )
    print("Edge image saved as edges.png")
    exit()

warped = perspective_transform(
    resized,
    document
)

cv2.imwrite(
    "detected_document.png",
    warped
)

cv2.imwrite(
    "document_edges.png",
    edges
)

print("\nDocument detected successfully!")
print("Saved:")
print("1. detected_document.png")
print("2. document_edges.png")