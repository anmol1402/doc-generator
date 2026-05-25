import streamlit as st
import ast
from datetime import datetime
import os
from src.ai_enhancer import enhance_documentation # Pulling from your existing file

# --- Page Configuration ---
st.set_page_config(page_title="AI Doc Generator", page_icon="⚙️", layout="wide")

# --- AST Parser Logic ---
class DocExtractor(ast.NodeVisitor):
    def __init__(self):
        self.docs = []
    def visit_FunctionDef(self, node):
        self.docs.append({"type": "Function", "name": node.name, "doc": ast.get_docstring(node) or "None"})
        self.generic_visit(node)
    def visit_ClassDef(self, node):
        self.docs.append({"type": "Class", "name": node.name, "doc": ast.get_docstring(node) or "None"})
        self.generic_visit(node)

# --- Streamlit UI ---
st.title("⚙️ AI Documentation Agent")
st.markdown("Paste your raw Python code below and watch the AI synthesize professional Markdown documentation.")

# Layout with two columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Source Code")
    user_code = st.text_area("Paste Python code here:", height=400, placeholder="def my_function():...")
    generate_btn = st.button("Generate Docs ✨", type="primary")

with col2:
    st.subheader("Generated Documentation")
    
    if generate_btn:
        if not user_code.strip():
            st.warning("Please enter some code to document.")
        else:
            with st.spinner("Analyzing code structure and generating docs..."):
                try:
                    # 1. Parse the Code
                    tree = ast.parse(user_code)
                    extractor = DocExtractor()
                    extractor.visit(tree)
                    
                    if not extractor.docs:
                        st.info("No valid Python classes or functions found to document.")
                    else:
                        # 2. Call Gemini API
                        ai_markdown = enhance_documentation(extractor.docs)
                        
                        # 3. Stamp the date using your required format
                        current_date = datetime.now().strftime("%d/%m/%Y")
                        final_output = f"> **Generated on:** {current_date}\n\n" + ai_markdown
                        
                        # Display the result
                        st.markdown(final_output)
                        
                        # Add a download button for the Markdown file
                        st.download_button(
                            label="Download .md File",
                            data=final_output,
                            file_name="API_DOCUMENTATION.md",
                            mime="text/markdown"
                        )
                except SyntaxError:
                    st.error("Syntax Error: The provided text is not valid Python code.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")