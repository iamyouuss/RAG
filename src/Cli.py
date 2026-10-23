from .Indexer import Indexer
from .Chunker import Chunker
from .Retriever import Retriever
import os
import json


class CLI():
    def __init__(self) -> None:
        self.files_path: list[str] = []
        self.chunker: Chunker
        self.indexer: Indexer
        self.retriever: Retriever

    def process_data(self, path_to_raw: str) -> None:
        files_path: list[str] = []
        for root, _, files in os.walk(path_to_raw):
            for file in files:
                if file.endswith((".txt", ".md", ".py")):
                    file_path = os.path.join(root, file)
                    files_path.append(file_path)
        self.files_path = files_path

    def index(self, path_to_raw: str = "data/raw",
              path_to_processed: str = "data/processed",
              max_chunk_size: int = 2000):
        self.process_data(path_to_raw)

        self.indexer = Indexer()
        self.chunker = Chunker(max_chunk_size, self.indexer)

        for file_path in self.files_path:
            self.chunker.chunk_file(file_path)

        os.makedirs(path_to_processed, exist_ok=True)
        path_to_sources = os.path.join(path_to_processed, "sources.json")
        path_to_index = os.path.join(path_to_processed, "index.json")

        with open(path_to_sources, "w", encoding="utf-8") as f:
            json.dump(self.chunker.sources, f,
                      default=lambda x: x.model_dump(), indent=4)

        with open(path_to_index, "w", encoding="utf-8") as f:
            json.dump(self.indexer.index, f, indent=4)

    def search(self, query: str, k: int,
               path_to_processed: str = "data/processed") -> None:
        self.retriever = Retriever(path_to_processed)
        self.retriever.get_k_sources(query, k)

    def search_datasets(self, k: int,
                        data_set_path: str = "data/raw",
                        save_directory: str = "data/processed",
                        ):
        ...

    def answer(self, query: str, k: int):
        ...

    def answer_dataset(self, student_search_results_path: str,
                       save_directory: str = "data/processed"):
        ...
