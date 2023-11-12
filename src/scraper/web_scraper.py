import os
import requests
from bs4 import BeautifulSoup

from scraper.formatting import apply_formatting


class Content:
    def __init__(self, url: str, title: str, body: str):
        """
        Represents the content of a webpage.

        Args:
            url (str): The URL of the webpage.
            title (str): The title of the webpage.
            body (str): The body/content of the webpage.
        """
        self.url = url
        self.title = title
        self.body = body


class WebScraper:

    def __init__(self, url: str, config: dict):
        """
        Initializes the WebScraper.

        Args:
            url (str): The URL of the webpage to scrape.
            config (dict): The configuration settings.
        """
        self.url = url
        self.html = self.get_html()
        self.config = config

    def get_html(self) -> str:
        """
        Retrieves the HTML content of the webpage.

        Returns:
            str: The HTML content.
        """
        response = requests.get(self.url)
        return response.text

    def extract_text(self) -> Content:
        """
        Extracts text content from the webpage.

        Returns:
            Content: The content of the webpage.
        """
        soup = BeautifulSoup(self.html, 'html.parser')
        title_bs = soup.find("title")
        if title_bs:
            title = title_bs.text
        else:
            title = ' '
        lines = soup.find_all(['p', 'h1', 'h2'])
        body = '\n\n'.join([self.process_element(line) for line in lines])
        return Content(self.url, title, body)

    def process_element(self, element) -> str:
        """
        Processes an HTML element and returns the formatted text.

        Args:
            element: The HTML element.

        Returns:
            str: The formatted text.
        """
        if element.name.startswith('h'):
            return '\n' + element.get_text().strip() + '\n'
        else:
            for link in element.find_all('a'):
                link_text = link.get_text().strip()
                link_url = self.config.get("link_format", "[{url}]").format(url=link["href"])
                link.replace_with(link_text + ' ' + link_url)
            return element.get_text().strip() + ' '

    def format_text(self, text: str) -> str:
        """
        Applies formatting to the text content.

        Args:
            text (Content): The content of the webpage.

        Returns:
            str: The formatted text.
        """
        return apply_formatting(text, self.config)

    @staticmethod
    def save_to_file(
            content: Content,
            formatted_text: str,
            output_file: str
    ) -> None:
        """
        Saves the formatted content to a file.

        Args:
            content (Content): The content of the webpage.
            formatted_text (str): The formatted text.
            output_file (str): The output file path.
        """
        try:
            # Extract the directory from the output_file
            output_directory = os.path.dirname(output_file)

            # Check if the directory exists, create it if not
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)

            # Write the content to the file
            with open(output_file, 'w', encoding='utf-8') as f:
                print("Заголовок: {}".format(content.title), file=f)
                print("\nАдрес    : {}\n".format(content.url), file=f)
                print(formatted_text, file=f)

        except Exception as e:
            print(f"Произошла ошибка при сохранении файла: {e}")

