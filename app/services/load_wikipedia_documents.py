from langchain_community.document_loaders import WikipediaLoader

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)

def load_wikipedia_documents(query: str):
    loader = WikipediaLoader(query=query, load_max_docs=3)
    docs = loader.load()
    return text_splitter.split_documents(docs)