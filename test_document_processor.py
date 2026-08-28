from document_processor import process_document

resume = """
Resume

Name: Rahul Kumar
Email: rahul@gmail.com
Phone: 9876543210
Skills: C++, Python, JavaScript
Education: B.Tech Computer Science
Experience: Software Developer Intern
Projects: Smart OCR System
"""

invoice = """
Invoice

Invoice Number: INV-1001
Date: 28/08/2026
Seller: ABC Store
Customer: Rahul Kumar
Item: Laptop
Item: Mouse
Subtotal: 50000
Tax: 9000
Total: 59000
"""

certificate = """
Certificate

Recipient: Rahul Kumar
Certificate Number: CERT-123
Course: Python Programming
Organization: ABC Institute
Issue Date: 28/08/2026
"""


print("========== RESUME ==========")

print(
    process_document(resume)
)


print("\n========== INVOICE ==========")

print(
    process_document(invoice)
)


print("\n========== CERTIFICATE ==========")

print(
    process_document(certificate)
)