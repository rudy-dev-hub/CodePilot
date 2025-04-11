# AI Dev Copilot

An intelligent code assistant that helps you understand and navigate your codebase using natural language queries.

## Features

- Intelligent code parsing and chunking
- Semantic search using FAISS vector database
- Natural language querying of codebase
- Streamlit-based user interface
- GPT-powered code understanding and responses

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
4. Run the Streamlit app:
   ```bash
   streamlit run ui/streamlit_app.py
   ```

## Project Structure

- `data/index/`: Vector database files for semantic search
- `scripts/`: Core functionality for parsing, chunking, and retrieving code
- `gpt/`: GPT integration for code understanding
- `ui/`: Streamlit-based user interface
- `test_codebase/`: Sample code for testing

## Usage

1. Start the Streamlit app
2. Enter your code-related question in natural language
3. Get intelligent responses based on your codebase context

## License

MIT 