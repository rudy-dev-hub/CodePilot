#!/usr/bin/env python
"""
Script to create the FAISS index from code chunks.
"""

import os
import sys

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the embedder module
from scripts.embedder import load_code_chunks, embed_chunks, store_embeddings

def main():
    """Create the FAISS index from code chunks."""
    print("Creating FAISS index from code chunks...")
    
    # Create the data/index directory if it doesn't exist
    os.makedirs("data/index", exist_ok=True)
    
    # Load code chunks
    chunks = load_code_chunks()
    print(f"Loaded {len(chunks)} code chunks")
    
    # Create embeddings
    embeddings, metadata = embed_chunks(chunks)
    print(f"Created embeddings with shape: {embeddings.shape}")
    
    # Store embeddings and metadata
    store_embeddings(embeddings, metadata)
    print("FAISS index created successfully!")

if __name__ == "__main__":
    main() 