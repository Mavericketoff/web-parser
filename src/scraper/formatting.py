import os


def apply_formatting(text: str, config: dict) -> str:
    """
    Apply formatting to the text based on the provided configuration.

    Args:
        text (str): The input text to be formatted.
        config (dict): The configuration settings.

    Returns:
        str: The formatted text.
    """
    formatted_text = ''
    paragraphs = text.split('\n\n')

    for paragraph in paragraphs:
        lines = paragraph.split('\n')
        for line in lines:
            words = line.split()
            line_length = 0

            for word in words:
                if '[' in word and ']' in word:
                    formatted_text += word + ' '
                    line_length += len(word) + 1
                elif line_length + len(word) <= config.get("line_length", 80):
                    formatted_text += word + ' '
                    line_length += len(word) + 1
                else:
                    formatted_text = formatted_text.rstrip() + '\n'
                    formatted_text += word + ' '
                    line_length = len(word) + 1

            formatted_text += '\n'

        if config.get("paragraph_spacing", True):
            formatted_text += '\n'

    return formatted_text.rstrip()


def generate_output_filename(url: str, output_format: str, output_folder: str = 'generated') -> str:
    """
    Generate the output filename based on the URL and output format.

    Args:
        url (str): The URL of the webpage.
        output_format (str): The desired output format.
        output_folder (str): The folder to save the file in.

    Returns:
        str: The generated output filename.
    """
    url_parts = url[url.index('//') + 1:].replace('/', '_')

    filename = os.path.join('..', output_folder, url_parts + '.' + output_format)
    return filename
