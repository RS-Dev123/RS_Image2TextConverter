def classify_document(text):

    text = text.lower()
    resume_keywords = [
        "resume",
        "curriculum vitae",
        "experience",
        "skills",
        "education",
        "projects",
        "work experience"
    ]

    invoice_keywords = [
        "invoice",
        "invoice number",
        "quantity",
        "price",
        "amount",
        "subtotal",
        "total",
        "tax"
    ]

    certificate_keywords = [
        "certificate",
        "certification",
        "awarded",
        "this is to certify",
        "certificate number",
        "completion"
    ]

    resume_score = 0
    invoice_score = 0
    certificate_score = 0


    for keyword in resume_keywords:

        if keyword in text:

            resume_score += 1


    for keyword in invoice_keywords:

        if keyword in text:

            invoice_score += 1


    for keyword in certificate_keywords:

        if keyword in text:

            certificate_score += 1


    # -----------------------------------------
    # Determine document type
    # -----------------------------------------

    scores = {
        "resume": resume_score,
        "invoice": invoice_score,
        "certificate": certificate_score
    }


    document_type = max(
        scores,
        key=scores.get
    )


    # -----------------------------------------
    # No meaningful match
    # -----------------------------------------

    if scores[document_type] == 0:

        return "unknown"


    return document_type