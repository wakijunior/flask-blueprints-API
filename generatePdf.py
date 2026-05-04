from fpdf import FPDF
from cloudinaryUpload import upload_pdf
from datetime import datetime


pdf = FPDF()

# def generate_pdf(txt, filename):
#     print('my filename in generate pdf is', filename)
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     pdf.multi_cell(200, 10, txt=txt, align='C')
#     pdf.output(f"reciepts/{filename}.pdf")
    
#     print(f"PDF generated and uploaded successfully as {filename}.pdf")
    
#     upload_pdf(filename)

class ReceiptPDF(FPDF):
    def header(self):
        # Company Name
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "YOUR COMPANY NAME", ln=True, align="C")

        # Subtitle
        self.set_font("Arial", "", 10)
        self.cell(0, 5, "Sales Receipt", ln=True, align="C")
        self.ln(5)


def generate_pdf(data, filename):
    pdf = ReceiptPDF()
    pdf.add_page()

    # Date & Receipt Info
    pdf.set_font("Arial", size=10)
    pdf.cell(100, 5, f"Receipt #: {data['receipt_no']}", ln=0)
    pdf.cell(0, 5, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=1)
    pdf.ln(5)

    # Customer Info
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 6, "Customer Details", ln=True)

    pdf.set_font("Arial", size=10)
    pdf.cell(0, 5, f"Name: {data['customer_name']}", ln=True)
    pdf.cell(0, 5, f"Phone: {data['phone']}", ln=True)
    pdf.ln(5)

    # Table Header
    pdf.set_font("Arial", "B", 11)
    pdf.cell(80, 8, "Item", border=1)
    pdf.cell(30, 8, "Qty", border=1, align="C")
    pdf.cell(40, 8, "Price", border=1, align="C")
    pdf.cell(40, 8, "Total", border=1, align="C")
    pdf.ln()

    # Table Content
    pdf.set_font("Arial", size=10)
    total_amount = 0

    for item in data["items"]:
        total = item["qty"] * item["price"]
        total_amount += total

        pdf.cell(80, 8, item["name"], border=1)
        pdf.cell(30, 8, str(item["qty"]), border=1, align="C")
        pdf.cell(40, 8, f"{item['price']:.2f}", border=1, align="R")
        pdf.cell(40, 8, f"{total:.2f}", border=1, align="R")
        pdf.ln()

    # Total Section
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(150, 8, "Total", border=0)
    pdf.cell(40, 8, f"{total_amount:.2f}", border=1, align="R")
    pdf.ln(10)

    # Footer Message
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 5, "Thank you for your business!", ln=True, align="C")

    # Save file
    pdf.output(f"reciepts/{filename}.pdf")

    print(f"PDF generated successfully as {filename}.pdf")

    upload_pdf(filename)