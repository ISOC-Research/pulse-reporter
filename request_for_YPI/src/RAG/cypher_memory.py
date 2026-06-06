import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

# Configuration of persistent storage path for this specific memory
MEMORY_DB_PATH = os.path.join("data", "cypher_memory_db")

class CypherMemory:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        # We use a separate collection to avoid polluting the document RAG
        self.vector_store = Chroma(
            persist_directory=MEMORY_DB_PATH,
            embedding_function=self.embeddings,
            collection_name="successful_cypher_queries"
        )

    def save_query(self, user_question, cypher_query, explanation="Valid query"):
        """
        Saves a successful query.
        """
        # We format the content to be readable by the LLM during retrieval
        content_to_embed = f"QUESTION: {user_question}\nCYPHER_QUERY: {cypher_query}\nEXPLANATION: {explanation}"
        
        # We add metadata to be able to filter if needed
        metadata = {
            "type": "cypher_example",
            "question": user_question,
            "query": cypher_query
        }
        
        doc = Document(page_content=content_to_embed, metadata=metadata)
        self.vector_store.add_documents([doc])
        print(f"💾 Cypher query saved in memory for: {user_question[:30]}...")

    def get_similar_examples(self, user_question, k=3):
        """
        Retrieves the k semantically closest examples.
        """
        try:
            results = self.vector_store.similarity_search(user_question, k=k)
            if not results:
                return ""
            
            # Format the examples for the prompt
            formatted_examples = "\n\n".join([f"--- EXAMPLE {i+1} ---\n{doc.page_content}" for i, doc in enumerate(results)])
            return formatted_examples
        except Exception as e:
            print(f"⚠️ Error retrieving Cypher memory: {e}")
            return ""

# Global instance
cypher_memory = CypherMemory()  