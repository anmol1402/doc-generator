import ast

class DocExtractor(ast.NodeVisitor):
    def __init__(self):
        self.docs = []

    def visit_FunctionDef(self, node):
        """Extracts docstrings and arguments from functions."""
        docstring = ast.get_docstring(node) or "No docstring provided."
        args = [arg.arg for arg in node.args.args]
        self.docs.append({
            "type": "Function", 
            "name": node.name, 
            "args": args, 
            "doc": docstring
        })
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        """Extracts docstrings from classes."""
        docstring = ast.get_docstring(node) or "No docstring provided."
        self.docs.append({
            "type": "Class", 
            "name": node.name, 
            "doc": docstring
        })
        self.generic_visit(node)

def parse_file(filepath):
    """Reads a python file and returns its structural metadata."""
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read())
            extractor = DocExtractor()
            extractor.visit(tree)
            return extractor.docs
        except SyntaxError:
            # Skip files with syntax errors
            return []
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return []