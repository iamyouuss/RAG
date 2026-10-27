from collections import defaultdict
import math
from .models import (MinimalSource, MinimalSearchResults,
                     StudentSearchResults, RagDataset)
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
                self.total_chunks if self.total_chunks > 0 else 1)

    def term_score(self, tf: int, doc_length: int) -> float:
        return tf * (self.k1 + 1) / (tf + self.k1 * (1 - self.b + self.b * (
            doc_length / self.avg_length)))

    def inverted_document_frequency(self, document_frequency: int) -> float:
        return math.log(1 + (self.total_chunks - document_frequency + 0.5) /
                        (document_frequency + 0.5))

    def get_top_k_sources(self, bm25_scores: defaultdict[str, float],
                          k: int) -> list[MinimalSource]:
        sorted_chunks = sorted(bm25_scores.items(),
                               key=lambda a: a[1], reverse=True)
        top_k_ids = [chunk_id for chunk_id, _ in sorted_chunks[:k]]
        return [self.sources[chunk_id] for chunk_id in top_k_ids]

    def single_retrieve(self, query: str, k: int) -> list[MinimalSource]:
        if not query.strip():
            print("Query is empty. Please provide a valid query.")
            return []
        if k <= 0:
            print(f"Invalid value for k: {k}. It should be superior to 0.")
            return []
        max_k = min(k, len(self.sources))
        indexer = Indexer()
        query_words = indexer.clean_content(query)
        if not query_words:
            print("No valid query words found.")
            return []
        bm25_scores: defaultdict[str, float] = defaultdict(float)
        for word in query_words:
            if word in self.index:
                df = len(self.index[word])
                for chunk_id, tf in self.index[word].items():
                    doc_length = self.sources[chunk_id].size
                    idf = self.inverted_document_frequency(df)
                    score = self.term_score(tf, doc_length)
                    bm25_scores[chunk_id] += (idf * score)
        return self.get_top_k_sources(bm25_scores, max_k)

    def dataset_retrieve(self, rag_dataset: RagDataset, k: int
                         ) -> StudentSearchResults:
        student_search_results = StudentSearchResults(search_results=[], k=k)
        for qst in rag_dataset.rag_questions:
            question_id = qst.question_id
            question = qst.question
            retrieved_sources = self.single_retrieve(question, k)
            search_result = MinimalSearchResults(
                question_id=question_id,
                question=question,
                retrieved_sources=retrieved_sources
                )
            student_search_results.search_results.append(search_result)
        return student_search_results
