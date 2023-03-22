# Crawreilly

*Crawreilly* is a Python-based web scraper built using [Scrapy](https://scrapy.org/) that allows you to download all books and other resources from [O'Reilly](https://www.oreilly.com/), pre-process the scraped HTML, CSS, and image resources, and save them locally as PDF files. To use this tool, you will need a valid subscription to [O'Reilly](https://www.oreilly.com/).


## Getting Started

### Prerequisites

To run this scraper, you'll need to have the following:

* Python >=3.9
* [Scrapy](https://scrapy.org/)
* [WeasyPrint](https://weasyprint.org/)
* MongoDB and a MongoDB cluster along with its URI for the app to communicate with the right database.


### Installation

1. Clone the repository: `git clone https://github.com/rifatrakib/crawreilly.git`

2. Open a terminal window and navigate to the repository directory: `cd crawreilly`

3. Create a virtual environment: `virtualenv venv`

4. Run `pip install poetry` to install [poetry](https://python-poetry.org/)

5. Install dependencies: `poetry install`


## Usage

### Authentication

First, you need to authenticate yourself with your [O'Reilly](https://www.oreilly.com/) credentials to access the resources. The `auth` spider does this automatically. Before running the spider, you need to create a file called `auth.sh` in the `keys/raw` directory of the repository and save the `cURL` command for logging in:

1. In a web browser, [log in to O'Reilly](https://www.oreilly.com/member/login/) using your credentials.

2. Use a web developer tool such as the network tab to capture the `cURL` command for the login request.

3. Save the cURL command as a `auth.sh` file in the `keys/raw` directory. For example, you could create a file called `auth.sh` with the following contents.

4. Run the scraper using the command `scrapy crawl auth`. This will log you in to [O'Reilly](https://www.oreilly.com/) and save the necessary session cookies for future requests.


### Collecting Catalogue Information

The `catalogue` spider collects information about all books and other resources from [O'Reilly catalogue](https://learning.oreilly.com/topics/) and stores them as a *CSV*, *JSON*, and *JSONLines* files locally in `data/csv`, `data/json`, and `data/jsonline` directories respectively, and store the *JSON* formatted records in MongoDB collections called `catalogue` after the spider name:

1. In a web browser, [log in to O'Reilly](https://www.oreilly.com/member/login/) using your credentials.

2. Use a web developer tool such as the network tab to capture the `cURL` command for the request that fetches paginated resource information and save it in `catalogue.sh` under the `keys/raw` directory.

3. In the terminal, navigate to the project directory.

4. Run the scraper using the command scrapy crawl catalogue -o catalogue.json. This will collect information about all books and other resources from [O'Reilly catalogue](https://learning.oreilly.com/topics/) and save it as a *CSV*, *JSON*, and *JSONLines* files in `data/csv`, `data/json`, and `data/jsonline` directories respectively, and store the *JSON* formatted records in MongoDB collections called `catalogue` after the spider name.


### Downloading and Pre-Processing Resources

The `book` spider downloads, pre-processes the scraped HTML, CSS, and image resources, and saves them locally in directories **based on their category and book title**:

1. In a web browser, [log in to O'Reilly](https://www.oreilly.com/member/login/) using your credentials.

2. Use a web developer tool such as the network tab to capture the `cURL` command for the request that fetches book information and downloads an image and save them in `book.sh` and `image.sh` respectively under the `keys/raw` directory.

3. In the terminal, navigate to the project directory.

4. Run the scraper using the command scrapy crawl book. This will download and pre-process the HTML, CSS, and image resources for each book in your O'Reilly subscription and save them locally based on their category and book title. The pre-processing includes, but not limited to, fixing links so that the final PDF is a more readable and complete representation of the book.

5. Information about each individual book in *JSON* format, which is also the source of the URLs for the corresponding HTMLs, CSSs, and images, will be stored in a MongoDB collection called `book` along with some metadata.


### Combining Resources into PDFs

After running the `book` spider, you can *combine all corresponding resources* (HTMLs, CSSs, and images) for each individual book and create **one PDF per book** by running the following command:

1. In the terminal, navigate to the project directory.

2. Run the command `python services/pdfmaker.py`. This will *combine all the corresponding resources* (HTMLs, CSSs, and images) for each individual book and create **one PDF per book**. The PDFs will be saved in the `data/books` directory.


## Contributing

Contributions are always welcome! Please follow these steps to contribute:

1. Fork the repository.

2. Create a new branch for your feature or bug fix.

3. Make your changes and test thoroughly.

4. Submit a pull request with a clear description of your changes.

Thank you for contributing to *Crawreilly*!


## License

This project is licensed under the **Apache License Version 2.0** - see the [LICENSE](https://github.com/rifatrakib/crawreilly/blob/master/LICENSE) file for details.
