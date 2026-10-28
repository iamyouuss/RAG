from src.models import (MinimalAnswer, MinimalSource, StudentSearchResults,
                        MinimalSearchResults, StudentSearchResultsAndAnswer)


class Generator():
    def retrieve_chunk(self, source: MinimalSource) -> str:
        start = source.first_character_index
        end = source.last_character_index
        with open(source.file_path, "r", encoding="utf-8") as f:
            content = f.read()
            return content[start:end]

    def generate(self):
        ...

    def single_answer(self, search_results: MinimalSearchResults
                      ) -> MinimalAnswer:
        answer = "answer"
        return MinimalAnswer(
            question_id=search_results.question_id,
            question=search_results.question,
            sources=search_results.retrieved_sources,
            answer=answer
        )

    def dataset_answer(self, student_search_results: StudentSearchResults
                       ) -> StudentSearchResultsAndAnswer:
        ssra = StudentSearchResultsAndAnswer(search_results=[],
                                             k=student_search_results.k)
        for search_results in student_search_results.search_results:
            minimal_answer = self.single_answer(search_results)
            ssra.search_results.append(minimal_answer)
