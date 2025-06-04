import re

def fix_markdown(text):
    # Remove escaping backslashes
    text = text.replace('\\', '')

    # Ensure bold and italic formatting is correctly applied
    text = re.sub(r'\*\*(.*?)\*\*', r'**\1**', text)  # Bold
    text = re.sub(r'\*(.*?)\*', r'*\1*', text)  # Italic

    # Replace double spaces with a single space
    text = text.replace('  ', ' ')

    # Replace double newline with a single newline
    text = text.replace('\n\n\n', '\n\n')

    return text

def fix_markdown_no_new_lines(text):
    # Remove escaping backslashes
    text = text.replace('\\', '')

    # Ensure bold and italic formatting is correctly applied
    text = re.sub(r'\*\*(.*?)\*\*', r'**\1**', text)  # Bold
    text = re.sub(r'\*(.*?)\*', r'*\1*', text)        # Italic

    # Replace multiple spaces with a single space
    text = re.sub(r' {2,}', ' ', text)

    # Replace two or more newlines with a single newline
    text = re.sub(r'\n{2,}', '\n', text)

    return text