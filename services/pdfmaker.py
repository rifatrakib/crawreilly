import os

from weasyprint import CSS, HTML


def create_book_pdf():
    for book_category in os.listdir("data/resources"):
        if "." in book_category:
            continue

        for book_dir in os.listdir(f"data/resources/{book_category}"):
            if "." in book_dir:
                continue

            # Create an empty list to store the HTML files
            html_dir = f"data/resources/{book_category}/{book_dir}"

            # Create an empty list to store the HTML files
            html_files = []
            stylesheets = []

            # Loop through the directory and add each HTML file to the list
            for file in os.listdir(html_dir):
                if file.endswith(".html"):
                    html_files.append(os.path.join(html_dir, file))
                elif file.endswith(".css"):
                    stylesheets.append(os.path.join(html_dir, file))

            # Sort the list of HTML files by filename
            html_files.sort()

            # Create a new HTML object
            html_string = ""

            # Loop through the HTML files and add each one to the HTML object
            for file in html_files:
                with open(file, "r") as reader:
                    html_string += reader.read()

            # Set the CSS styles for the document
            css = []
            for stylesheet in stylesheets:
                css.append(CSS(filename=stylesheet))

            css_string = CSS(string="@media print {html {page-break-after: always;}}")
            css.append(css_string)

            # Generate the PDF document
            pdf_html = HTML(string=html_string).render(stylesheets=css)
            pdf_html.write_pdf(f"{html_dir}/{book_dir}.pdf")


if __name__ == "__main__":
    create_book_pdf()
