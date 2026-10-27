from .models import MinimalSource
from .Indexer import Indexer


class Chunker():
    def __init__(self, chunk_size: int, indexer: Indexer) -> None:
        self.counter: int = 1
        self.chunk_size: int = chunk_size
        self.sources: dict[str, MinimalSource] = {}
        self.indexer = indexer

    def add_source(self, file_path: str, chunked_content: str,
                   start: int, end: int) -> None:
        chunk = MinimalSource(file_path=file_path,
                              first_character_index=start,
                              last_character_index=end)
        chunk_nb = f"chunk_{self.counter}"
        self.sources[chunk_nb] = chunk
        self.counter += 1
        self.indexer.index_source(chunked_content, chunk_nb)

    def code_chunking(self, file_path: str, content: str, length: int) -> None:
        for i in range(0, length, self.chunk_size):
            end = min(i + self.chunk_size, length)
            chunked_content = content[i:end]
            self.add_source(file_path, chunked_content, i, end)

    def text_chunking(self, file_path: str, content: str, length: int) -> None:
        for i in range(0, length, self.chunk_size):
            end = min(i + self.chunk_size, length)
            chunked_content = content[i:end]
            self.add_source(file_path, chunked_content, i, end)

    def chunk_file(self, file_path: str) -> None:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            length = len(content)
        except FileNotFoundError:
            print(f"Cannot open file '{file_path}'")
            return
        if length == 0:
            return
        if length <= self.chunk_size:
            self.add_source(file_path, content[0: length], 0, length)
        else:
            match file_path.split(".")[-1]:
                case "py":
                    self.code_chunking(file_path, content, length)
                case "txt" | "md":
                    self.text_chunking(file_path, content, length)
