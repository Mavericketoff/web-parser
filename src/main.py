from scraper.formatting import generate_output_filename
from scraper.web_scraper import WebScraper, Content
from colorama import Fore, Style
from art import text2art
import json
import argparse


def parse_command_line_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(description='Web Scraper')
    parser.add_argument(
        '--url',
        required=True,
        help='URL of the webpage to scrape'
    )
    parser.add_argument(
        '--config',
        default='configs/config.json',
        help='Path to the configuration file'
    )
    return parser.parse_args()


def load_config(config_file: str) -> dict:
    """
    Load configuration from a JSON file.

    Args:
        config_file (str): Path to the configuration file.

    Returns:
        dict: Loaded configuration.
    """
    with open(config_file, 'r', encoding='utf-8') as file:
        return json.load(file)


def main():
    args = parse_command_line_arguments()
    config = load_config(args.config)
    scraper = WebScraper(args.url, config)
    content = scraper.extract_text()
    formatted_text = scraper.format_text(content.body)
    output_file = generate_output_filename(
        args.url,
        config.get("output_format", "txt"),
        output_folder='generated'
    )
    scraper.save_to_file(content, formatted_text, output_file)
    author(content, formatted_text, output_file)


def author(content: Content,
           formatted_text: str,
           output_file: str
           ) -> None:
    # Добавление цвета к выводу с помощью colorama
    print(f"{Fore.BLUE}Заголовок: {content.title}{Style.RESET_ALL}")
    print(f"\n{Fore.GREEN}Адрес    : {content.url}\n{Style.RESET_ALL}")
    print(formatted_text)

    ascii_art = text2art("Web Scraper")
    print(f"\n{Fore.LIGHTMAGENTA_EX}{ascii_art}{Style.RESET_ALL}")
    print(f"\n{Fore.LIGHTMAGENTA_EX}By: Mavericketoff\n")


if __name__ == '__main__':
    main()
