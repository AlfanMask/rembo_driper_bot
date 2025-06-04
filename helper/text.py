import re

def fix_markdown(text):
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