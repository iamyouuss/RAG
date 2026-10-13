import os
from .models import MinimalSource


class Indexer():
    def __init__(self) -> None:
        ...


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
        self.indexer.add_source(chunk)

    def code_chunking(self, file_path: str, content: str, length: int) -> None:
        ...

    def text_chunking(self, file_path: str, content: str, length: int) -> None:
        ...

    def chunking_files(self, file_path: str, content: str, length: int
                       ) -> None:
        if length <= self.chunk_size:
            self.add_source(file_path, 0, length - 1)
        else:
            match file_path.split(".")[-1]:
                case "py":
                    self.code_chunking(file_path, content, length)
                case "txt" | "md":
                    self.text_chunking(file_path, content, length)


class FileLoader():
    def __init__(self, path: str, chunker: Chunker) -> None:
        self.chunker = chunker
        self.path: str = path

    def open_files(self) -> None:
        for root, _, files in os.walk(self.path):
            for file in files:
                if file.endswith((".txt", ".md", ".py")):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        content = f.read()
                        self.chunker.chunking_files(file_path, content,
                                                    len(content))


class RAG():
    def __init__(self, path: str, chunk_size: int) -> None:
        self.path: str = path
        self.chunk_size: int = chunk_size

    def get_started(self) -> None:
        indexer = Indexer()
        chunker = Chunker(self.chunk_size, indexer)
        Fl = FileLoader(self.path, chunker)
        Fl.open_files()
