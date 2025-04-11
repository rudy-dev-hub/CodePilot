"""
GPT integration for code understanding and responses.
"""

import os
import openai
from dotenv import load_dotenv
from typing import Dict, Any, Optional
import sys
import json

# Add the parent directory to the path so we can import from scripts
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.retriever import get_context_for_query

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def format_prompt(query: str, context: str) -> str:
    """
    Format the prompt for GPT with the query and context.
    
    Args:
        query: User's question
        context: Retrieved code context
        
    Returns:
        Formatted prompt string
    """
    prompt = f"""You are an AI coding assistant. Answer the following question about the codebase based on the provided context.

Context:
{context}

Question: {query}

Please provide a clear, concise, and helpful answer. If the context doesn't contain enough information to answer the question, say so and suggest what additional information might be needed.
"""
    return prompt

def get_gpt_response(prompt: str, model: str = "gpt-4") -> str:
    """
    Get a response from GPT.
    
    Args:
        prompt: Formatted prompt string
        model: GPT model to use
        
    Returns:
        GPT's response
    """
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an AI coding assistant that helps users understand codebases."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error getting response from GPT: {str(e)}"

def process_query(query: str, top_k: int = 5, model: str = "gpt-4") -> Dict[str, Any]:
    """
    Process a user query by retrieving context and getting a GPT response.
    
    Args:
        query: User's question
        top_k: Number of similar chunks to retrieve
        model: GPT model to use
        
    Returns:
        Dictionary with query, context, and response
    """
    # Get context from retriever
    context = get_context_for_query(query, top_k)
    
    # Format prompt
    prompt = format_prompt(query, context)
    
    # Get response from GPT
    response = get_gpt_response(prompt, model)
    
    # Return results
    return {
        "query": query,
        "context": context,
        "response": response
    }

if __name__ == "__main__":
    # Example usage
    try:
        query = "How does the Calculator class work?"
        print(f"Processing query: {query}")
        
        result = process_query(query)
        
        print("\nResponse:")
        print(result["response"])
        
    except Exception as e:
        print(f"Error: {e}") 