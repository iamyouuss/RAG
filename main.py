from src import RAG


def main() -> None:
    rag = RAG(path="data/raw/vllm-0.10.1")
    rag.get_started()


if __name__ == "__main__":
    main()
