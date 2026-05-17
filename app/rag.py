# app/rag.py
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

class RAGSystem:
    def __init__(self):
        self.embeddings = SentenceTransformerEmbeddings(
            model_name="paraphrase-multilingual-MiniLM-L12-v2"
           
        )
        self.vectordb = None
    
    def load_documents(self, file_path: str):
        """FAQ বা Document load করো"""
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        
       
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = splitter.create_documents([text])
        
        # Vector DB  save 
        self.vectordb = Chroma.from_documents(
            chunks,
            self.embeddings,
            persist_directory="./chroma_db"
        )
        print(f"✅ {len(chunks)} chunks loaded!")
    
    def search(self, query: str, k: int = 3):
        """User question এর সাথে relevant info খোঁজো"""
        if not self.vectordb:
            self.vectordb = Chroma(
                persist_directory="./chroma_db",
                embedding_function=self.embeddings
            )
        
        results = self.vectordb.similarity_search(query, k=k)
        context = "\n".join([doc.page_content for doc in results])
        return context