from pypdf import PdfMerger

path = r"C:\Users\lucie\Documents\Partner Visa\3. Social Aspects\Form888\Deenie Adams\drafts"

pdfs = [path + "\888_page1.pdf", path + "\888_page2_signed.pdf"]

merger = PdfMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write("merged.pdf")
merger.close()