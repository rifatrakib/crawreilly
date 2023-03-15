def format_folder_and_file_name(name):
    mapper = {
        "\\": " ",
        "/": " ",
        ":": " - ",
        "*": " ",
        "?": "",
        '"': " - ",
        "<": " - ",
        ">": " - ",
        "|": " ",
    }

    formatted_chars = []
    for char in name:
        if char in mapper:
            formatted_chars.append(char.replace(char, mapper[char]))
        else:
            formatted_chars.append(char)

    formatted_name = "".join(formatted_chars)
    return formatted_name
