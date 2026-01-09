import os
from pypdf import PdfReader

def pdf_to_markdown(pdf_path, output_path):
    print(f"Processing {pdf_path}...")
    try:
        reader = PdfReader(pdf_path)
        text_content = []
        
        # Meta Info
        text_content.append(f"# Extracted Content: {os.path.basename(pdf_path)}\n")
        text_content.append(f"**Total Pages**: {len(reader.pages)}\n\n")

        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text_content.append(f"## Page {i+1}\n")
                text_content.append(page_text)
                text_content.append("\n---\n")
            else:
                text_content.append(f"## Page {i+1}\n")
                text_content.append("*[No text extracted - likely image/scan]*\n")
                text_content.append("\n---\n")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(text_content))
        
        print(f"Saved to {output_path}")

    except Exception as e:
        print(f"Failed to process {pdf_path}: {e}")

if __name__ == "__main__":
    files_to_process = [
        ("1158 Arch Set (1).pdf", "1158_Arch_Set.md"),
        ("PE fire-alarm workflow.pdf", "PE_Workflow.md"),
        # NFPA 72 is likely too large for a full dump, but we'll try or maybe skip if it takes too long.
        # User asked for it, so we include it.
        ("NFPA 72-19-PDF (1).pdf", "NFPA_72_Extracted.md")
    ]

    for pdf, md in files_to_process:
        if os.path.exists(pdf):
            pdf_to_markdown(pdf, md)
        else:
            print(f"File not found: {pdf}")
