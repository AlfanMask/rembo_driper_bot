import re

def fix_markdown(text):
    # Remove escaping backslashes
    text = text.replace('\\', '')

    # Ensure bold and italic formatting is correctly applied
    text = re.sub(r'\*\*(.*?)\*\*', r'**\1**', text)  # Bold
    text = re.sub(r'\*(.*?)\*', r'*\1*', text)  # Italic

    # Replace double spaces with a single space
    text = text.replace('  ', ' ')

    return text