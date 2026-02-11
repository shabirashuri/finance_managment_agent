import pdfplumber

def extract_raw_text_from_pdf(file_path: str) -> str:
    """
    Extracts raw text from a PDF.
    No parsing, no structuring, no assumptions.
    """

    full_text = []

    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                full_text.append(
                    f"\n--- Page {page_number} ---\n{text}"
                )
            else:
                full_text.append(
                    f"\n--- Page {page_number} ---\n[NO TEXT FOUND]"
                )

    return "\n".join(full_text)
