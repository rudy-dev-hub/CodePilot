"""
Code parser for extracting files, classes, and functions from the codebase.
"""

import os
import ast
from typing import Dict, List, Any, Tuple

def parse_codebase(codebase_path):
    """
    Parse the entire codebase and extract files, classes, and functions.
    
    Args:
        codebase_path: Path to the codebase root directory
        
    Returns:
        Dict containing the parsed codebase structure
    """
    if not os.path.exists(codebase_path):
        raise ValueError(f"Codebase path does not exist: {codebase_path}")
    
    result = {
        "files": [],
        "classes": [],
        "functions": [],
        "code_chunks": []
    }
    
    # Extract all files
    files = extract_files(codebase_path)
    result["files"] = files
    
    # For each file, extract classes and functions
    for file_path in files:
        if file_path.endswith('.py'):  # Only process Python files
            classes = extract_classes(file_path)
            functions = extract_functions(file_path)
            
            result["classes"].extend(classes)
            result["functions"].extend(functions)
            
            # Generate code chunks for embeddings
            code_chunks = generate_code_chunks(file_path, classes, functions)
            result["code_chunks"].extend(code_chunks)
    
    return result

def extract_files(directory):
    """
    Extract all files from a directory recursively.
    
    Args:
        directory: Path to the directory
        
    Returns:
        List of file paths
    """
    files = []
    
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            # Skip hidden files and directories
            if filename.startswith('.'):
                continue
                
            # Skip __pycache__ directories
            if '__pycache__' in root:
                continue
                
            file_path = os.path.join(root, filename)
            files.append(file_path)
    
    return files

def get_source_and_docstring(node, source_lines):
    """
    Extract source code and docstring from an AST node.
    
    Args:
        node: AST node
        source_lines: List of source code lines
        
    Returns:
        Tuple of (source_code, docstring)
    """
    # Get the source code for this node
    start_line = node.lineno - 1  # Convert to 0-indexed
    end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line + 1
    
    # Ensure we don't go beyond the source lines
    if end_line > len(source_lines):
        end_line = len(source_lines)
    
    source_code = '\n'.join(source_lines[start_line:end_line])
    
    # Extract docstring
    docstring = ast.get_docstring(node)
    if docstring is None:
        docstring = ""
    
    return source_code, docstring

def extract_classes(file_path):
    """
    Extract classes from a Python file.
    
    Args:
        file_path: Path to the Python file
        
    Returns:
        List of dictionaries containing class information
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            source_lines = content.split('\n')
            
        tree = ast.parse(content)
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                source_code, docstring = get_source_and_docstring(node, source_lines)
                
                class_info = {
                    "name": node.name,
                    "file": file_path,
                    "line": node.lineno,
                    "source_code": source_code,
                    "docstring": docstring,
                    "methods": []
                }
                
                # Extract methods
                for child in node.body:
                    if isinstance(child, ast.FunctionDef):
                        method_source, method_docstring = get_source_and_docstring(child, source_lines)
                        
                        method_info = {
                            "name": child.name,
                            "line": child.lineno,
                            "source_code": method_source,
                            "docstring": method_docstring
                        }
                        class_info["methods"].append(method_info)
                
                classes.append(class_info)
        
        return classes
    except Exception as e:
        print(f"Error parsing file {file_path}: {e}")
        return []

def extract_functions(file_path):
    """
    Extract functions from a Python file.
    
    Args:
        file_path: Path to the Python file
        
    Returns:
        List of dictionaries containing function information
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            source_lines = content.split('\n')
            
        tree = ast.parse(content)
        functions = []
        
        for node in ast.walk(tree):
            # Only extract top-level functions (not methods inside classes)
            if isinstance(node, ast.FunctionDef) and not isinstance(node.parent, ast.ClassDef):
                source_code, docstring = get_source_and_docstring(node, source_lines)
                
                function_info = {
                    "name": node.name,
                    "file": file_path,
                    "line": node.lineno,
                    "source_code": source_code,
                    "docstring": docstring
                }
                functions.append(function_info)
        
        return functions
    except Exception as e:
        print(f"Error parsing file {file_path}: {e}")
        return []

def generate_code_chunks(file_path, classes, functions):
    """
    Generate code chunks suitable for embeddings.
    
    Args:
        file_path: Path to the Python file
        classes: List of class information
        functions: List of function information
        
    Returns:
        List of code chunks with metadata
    """
    code_chunks = []
    
    # Add classes
    for cls in classes:
        if cls["file"] == file_path:
            chunk = {
                "type": "class",
                "name": cls["name"],
                "file": file_path,
                "line": cls["line"],
                "content": cls["source_code"],
                "docstring": cls["docstring"],
                "metadata": {
                    "num_methods": len(cls["methods"])
                }
            }
            code_chunks.append(chunk)
            
            # Add methods as separate chunks
            for method in cls["methods"]:
                method_chunk = {
                    "type": "method",
                    "name": method["name"],
                    "class": cls["name"],
                    "file": file_path,
                    "line": method["line"],
                    "content": method["source_code"],
                    "docstring": method["docstring"]
                }
                code_chunks.append(method_chunk)
    
    # Add functions
    for func in functions:
        if func["file"] == file_path:
            chunk = {
                "type": "function",
                "name": func["name"],
                "file": file_path,
                "line": func["line"],
                "content": func["source_code"],
                "docstring": func["docstring"]
            }
            code_chunks.append(chunk)
    
    return code_chunks

if __name__ == "__main__":
    # Example usage
    import sys
    import json
    
    if len(sys.argv) > 1:
        codebase_path = sys.argv[1]
    else:
        codebase_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    result = parse_codebase(codebase_path)
    
    # Print summary
    print(f"Found {len(result['files'])} files")
    print(f"Found {len(result['classes'])} classes")
    print(f"Found {len(result['functions'])} functions")
    print(f"Generated {len(result['code_chunks'])} code chunks for embeddings")
    
    # Print detailed information
    print("\nClasses:")
    for cls in result['classes']:
        print(f"  {cls['name']} in {cls['file']} (line {cls['line']})")
        print(f"    Methods: {len(cls['methods'])}")
        print(f"    Docstring: {cls['docstring'][:50]}..." if cls['docstring'] else "    No docstring")
    
    print("\nFunctions:")
    for func in result['functions']:
        print(f"  {func['name']} in {func['file']} (line {func['line']})")
        print(f"    Docstring: {func['docstring'][:50]}..." if func['docstring'] else "    No docstring")
    
    # Save code chunks to a JSON file
    output_file = "code_chunks.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result['code_chunks'], f, indent=2)
    
    print(f"\nCode chunks saved to {output_file}") 