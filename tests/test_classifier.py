from document_classifier import classify_document


resume_text = """
Rahul Kumar

Skills:
C++
Python
JavaScript

Education:
B.Tech Computer Science

Projects:
OCR Document Scanner

Experience:
Software Developer Intern
"""


invoice_text = """
INVOICE

Invoice Number: INV-1001

Item
Quantity
Price
Amount

Laptop
1
50000

Tax
Total
"""


certificate_text = """
CERTIFICATE

This is to certify that Rahul Kumar
has successfully completed the course.

Certificate Number: CERT12345

Date: 28/08/2026
"""


print(
    "Resume:",
    classify_document(resume_text)
)

print(
    "Invoice:",
    classify_document(invoice_text)
)

print(
    "Certificate:",
    classify_document(certificate_text)
)