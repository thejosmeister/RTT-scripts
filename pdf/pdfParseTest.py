from pdfminer.high_level import extract_text

text = extract_text('wg 2013.pdf', page_numbers=[10])

print(text)