"""
Code embedding and storage in vector database.
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

def embed_chunks(chunks: List[Dict[str, Any]]) -> Tuple[np.ndarray, List[Dict[str, Any]]]:
    """
    Convert code chunks into embeddings using OpenAI's API.
    
    Args:
        chunks: List of code chunks with 'content' and 'docstring' fields
        
    Returns:
        Tuple of (embeddings array, metadata list)
    """
    embeddings = []
    metadata = []
    
    for i, chunk in enumerate(chunks):
        # Combine content and docstring for better semantic understanding
        text_to_embed = chunk["content"]
        if chunk.get("docstring"):
            text_to_embed = f"{chunk['docstring']}\n\n{text_to_embed}"
        
        # Get embedding from OpenAI
        response = openai.embeddings.create(
            model="text-embedding-3-small",
            input=text_to_embed
        )
        
        # Extract embedding vector
        embedding = response.data[0].embedding
        embeddings.append(embedding)
        
        # Store metadata for retrieval
        chunk_metadata = {
            "id": i,
            "type": chunk.get("type", "unknown"),
            "name": chunk.get("name", "unknown"),
            "file": chunk.get("file", "unknown"),
            "line": chunk.get("line", 0),
            "content": chunk["content"],
            "docstring": chunk.get("docstring", "")
        }
        metadata.append(chunk_metadata)
    
    return np.array(embeddings, dtype=np.float32), metadata

def store_embeddings(embeddings: np.ndarray, metadata: List[Dict[str, Any]], index_path: str = "data/index"):
    """
    Store embeddings and metadata for later retrieval.
    
    Args:
        embeddings: numpy array of embeddings
        metadata: list of metadata dictionaries
        index_path: path to store the index files
    """
    # Create directory if it doesn't exist
    os.makedirs(index_path, exist_ok=True)
    
    # Save metadata
    metadata_path = os.path.join(index_path, "metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f)
    
    # Create and save FAISS index
    index = create_faiss_index(embeddings)
    index_path = os.path.join(index_path, "code_index.faiss")
    faiss.write_index(index, index_path)
    
    print(f"Stored {len(embeddings)} embeddings in {index_path}")
    print(f"Metadata saved to {metadata_path}")

def create_faiss_index(embeddings: np.ndarray) -> faiss.Index:
    """
    Create a FAISS index from embeddings.
    
    Args:
        embeddings: numpy array of embeddings
        
    Returns:
        FAISS index
    """
    # Get embedding dimension
    dimension = embeddings.shape[1]
    
    # Create index
    index = faiss.IndexFlatL2(dimension)
    
    # Add vectors to the index
    index.add(embeddings)
    
    return index

def load_code_chunks(chunks_path: str = "code_chunks.json") -> List[Dict[str, Any]]:
    """
    Load code chunks from a JSON file.
    
    Args:
        chunks_path: path to the JSON file
        
    Returns:
        List of code chunks
    """
    if not os.path.exists(chunks_path):
        raise FileNotFoundError(f"Code chunks file not found: {chunks_path}")
    
    with open(chunks_path, "r") as f:
        chunks = json.load(f)
    
    return chunks

if __name__ == "__main__":
    # Example usage
    try:
        # Load code chunks
        chunks = load_code_chunks()
        print(f"Loaded {len(chunks)} code chunks")
        
        # Create embeddings
        embeddings, metadata = embed_chunks(chunks)
        print(f"Created embeddings with shape: {embeddings.shape}")
        
        # Store embeddings and metadata
        store_embeddings(embeddings, metadata)
        
    except Exception as e:
        print(f"Error: {e}") 