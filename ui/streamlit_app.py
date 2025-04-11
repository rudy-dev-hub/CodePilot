"""
Streamlit UI for the AI Dev Copilot.
"""

import streamlit as st
import os
import sys
import time
from typing import Dict, Any

# Add the parent directory to the path so we can import from gpt
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gpt.query_engine import process_query

# Set page config
st.set_page_config(
    page_title="AI Dev Copilot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4B8BBE;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #306998;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4B8BBE;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-size: 1rem;
    }
    .stButton>button:hover {
        background-color: #306998;
    }
    .response-box {
        background-color: #f0f2f6;
        border-radius: 5px;
        padding: 1rem;
        margin-top: 1rem;
    }
    .code-block {
        background-color: #282c34;
        color: #abb2bf;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def display_response(response_data: Dict[str, Any]):
    """Display the response from the query engine."""
    # Display the response
    st.markdown("### Answer")
    st.markdown(response_data["response"])
    
    # Display the context in an expander
    with st.expander("View Retrieved Code Context"):
        st.markdown(response_data["context"])

def main():
    # Header
    st.markdown("<h1 class='main-header'>AI Dev Copilot</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Ask questions about your codebase and get intelligent answers</p>", unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## Settings")
        model = st.selectbox(
            "Select GPT Model",
            ["gpt-4", "gpt-3.5-turbo"],
            index=0
        )
        top_k = st.slider(
            "Number of code chunks to retrieve",
            min_value=1,
            max_value=10,
            value=5
        )
        
        st.markdown("---")
        st.markdown("## About")
        st.markdown("""
        AI Dev Copilot helps you understand your codebase by:
        
        - Parsing your code into semantic chunks
        - Creating embeddings for semantic search
        - Retrieving relevant code based on your questions
        - Providing intelligent answers using GPT
        """)
        
        st.markdown("---")
        st.markdown("## Example Questions")
        st.markdown("""
        - How does the Calculator class work?
        - What functions are available in the codebase?
        - Explain the main function in sample.py
        - What parameters does the add function take?
        """)
    
    # Main content
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input("Enter your question about the codebase:", placeholder="e.g., How does the Calculator class work?")
    
    with col2:
        submit_button = st.button("Ask", key="submit_button")
    
    # Process query
    if submit_button:
        if query:
            with st.spinner("Thinking..."):
                # Add a small delay to show the spinner
                time.sleep(0.5)
                
                # Process the query
                response_data = process_query(query, top_k=top_k, model=model)
                
                # Display the response
                display_response(response_data)
        else:
            st.warning("Please enter a question")

if __name__ == "__main__":
    main() 