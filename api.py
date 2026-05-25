# api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ast
from datetime import datetime
from src.ai_enhancer import enhance_documentation # Pulls from our existing AI script

app = FastAPI()

# This allows your HTML frontend to communicate with this Python backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define what data the frontend will send us
class CodeInput(BaseModel):
    code: str

# Adapted parser to read text directly from the frontend
class DocExtractor(ast.NodeVisitor):
    def __init__(self):
        self.docs = []
    def visit_FunctionDef(self, node):
        self.docs.append({"type": "Function", "name": node.name, "doc": ast.get_docstring(node) or "None"})
        self.generic_visit(node)
    def visit_ClassDef(self, node):
        self.docs.append({"type": "Class", "name": node.name, "doc": ast.get_docstring(node) or "None"})
        self.generic_visit(node)

@app.post("/generate")
def generate_api_docs(payload: CodeInput):
    try:
        # 1. Parse the incoming code from the frontend
        tree = ast.parse(payload.code)
        extractor = DocExtractor()
        extractor.visit(tree)
        
        if not extractor.docs:
            return {"result": "No valid Python classes or functions found to document."}

        # 2. Send the extracted metadata to Gemini
        ai_markdown = enhance_documentation(extractor.docs)
        
        # 3. Stamp the generation date
        current_date = datetime.now().strftime("%d/%m/%Y")
        final_output = f"> **Generated on:** {current_date}\n\n" + ai_markdown

        return {"result": final_output}
    except Exception as e:
        return {"result": f"Error processing code: {str(e)}"}