import os
from .models import MinimalSource


def retrieve_files(file_path: str, content: str, length: int) -> None:
    limit = 2000
    _ = content.split()
    if length < limit:
        source = MinimalSource(file_path=file_path,
                               first_character_index=0,
                               last_character_index=length - 1)
        os.makedirs("data/processed", exist_ok=True)
        with open("data/processed/sources.txt", "a") as f:
            f.write(f"{source.json()}\n")
    else:
        print(f"File {file_path} is too long ({length} characters). Splitting into chunks of {limit} characters.")
    for i in range(0, length):
        ...


def open_files() -> None:
    path = "data/raw/vllm-0.10.1"
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith((".txt", ".md", ".py")):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                    retrieve_files(file_path, content, len(content))
