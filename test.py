import re

def get_unique_words(filename):
    content = file.read()
    pattern = r'\b\w+\b'
    matches = re.findall(pattern, content)
    keywords = set(matches)
    return list(keywords)
# print(get_unique_words("fichier.txt"))
file="fichier.txt"
def get_file_extension(file):
    return file.split(".")[-1]
def verify_extension(file_name):
    if get_file_extension()=="txt":
            t_txt = open(file_name, "r")
            get_unique_words(t)
        

