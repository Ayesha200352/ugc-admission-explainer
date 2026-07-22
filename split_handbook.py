from pypdf import PdfReader, PdfWriter

def extract_pages(input_pdf, output_pdf, start_page, end_page):
    """
    Extracts pages [start_page, end_page] (inclusive, 1-indexed)
    from input_pdf and saves them as output_pdf.
    """
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for page_num in range(start_page - 1, end_page):  # convert to 0-indexed
        writer.add_page(reader.pages[page_num])

    with open(output_pdf, "wb") as f:
        writer.write(f)

    print(f"Saved pages {start_page}-{end_page} to {output_pdf}")


if __name__ == "__main__":
    handbook = "data/handbooks/handbook_2024_2025.pdf"
    extract_pages(handbook, "data/policy_notices/section1_admissions_policy.pdf", 15, 22)
    extract_pages(handbook, "data/faculty_sections/arts_stream.pdf", 39, 50)

    # Verified against the actual PDF's table of contents and page content.
    extract_pages(handbook, "data/faculty_sections/management.pdf", 51, 56)
    extract_pages(handbook, "data/faculty_sections/bio_science.pdf", 58, 75)
    extract_pages(handbook, "data/faculty_sections/engineering.pdf", 76, 84)

    # Bonus: Section 9 of the handbook already contains the previous
    # year's Z-score cut-off marks.
    extract_pages(handbook, "data/zscore_reports/zscore_cutoffs_2024_2025_handbook.pdf", 196, 205)