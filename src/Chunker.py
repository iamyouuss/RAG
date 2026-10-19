from .models import MinimalSource
from .Indexer import Indexer


class Chunker():
    def __init__(self, chunk_size: int, indexer: Indexer) -> None:
        self.counter: int = 1
        self.chunk_size: int = chunk_size
        self.sources: dict[str, MinimalSource] = {}
        self.indexer = indexer

    def add_source(self, file_path: str, start: int, end: int) -> None:
        chunk = MinimalSource(file_path=file_path,
                              first_character_index=start,
                              last_character_index=end)
        self.sources[f"chunk_{self.counter}"] = chunk
        self.counter += 1
        self.indexer.index_source(chunk)

    def code_chunking(self, file_path: str, content: str, length: int) -> None:
        self.add_source(file_path, 0, 200)

    def text_chunking(self, file_path: str, content: str, length: int) -> None:
        self.add_source(file_path, 0, 200)

    def chunk_file(self, file_path: str) -> None:
        with open(file_path, 'r') as f:
            content = f.read()
        length = len(content)
        if length <= self.chunk_size:
            self.add_source(file_path, 0, length - 1)
        else:
            match file_path.split(".")[-1]:
                case "py":
                    self.code_chunking(file_path, content, length)
                case "txt" | "md":
                    self.text_chunking(file_path, content, length)
