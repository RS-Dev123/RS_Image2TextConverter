def clean_text(text):
    """
    Clean raw OCR text.

    Removes:
    - Empty lines
    - Extra spaces
    - Spaces at the beginning/end of lines
    """

    lines = text.splitlines()

    cleaned_lines = []

    for line in lines:

        # Remove spaces from beginning and end
        line = line.strip()

        # Ignore empty lines
        if line == "":
            continue

        # Replace multiple spaces with one space
        line = " ".join(line.split())

        cleaned_lines.append(line)

    # Join all cleaned lines
    return "\n".join(cleaned_lines)