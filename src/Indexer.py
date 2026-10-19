class Indexer():
    def __init__(self) -> None:
        self.inverted_index: dict[str, int] = {}

    def ponctuation(self, content: str) -> str:
        ...

    def normalize(self, content: str) -> str:
        ...

    def filter_words(self, content: str) -> str:
        ...

    def clean_sources(self, content: str) -> str:
        content = self.ponctuation(content)
        content = self.normalize(content)
        content = self.filter_words(content)

    def index_source(self, content: str) -> None:
        cleaned_content = self.clean_sources(content)
        cleaned_content.count()
