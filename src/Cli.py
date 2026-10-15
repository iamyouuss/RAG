
import os


class CLI():
    def __init__(self) -> None:
        self.files_path: list[str] = []

    def process_data(self, path_to_raw: str = "data/raw") -> list[str]:
        files_path: list[str] = []
        for root, _, files in os.walk(path_to_raw):
            for file in files:
                if file.endswith((".txt", ".md", ".py")):
                    file_path = os.path.join(root, file)
                    files_path.append(file_path)
                    # with open(file_path, 'r') as f:
                    #    content = f.read()
        return files_path

    def index(self, path_to_raw: str = "data/raw",
              path_to_processed: str = "data/processed",
              max_chunk_size: int = 2000):
        self.files_path = self.process_data(path_to_raw)


    def search(self, query: str, k: int):
        ...

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
