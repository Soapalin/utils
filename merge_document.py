from pypdf import PdfMerger
from pypdf import PdfReader
from pypdf import PdfWriter

# pdfs = [ r'C:\Sandbox\Python Learning\log_analysis_tools\result.pdf',r'C:\Users\lucien.tran\Downloads\signed.pdf']

# merger = PdfMerger()

# for pdf in pdfs:
#     merger.append(pdf)

# merger.write("Form959_signed_LT.pdf")
# merger.close()

pdf = r"C:\Sandbox\apply-for-relationship-registration-form3__0.pdf"

reader = PdfReader(pdf)

nb_of_pages = len(reader.pages) -1
# only_pages = reader.pages[5]

writer = PdfWriter()
# for _ in range(nb_of_pages):
#     writer.add_page(reader.pages[_])
    
# writer.write("result.pdf")

writer.add_page(reader.pages[5])
writer.write("stat_declaration.pdf")
