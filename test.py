import re

def get_unique_words(filename):
    with open(filename, 'r') as file:
        content = file.read()
        pattern = r'\b\w+\b'
        matches = re.findall(pattern, content)
        keywords = set(matches)
        return list(keywords)
print(get_unique_words("fichier.txt"))