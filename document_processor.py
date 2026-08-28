from document_classifier import classify_document

from resume_extractor import extract_resume_fields
from invoice_extractor import extract_invoice_fields
from certificate_extractor import extract_certificate_fields


def process_document(text):

    document_type = classify_document(text)

    if document_type == "resume":

        data = extract_resume_fields(text)

    elif document_type == "invoice":

        data = extract_invoice_fields(text)

    elif document_type == "certificate":

        data = extract_certificate_fields(text)

    else:

        data = {
            "document_type": "unknown",
            "message": "Document type could not be determined."
        }

    return data