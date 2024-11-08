from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Monthly Sales Report", ln=True, align="C")
pdf.ln(10)

# Adding a table
pdf.set_font("Arial", "B", 12)
columns = ["Product", "Units Sold", "Total Revenue"]
for col in columns:
    pdf.cell(60, 10, col, border=1, align="C")
pdf.ln()

data = [
    ["Product A", "100", "$500"],
    ["Product B", "150", "$750"],
    ["Product C", "120", "$600"]
]

pdf.set_font("Arial", "", 12)
for row in data:
    for item in row:
        pdf.cell(60, 10, item, border=1, align="C")
    pdf.ln()

pdf.output("sales_report.pdf")
