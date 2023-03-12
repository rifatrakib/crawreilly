def log_writer(file_path, string):
    with open(file_path, "a") as writer:
        writer.write(string)
