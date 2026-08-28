def extract_resume_fields(text):

    fields = {
        "document_type": "resume",
        "name": "",
        "email": "",
        "phone": "",
        "skills": [],
        "education": "",
        "experience": "",
        "projects": ""
    }

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        if line == "":
            continue

        lower_line = line.lower()

        if lower_line.startswith("name:"):
            fields["name"] = line.split(":", 1)[1].strip()

        elif lower_line.startswith("email:"):
            fields["email"] = line.split(":", 1)[1].strip()

        elif lower_line.startswith("phone:"):
            fields["phone"] = line.split(":", 1)[1].strip()

        elif lower_line.startswith("skills:"):
            skills = line.split(":", 1)[1].strip()

            if skills:
                fields["skills"] = [
                    skill.strip()
                    for skill in skills.split(",")
                ]

        elif lower_line.startswith("education:"):
            fields["education"] = line.split(":", 1)[1].strip()

        elif lower_line.startswith("experience:"):
            fields["experience"] = line.split(":", 1)[1].strip()

        elif lower_line.startswith("projects:"):
            fields["projects"] = line.split(":", 1)[1].strip()

    return fields