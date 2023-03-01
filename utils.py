import spacy
from collections import Counter
import pathlib

nlp = spacy.load("fr_core_news_sm")
def textee(file_path):
    doc = nlp(pathlib.Path(file_path).read_text(encoding="utf-8"))
    words = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    result_wo=Counter(words).most_common(5)
    result=[]
    for i in range(len(result_wo)):
        result.append(result_wo[i][0])
    return result