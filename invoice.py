from fpdf import FPDF

pdf = FPDF()
pdf.add_page()

# Invoice Header
pdf.set_font("Arial", "B", 14)
pdf.cell(0, 10, "Invoice", ln=True, align="C")
pdf.ln(10)

# Customer Details
pdf.set_font("Arial", "", 12)
pdf.cell(0, 10, "Customer Name: John Doe", ln=True)
pdf.cell(0, 10, "Address: 1234 Elm St, Anytown, USA", ln=True)
pdf.ln(10)

# Invoice Table
pdf.set_font("Arial", "B", 12)
pdf.cell(60, 10, "Description", border=1,align="C")
pdf.cell(30, 10, "Qty", border=1)
pdf.cell(30, 10, "Unit Price", border=1)
pdf.cell(30, 10, "Total", border=1)
pdf.ln()

items = [
    ["Widget A", "2", "$15.00", "$30.00"],
    ["Widget B", "3", "$12.00", "$36.00"],
]

pdf.set_font("Arial", "", 12)
for item in items:
    pdf.cell(60, 10, item[0], border=1)
    pdf.cell(30, 10, item[1], border=1)
    pdf.cell(30, 10, item[2], border=1)
    pdf.cell(30, 10, item[3], border=1)
    pdf.ln()

# Total Amount
pdf.set_font("Arial", "B", 12)
pdf.cell(120, 10, "Total", border=1)
pdf.cell(30, 10, "$66.00", border=1)
pdf.output("invoice.pdf")
