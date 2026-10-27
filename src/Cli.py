from .Indexer import Indexer
from .Chunker import Chunker
from .Retriever import Retriever
from .Generator import Generator
import os
from pathlib import Path
import json
from .models import RagDataset, StudentSearchResults
from pydantic import ValidationError

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"


class CLI():
    def __init__(self) -> None:
        self.files_path: list[str]

    def init_retriever(self, processed_dir: str) -> Retriever | None:
        try:
            retriever = Retriever(Path(processed_dir))
            return retriever
        except FileNotFoundError:
            print("Cannot accessed processed data for retrieving. "
                  "Did you launched 'index' command ?")
            return None

    def process_data(self, path_to_raw: str) -> None:
        self.files_path = []
        for root, _, files in os.walk(path_to_raw):
            for file in files:
                if file.endswith((".txt", ".md", ".py")):
                    file_path = os.path.join(root, file)
                    self.files_path.append(file_path)

    def index(self, max_chunk_size: int = 2000) -> None:
        self.process_data(RAW_DIR)

        if max_chunk_size <= 0:
            print(f"Invalid value for max_chunk_size: {max_chunk_size}. "
                  "It should be superior to 0.")
            return
        indexer = Indexer()
        chunker = Chunker(max_chunk_size, indexer)

        for file_path in self.files_path:
            chunker.chunk_file(file_path)

        try:
            os.makedirs(PROCESSED_DIR, exist_ok=True)
            processed_dir = Path(PROCESSED_DIR)
            path_to_sources = processed_dir / "sources.json"
            path_to_index = processed_dir / "index.json"

            with open(path_to_sources, "w", encoding="utf-8") as f:
                json.dump(chunker.sources, f,
                          default=lambda x: x.model_dump(), indent=4)

            with open(path_to_index, "w", encoding="utf-8") as f:
                json.dump(indexer.index, f, indent=4)
        except FileNotFoundError as e:
            print(f"Error occurred while saving index and sources: {e}")

    def search(self, query: str, k: int) -> None:
        retriever = self.init_retriever(PROCESSED_DIR)
        if retriever is None:
            return

        results = retriever.single_retrieve(query, k)
        for result in results:
            print(f"{result.file_path} [{result.first_character_index}:"
                  f"{result.last_character_index}]")

    def search_dataset(self, dataset_path: str, k: int,
                       save_directory: str = "data/output/search_results"
                       ) -> None:
        try:
            with open(dataset_path, "r", encoding="utf-8") as f:
                questions = json.load(f)
                rag_dataset = RagDataset(**questions)
        except FileNotFoundError as e:
            print(f"Cannot open file {dataset_path}: {e}")
            return
        except ValidationError as e:
            print(f"Error occurred while loading dataset: {e}")
            return

        retriever = self.init_retriever(PROCESSED_DIR)
        if retriever is None:
            return

        try:
            ssr: StudentSearchResults = retriever.dataset_retrieve(
                rag_dataset, k)
            save_dir = Path(save_directory)
            path_to_save = save_dir / Path(dataset_path).name
            save_dir.mkdir(parents=True, exist_ok=True)
            with open(path_to_save, "w", encoding="utf-8") as f:
                json.dump(ssr.model_dump(), f, indent=4)
        except FileNotFoundError as e:
            print(f"Error occurred while saving search results: {e}")

    def answer(self, query: str, k: int) -> None:
        generator = Generator()
        generator.generate()

    def answer_dataset(
            self, student_search_results_path: str,
            save_directory: str = "data/output/search_results_and_answer"
            ) -> None:
        ...
