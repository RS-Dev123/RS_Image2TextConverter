def extract_invoice_fields(text):

    fields = {
        "document_type": "invoice",
        "invoice_number": "",
        "date": "",
        "seller": "",
        "customer": "",
        "items": [],
        "subtotal": "",
        "tax": "",
        "total": ""
    }

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        if line == "":
            continue

        lower_line = line.lower()

        if lower_line.startswith("invoice number:"):
            fields["invoice_number"] = line.split(":", 1)[1].strip()

        elif lower_line.startswith("invoice no:"):
            fields["invoice_number"] = line.split(":", 1)[1].strip()

        elif lower_line.startswith("date:"):
            fields["date"] = line.split(":", 1)[1].strip()

        elif lower_line.startswith("seller:"):
            fields["seller"] = line.split(":", 1)[1].strip()

        elif lower_line.startswith("customer:"):
            fields["customer"] = line.split(":", 1)[1].strip()

        elif lower_line.startswith("subtotal:"):
            fields["subtotal"] = line.split(":", 1)[1].strip()

        elif lower_line.startswith("tax:"):
            fields["tax"] = line.split(":", 1)[1].strip()

        elif lower_line.startswith("total:"):
            fields["total"] = line.split(":", 1)[1].strip()

        elif lower_line.startswith("item:"):

            item = line.split(":", 1)[1].strip()

            if item:
                fields["items"].append(item)

    return fields