def extract_fields(text):

    fields = {
        "name": "",
        "age": "",
        "email": "",
        "phone": "",
        "course": "",
        "college": "",
        "date": ""
    }

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        if line == "":
            continue

        lower_line = line.lower()

        # ==========================================
        # NAME
        # ==========================================

        if (
            lower_line.startswith("name:") or
            lower_line.startswith("name -") or
            lower_line.startswith("full name:") or
            lower_line.startswith("student name:")
        ):

            if ":" in line:

                value = line.split(":", 1)[1].strip()

            elif "-" in line:

                value = line.split("-", 1)[1].strip()

            else:

                value = ""

            fields["name"] = value


        # ==========================================
        # AGE
        # ==========================================

        elif (
            lower_line.startswith("age:") or
            lower_line.startswith("age -")
        ):

            if ":" in line:

                value = line.split(":", 1)[1].strip()

            elif "-" in line:

                value = line.split("-", 1)[1].strip()

            else:

                value = ""

            fields["age"] = value


        # ==========================================
        # EMAIL
        # ==========================================

        elif (
            lower_line.startswith("email:") or
            lower_line.startswith("email -") or
            lower_line.startswith("e-mail:") or
            lower_line.startswith("email id:")
        ):

            if ":" in line:

                value = line.split(":", 1)[1].strip()

            elif "-" in line:

                value = line.split("-", 1)[1].strip()

            else:

                value = ""

            fields["email"] = value


        # ==========================================
        # PHONE
        # ==========================================

        elif (
            lower_line.startswith("phone:") or
            lower_line.startswith("phone -") or
            lower_line.startswith("mobile:") or
            lower_line.startswith("mobile no:") or
            lower_line.startswith("contact:")
        ):

            if ":" in line:

                value = line.split(":", 1)[1].strip()

            elif "-" in line:

                value = line.split("-", 1)[1].strip()

            else:

                value = ""

            fields["phone"] = value


        # ==========================================
        # COURSE
        # ==========================================

        elif (
            lower_line.startswith("course:") or
            lower_line.startswith("course -") or
            lower_line.startswith("program:")
        ):

            if ":" in line:

                value = line.split(":", 1)[1].strip()

            elif "-" in line:

                value = line.split("-", 1)[1].strip()

            else:

                value = ""

            fields["course"] = value


        # ==========================================
        # COLLEGE
        # ==========================================

        elif (
            lower_line.startswith("college:") or
            lower_line.startswith("college -") or
            lower_line.startswith("university:") or
            lower_line.startswith("institution:")
        ):

            if ":" in line:

                value = line.split(":", 1)[1].strip()

            elif "-" in line:

                value = line.split("-", 1)[1].strip()

            else:

                value = ""

            fields["college"] = value


        # ==========================================
        # DATE
        # ==========================================

        elif (
            lower_line.startswith("date:") or
            lower_line.startswith("date -") or
            lower_line.startswith("dob:") or
            lower_line.startswith("date of birth:")
        ):

            if ":" in line:

                value = line.split(":", 1)[1].strip()

            elif "-" in line:

                value = line.split("-", 1)[1].strip()

            else:

                value = ""

            fields["date"] = value


    return fields