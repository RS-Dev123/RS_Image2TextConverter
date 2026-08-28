import pytesseract


def get_ocr_confidence(image):

    data = pytesseract.image_to_data(
        image,
        config="--psm 6",
        output_type=pytesseract.Output.DICT
    )

    confidence_values = []

    for confidence in data["conf"]:

        try:

            confidence = float(confidence)

            if confidence >= 0:
                confidence_values.append(confidence)

        except ValueError:

            continue

    if len(confidence_values) == 0:

        return 0.0

    average_confidence = (
        sum(confidence_values)
        / len(confidence_values)
    )

    return round(
        average_confidence,
        2
    )