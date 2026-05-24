import os
import json
import google.generativeai as genai

def enhance_documentation(raw_docs):
    """Sends raw code metadata to Gemini to generate beautiful Markdown docs."""
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("Warning: GEMINI_API_KEY not found in environment. Generating basic offline documentation...")
        return _generate_basic_markdown(raw_docs)

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')

        prompt = f"""
        You are an expert technical writer and developer. I will provide you with raw extracted metadata 
        from a Python codebase (classes, functions, arguments, file locations, and existing docstrings).
        
        Please generate a clean, professional, and highly readable Markdown documentation file.
        - Group the documentation logically by file or functionality.
        - Use Markdown tables for arguments if appropriate.
        - Add a brief introductory paragraph summarizing what this code seems to do.
        - Do NOT include the JSON raw data in your output.
        
        Raw Data:
        {json.dumps(raw_docs, indent=2)}
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        print(f"Error communicating with Gemini API: {e}")
        print("Falling back to basic offline documentation...")
        return _generate_basic_markdown(raw_docs)

def _generate_basic_markdown(raw_docs):
    """Fallback generator if the API is unavailable or unconfigured."""
    md = "# Project Technical Documentation\n\n"
    for item in raw_docs:
        md += f"## {item['type']}: `{item.get('name', 'Unknown')}`\n"
        if 'file' in item:
            md += f"**File:** `{item['file']}`\n\n"
        if item['type'] == 'Function' and 'args' in item:
            md += f"**Arguments:** {', '.join(item['args']) if item['args'] else 'None'}\n\n"
        md += f"> {item.get('doc', '')}\n\n---\n"
    return md