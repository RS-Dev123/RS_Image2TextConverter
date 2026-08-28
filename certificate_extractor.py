def extract_certificate_fields(text):

    fields = {
        "document_type": "certificate",
        "recipient": "",
        "certificate_number": "",
        "course": "",
        "organization": "",
        "issue_date": ""
    }

    lines = text.splitlines()
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        lower_line = line.lower()
        if lower_line.startswith("recipient:"):
            fields["recipient"] = line.split(":", 1)[1].strip()
        elif lower_line.startswith("name:"):
            fields["recipient"] = line.split(":", 1)[1].strip()
        elif lower_line.startswith("certificate number:"):
            fields["certificate_number"] = line.split(":", 1)[1].strip()
        elif lower_line.startswith("certificate no:"):
            fields["certificate_number"] = line.split(":", 1)[1].strip()
        elif lower_line.startswith("course:"):
            fields["course"] = line.split(":", 1)[1].strip()
        elif lower_line.startswith("organization:"):
            fields["organization"] = line.split(":", 1)[1].strip()
        elif lower_line.startswith("institution:"):
            fields["organization"] = line.split(":", 1)[1].strip()
        elif lower_line.startswith("date:"):
            fields["issue_date"] = line.split(":", 1)[1].strip()
        elif lower_line.startswith("issue date:"):
            fields["issue_date"] = line.split(":", 1)[1].strip()
    return fields