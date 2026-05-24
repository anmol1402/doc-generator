import os
import argparse
from src.parser import parse_file
from src.ai_enhancer import enhance_documentation
from dotenv import load_dotenv

# Load local environment variables from a .env file if it exists (for local testing)
load_dotenv()

def main():
    # Setup command line arguments
    parser = argparse.ArgumentParser(description="AI-Powered Documentation Generator")
    parser.add_argument("--target", default=".", help="Target directory to document (default: current directory)")
    parser.add_argument("--output", default="API_DOCUMENTATION.md", help="Output Markdown file path")
    args = parser.parse_args()

    all_docs = []
    print(f"[*] Scanning directory: {args.target}")
    
    # Traverse the directory
    for root, _, files in os.walk(args.target):
        # Ignore common hidden directories and virtual environments
        if any(ignored in root for ignored in ['.git', '__pycache__', 'venv', 'env', '.github']):
            continue
            
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                print(f"   -> Parsing {filepath}...")
                
                file_docs = parse_file(filepath)
                if file_docs:
                    # Inject the file path into the metadata so the AI knows where it came from
                    for doc in file_docs:
                        doc['file'] = filepath
                    all_docs.extend(file_docs)

    if not all_docs:
        print("[!] No valid Python classes or functions found to document.")
        return

    print("\n[*] Structuring and enhancing documentation with AI...")
    final_markdown = enhance_documentation(all_docs)

    # Write the output to a file
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(final_markdown)
        
    print(f"\n[+] Success! Documentation generated at: {args.output}")

if __name__ == "__main__":
    main()