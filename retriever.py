from langchain_community.docstore.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from smolagents import Tool
from langchain_community.retrievers import BM25Retriever
from smolagents import CodeAgent, InferenceClientModel
import json

with open("alzheimer_targets.json", "r", encoding="utf-8") as f:
    data = json.load(f)

source_docs = [
    Document(page_content=doc["full_text"], metadata={"source": doc["pmcid"]})
    for doc in data
]

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=150,
    add_start_index=True,
    strip_whitespace=True,
    separators=["\n\n", "\n", ".", " ", ""],
)
docs_processed = text_splitter.split_documents(source_docs)



class RetrieverTool(Tool):
    name = "retriever"
    description = "Uses semantic search to retrieve the parts of transformers documentation that could be most relevant to answer your query."
    inputs = {
        "query": {
            "type": "string",
            "description": "The query to perform. This should be semantically close to your target documents. Use the affirmative form rather than a question.",
        }
    }
    output_type = "string"

    def __init__(self, docs, **kwargs):
        super().__init__(**kwargs)
        s
        self.retriever = BM25Retriever.from_documents(
            docs, k=10
        )

    def forward(self, query: str) -> str:

        assert isinstance(query, str), "Your search query must be a string"


        docs = self.retriever.invoke(query)


        return "\nRetrieved documents:\n" + "".join(
            [
                f"\n\n===== Document {str(i)} , source {doc.metadata['source']}=====\n" + doc.page_content
                for i, doc in enumerate(docs)
            ]
        )

retriever_tool = RetrieverTool(docs_processed)