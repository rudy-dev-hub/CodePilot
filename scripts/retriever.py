"""
Retrieves relevant code chunks from the vector database.
"""

import os
import json
import numpy as np
import faiss
from typing import List, Dict, Any, Tuple
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def load_index_and_metadata(index_path: str = "data/index") -> Tuple[faiss.Index, List[Dict[str, Any]]]:
    """
    Load the FAISS index and metadata from disk.
    
    Args:
        index_path: Path to the directory containing the index and metadata
        
    Returns:
        Tuple of (FAISS index, metadata list)
    """
    # Load FAISS index
    index_file = os.path.join(index_path, "code_index.faiss")
    if not os.path.exists(index_file):
        raise FileNotFoundError(f"FAISS index not found: {index_file}")
    
    index = faiss.read_index(index_file)
    
    # Load metadata
    metadata_file = os.path.join(index_path, "metadata.json")
    if not os.path.exists(metadata_file):
        raise FileNotFoundError(f"Metadata file not found: {metadata_file}")
    
    with open(metadata_file, "r") as f:
        metadata = json.load(f)
    
    return index, metadata

def embed_query(query: str) -> np.ndarray:
    """
    Embed a user query using the same model as the code chunks.
    
    Args:
        query: User's question
        
    Returns:
        Embedding vector as numpy array
    """
    # Get embedding from OpenAI
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    
    # Extract embedding vector and convert to numpy array
    embedding = np.array(response.data[0].embedding, dtype=np.float32)
    
    return embedding

def search_similar_chunks(query: str, top_k: int = 5, index_path: str = "data/index") -> List[Dict[str, Any]]:
    """
    Search for code chunks similar to the query.
    
    Args:
        query: User's question
        top_k: Number of similar chunks to retrieve
        index_path: Path to the directory containing the index and metadata
        
    Returns:
        List of relevant code chunks with metadata
    """
    # Load index and metadata
    index, metadata = load_index_and_metadata(index_path)
    
    # Embed the query
    query_embedding = embed_query(query)
    
    # Reshape for FAISS (needs to be 2D)
    query_embedding = query_embedding.reshape(1, -1)
    
    # Search for similar vectors
    distances, indices = index.search(query_embedding, top_k)
    
    # Get the relevant chunks
    relevant_chunks = []
    for i, idx in enumerate(indices[0]):
        if idx < len(metadata):  # Ensure index is valid
            chunk = metadata[idx]
            chunk["distance"] = float(distances[0][i])  # Add distance score
            relevant_chunks.append(chunk)
    
    return relevant_chunks

def get_context_for_query(query: str, top_k: int = 5) -> str:
    """
    Get formatted context from relevant code chunks for a query.
    
    Args:
        query: User's question
        top_k: Number of similar chunks to retrieve
        
    Returns:
        Formatted context string
    """
    chunks = search_similar_chunks(query, top_k)
    return format_retrieved_chunks(chunks)

def format_retrieved_chunks(chunks: List[Dict[str, Any]]) -> str:
    """
    Format retrieved chunks into a readable context string.
    
    Args:
        chunks: List of code chunks with metadata
        
    Returns:
        Formatted context string
    """
    if not chunks:
        return "No relevant code chunks found."
    
    context = "Here are the relevant code snippets:\n\n"
    
    for i, chunk in enumerate(chunks):
        context += f"--- Chunk {i+1} ---\n"
        context += f"File: {chunk.get('file', 'unknown')}\n"
        context += f"Type: {chunk.get('type', 'unknown')}\n"
        context += f"Name: {chunk.get('name', 'unknown')}\n"
        
        if chunk.get("docstring"):
            context += f"Docstring: {chunk['docstring']}\n"
        
        context += f"Code:\n{chunk.get('content', '')}\n\n"
    
    return context

if __name__ == "__main__":
    # Example usage
    try:
        query = "How does the Calculator class work?"
        print(f"Query: {query}")
        
        chunks = search_similar_chunks(query)
        print(f"Found {len(chunks)} relevant chunks")
        
        context = format_retrieved_chunks(chunks)
        print("\nContext:")
        print(context)
        
    except Exception as e:
        print(f"Error: {e}") 