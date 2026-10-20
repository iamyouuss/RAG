from collections import defaultdict
import re

TOKEN_PATTERN = re.compile(r"\w+")
ENGLISH_STOP_WORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an",
    "and", "any", "are", "as", "at", "be", "because", "been", "before",
    "being", "below", "between", "both", "but", "by", "can", "did", "do",
    "does", "doing", "don", "down", "during", "each", "few", "for", "from",
    "further", "had", "has", "have", "having", "he", "her", "here", "hers",
    "herself", "him", "himself", "his", "how", "i", "if", "in", "into", "is",
    "it", "its", "itself", "just", "me", "more", "most", "my", "myself", "no",
    "nor", "not", "now", "of", "off", "on", "once", "only", "or", "other",
    "our", "ours", "ourselves", "out", "over", "own", "s", "same", "she",
    "should", "so", "some", "such", "t", "than", "that", "the", "their",
    "theirs", "them", "themselves", "then", "there", "these", "they", "this",
    "those", "through", "to", "too", "under", "until", "up", "very", "was",
    "we", "were", "what", "when", "where", "which", "while", "who", "whom",
    "why", "will", "with", "you", "your", "yours", "yourself", "yourselves"
}


class Indexer():
    def __init__(self) -> None:
        self.index: defaultdict[
            str, defaultdict[str, int]] = defaultdict(lambda: defaultdict(int))

    def clean_content(self, content: str) -> list[str]:
        tokens = TOKEN_PATTERN.findall(content.lower())
        return [word for word in tokens if word not in ENGLISH_STOP_WORDS]

    def index_source(self, content: str, chunk_nb: str) -> None:
        words_list = self.clean_content(content)
        for word in words_list:
            self.index[word][chunk_nb] += 1
