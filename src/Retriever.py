from collections import defaultdict
import math

from .models import MinimalSource
import os
import json
from .Indexer import Indexer


class Retriever():
    def __init__(self, processed_dir: str) -> None:
        self.k1: float = 1.5
        self.b: float = 0.75

        with open(os.path.join(processed_dir, "index.json"), "r") as f:
            self.index = json.load(f)

        with open(os.path.join(processed_dir, "sources.json"), "r") as f:
            retrieved_sources = json.load(f)
            self.sources = {
                source_id: MinimalSource(**source_data)
                for source_id, source_data in retrieved_sources.items()
            }

        self.total_chunks: int = len(self.sources)
        self.avg_length: float = sum(
            source.size for source in self.sources.values()) / (
                self.total_chunks if self.total_chunks > 0 else 0)
        self.bm25_scores: defaultdict[float] = defaultdict(float)

    def term_frequency(self, term: str, document_id: str) -> int:
        ...

    def inverted_document_frequency(self, document_frequency: int) -> float:
        return math.log(1 + (self.total_chunks - document_frequency + 0.5) /
                        (document_frequency + 0.5))

    def get_bm25_score(self, term_frequency: int, doc_length: int) -> float:
        ...

    def get_k_sources(self, query: str, k: int) -> None:
        indexer = Indexer()
        query_words = indexer.clean_content(query)
        if not query_words:
            print("No valid query words found.")
            return
        for word in query_words:
            if word in self.index:
                ...
