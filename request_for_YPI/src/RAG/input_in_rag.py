from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.utils.logger import logger
from src.RAG.embedding import get_embedding_model
from src.RAG.knowledges_graph import store_document_with_chunks
from src.tools.summarize_text import summarize_raw_content



def input_in_rag(text: str, url: str, source_type: str):
    """
    Fonction DÉDIÉE à l'ingestion RAG.
    Gère le nettoyage, le découpage, la vectorisation et le stockage.
    """
    try:
        logger.info(f"💾 RAG processing for: {url}")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        chunks_text = text_splitter.split_text(text)
        
        if not chunks_text:
            logger.warning("❌ RAG: No chunks generated (empty text?)")
            return

        embedding_model = get_embedding_model(task_type="retrieval_document")
        if not embedding_model:
            logger.error("❌ RAG Skip: Embedding model not loaded (Check API key).")
            return

        vectors = embedding_model.embed_documents(chunks_text)
        
        chunks_data = []
        for i, (chunk_txt, vector) in enumerate(zip(chunks_text, vectors)):
            chunks_data.append({
                "text": chunk_txt,
                "embedding": vector,
                "chunk_index": i
            })
        
        meta_summary = summarize_raw_content(text, summarize_type='short')


        doc_data = {
            "url": url,
            "title": f"Scraped from {url}",
            "summary": meta_summary,
            "type": source_type,
            "full_text": text 
        }

        store_document_with_chunks(doc_data, chunks_data)
        logger.info(f"✅ RAG Success: {len(chunks_data)} chunks vectorized and stored.")

    except Exception as e:
        logger.error(f"⚠️ Critical error in input_in_rag: {e}")