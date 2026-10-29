from src.models import (MinimalAnswer, MinimalSource, StudentSearchResults,
                        MinimalSearchResults, StudentSearchResultsAndAnswer)
from transformers import pipeline

MODEL_NAME = "Qwen/Qwen3-0.6B"


class Generator():
    def __init__(self, model_name: str = MODEL_NAME) -> None:
        self.pipe = pipeline(
            "text-generation",
            model=model_name
        )

    def retrieve_chunk(self, source: MinimalSource) -> str:
        start = source.first_character_index
        end = source.last_character_index
        with open(source.file_path, "r", encoding="utf-8") as f:
            content = f.read()
            return content[start:end]

    def build_context(self, question: str, sources: list[MinimalSource]
                      ) -> list[dict[str, str]]:
        context = "\n".join([self.retrieve_chunk(s) for s in sources])
        return [
            {
                "role": "system",
                "content": (
                    "You are a strict and helpful assistant. "
                    "Answer the question in exactly ONE single, "
                    "concise sentence using ONLY the provided sources. "
                    "Do not include any reasoning, thinking process, "
                    "or extra explanations. If you cannot find the answer "
                    "in the sources, just say 'I don't know'."
                    )
            },
            {
                "role": "user",
                "content": (f"Context: {context}\n\n Question: {question}")
            }
        ]

    def generate(self, prompt: list[dict[str, str]]) -> str:
        output = self.pipe(prompt, max_new_tokens=400)
        text = output[0]["generated_text"][-1]["content"]
        if "</think>" in text:
            text = text.split("</think>")[-1].strip()
        return text

    def single_answer(self, search_results: MinimalSearchResults
                      ) -> MinimalAnswer:
        prompt = self.build_context(search_results.question,
                                    search_results.retrieved_sources)
        answer = self.generate(prompt)
        return MinimalAnswer(
            question_id=search_results.question_id,
            question=search_results.question,
            retrieved_sources=search_results.retrieved_sources,
            answer=answer
        )

    def dataset_answer(self, student_search_results: StudentSearchResults
                       ) -> StudentSearchResultsAndAnswer:
        return StudentSearchResultsAndAnswer(
            search_results=[
                self.single_answer(search_results)
                for search_results in student_search_results.search_results],
            k=student_search_results.k)
