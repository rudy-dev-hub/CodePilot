# AI Dev Copilot

An intelligent code assistant that helps you understand and navigate your codebase using natural language queries.

## Features

- Intelligent code parsing and chunking
- Semantic search using FAISS vector database
- Natural language querying of codebase
- Streamlit-based user interface
- GPT-powered code understanding and responses

## Demo

The `demo/` folder contains screenshots and examples of the AI Dev Copilot in action. You can see:

- The Streamlit interface
- Example queries and responses
- How the system retrieves relevant code chunks
- The quality of GPT-generated answers

To see the demo in action, you can run the application locally following the setup instructions below.

## Setup

### Option 1: Using Setup Scripts (Recommended)

#### For macOS/Linux:
```bash
# Make the setup script executable
chmod +x setup.sh

# Run the setup script
./setup.sh
```

#### For Windows:
```bash
# Run the setup batch file
setup.bat
```

### Option 2: Manual Setup

1. Create a virtual environment:
   ```bash
   # For macOS/Linux
   python -m venv venv
   source venv/bin/activate

   # For Windows
   python -m venv venv
   venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

4. Create necessary directories:
   ```bash
   mkdir -p data/index
   mkdir -p test_codebase
   ```

## Running the Application

1. Activate the virtual environment (if not already activated):
   ```bash
   # For macOS/Linux
   source venv/bin/activate

   # For Windows
   venv\Scripts\activate
   ```

2. Create the FAISS index (first time only):
   ```bash
   python create_index.py
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run ui/streamlit_app.py
   ```

## Project Structure

- `data/index/`: Vector database files for semantic search
- `scripts/`: Core functionality for parsing, chunking, and retrieving code
- `gpt/`: GPT integration for code understanding
- `ui/`: Streamlit-based user interface
- `test_codebase/`: Sample code for testing
- `demo/`: Screenshots and examples of the application in action

## Usage

1. Start the Streamlit app
2. Enter your code-related question in natural language
3. Get intelligent responses based on your codebase context

## License

MIT

---

Made by Rudresh Upadhyaya ❤️

