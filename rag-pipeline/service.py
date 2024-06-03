import bentoml

from haystack import Pipeline, Document

from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.generators import HuggingFaceLocalGenerator

from haystack.components.builders.prompt_builder import PromptBuilder

"""
Basic question answering RAG pipeline packed into a bento service
to easily get optimized docker containers for downstream deployment. 
"""


@bentoml.service
class Basicpipeline:
    def __init__(self) -> None:
        self.document_store = self._setup_document_store()
        # Basic RAG template with some encouragement (https://arxiv.org/abs/2402.14531)
        self.prompt_template = """
        Given the documents below, answer the question. Be precise
        and exact in your answer. I believe that you can do it! 
        Documents:
        {% for doc in documents %}
            {{ doc.content }}
        {% endfor %}
        Question: {{question}}
        Answer:
        """

        self.rag_pipeline = self._construct_rag_pipeline()

    def _construct_rag_pipeline(self):
        retriever = InMemoryBM25Retriever(document_store=self.document_store)
        prompt_builder = PromptBuilder(template=self.prompt_template)
        llm = HuggingFaceLocalGenerator(
            model="google/flan-t5-large",
            task="text2text-generation",
        )

        rag_pipeline = Pipeline()
        rag_pipeline.add_component("llm", llm)

        rag_pipeline.add_component("retriever", retriever)
        rag_pipeline.add_component("prompt_builder", prompt_builder)

        rag_pipeline.connect("prompt_builder", "llm")
        rag_pipeline.connect("retriever", "prompt_builder.documents")
        return rag_pipeline

    def _setup_document_store(self):
        # Setup a in memory store
        document_store = InMemoryDocumentStore()
        document_store.write_documents(
            [
                Document(content="Naim hates brussels sprouts"),
                Document(
                    content="John is looking for a solar panel provider to reduce his energy costs. "
                ),
                Document(content="Mary is a chartered accountant"),
            ]
        )

        return document_store

    # Endpoint to answer a simple question
    @bentoml.api
    def ask(self, question: str = "Who is a chartered accountant?") -> str:
        results = self.rag_pipeline.run(
            {
                "retriever": {"query": question},
                "prompt_builder": {"question": question},
            }
        )

        if len(results["llm"]["replies"]) > 0:
            return results["llm"]["replies"][0]

        return "You asked a very hard question!"
