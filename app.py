import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(page_title="AI Doc Generator", page_icon="⚙️", layout="wide")

# --- Streamlit UI ---
st.title("⚙️ AI Documentation Agent (Multi-Language)")
st.markdown("Paste your raw code (Python, C, JavaScript, etc.) below to generate Markdown docs.")

# Layout with two columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Source Code")
    user_code = st.text_area("Paste code here:", height=400, placeholder="int main() {\n  return 0;\n}")
    generate_btn = st.button("Generate Docs ✨", type="primary")

with col2:
    st.subheader("Generated Documentation")
    
    if generate_btn:
        if not user_code.strip():
            st.warning("Please enter some code to document.")
        else:
            with st.spinner("Analyzing code structure and generating docs..."):
                try:
                    # Grab the API key securely from Streamlit secrets
                    api_key = st.secrets["GEMINI_API_KEY"]
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    # Send the raw code directly to the AI
                    prompt = f"""
                    You are an expert technical writer. Analyze the following source code and generate clean, professional API documentation in Markdown.
                    - Identify the programming language automatically.
                    - Document all classes, structs, functions, and methods.
                    - Use Markdown tables for arguments and return types if appropriate.
                    - Do NOT include the original code block in the output.
                    
                    Raw Code:
                    {user_code}
                    """
                    
                    response = model.generate_content(prompt)
                    
                    # Stamp the date using the strict dd/mm/yyyy format
                    current_date = datetime.now().strftime("%d/%m/%Y")
                    final_output = f"> **Generated on:** {current_date}\n\n" + response.text
                    
                    # Display the result
                    st.markdown(final_output)
                    
                    # Add a download button for the Markdown file
                    st.download_button(
                        label="Download .md File",
                        data=final_output,
                        file_name="API_DOCUMENTATION.md",
                        mime="text/markdown"
                    )
                except KeyError:
                    st.error("API Key not found. Please ensure GEMINI_API_KEY is set in Streamlit Secrets.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
