from fastmcp import FastMCP
import os
from pypdf import PdfWriter

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
mcp = FastMCP("Billing-MCP-Server")

# -------------------------------
# Tools
# -------------------------------

@mcp.tool()
def get_customer_data(customer_id: str):
    '''
    Fetch customer details by customer ID.
    
    :param customer_id: Description
    :type customer_id: str
    '''
    return {
        "customer_id": customer_id,
        "name": "ABC Corp",
        "email": "billing@abccorp.com",
        "address": "Mumbai, India",
        "payment_terms": "Net 30"
    }

@mcp.tool()
def get_transactions(customer_id: str):
    '''
    Fetch transaction details for a customer.
    
    :param customer_id: Description
    :type customer_id: str
    '''
    return [
        {"item": "Cloud Services", "amount": 5000, "tax": 900},
        {"item": "Support Plan", "amount": 2000, "tax": 360}
    ]
@mcp.tool()
def generate_invoice_pdf(invoice_data: dict):
    os.makedirs("invoice", exist_ok=True)

    invoice_id = invoice_data.get("invoice_id", "INV-1001")
    file_path = f"invoice/{invoice_id}.pdf"

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    y = height - 50
    customer = invoice_data.get("customer", {})
    customer_id = customer.get("customer_id", "CUST-101")
    name = customer.get("name", "ABC Corp")
    email = customer.get("email", "billing@abccorp.com")
    address = customer.get("address", "Mumbai, India")
    terms = customer.get("payment_terms", "N/A")
    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Billing Invoice")
    y -= 40

    # Customer Info
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Customer: {invoice_data['customer']['name']}")
    c.drawString(300, y, f"Invoice ID: {invoice_id}")
    y -= 20
    c.drawString(50, y, f"Email: {invoice_data['customer']['email']}")
    c.drawString(300, y, f"Date: {invoice_data.get('date', '2024-01-01')}")
    y -= 40

    # Items
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Item")
    c.drawString(300, y, "Amount")
    y -= 20

    total = 0
    c.setFont("Helvetica", 10)

    for item in invoice_data["items"]:
        c.drawString(50, y, item["item"])
        c.drawString(300, y, f"₹{item['amount']} + ₹{item['tax']} tax")
        total += item["amount"] + item["tax"]
        y -= 20

    y -= 20
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, f"Total: ₹{total}")

    c.save()

    return {
        "invoice_id": invoice_id,
        "pdf_path": file_path
    }

@mcp.tool()
def generate_invoice_pdf1(invoice_data: dict):
    '''
    Generate PDF for the given invoice data.
    param invoice_data: Description
    :type invoice_data: dict
    '''
    return {
        "invoice_id": "INV-1001",
        "pdf_url": "https://invoices.company.com/INV-1001.pdf"
    }

@mcp.tool()
def send_invoice(email: str, pdf_url: str):
    '''
    Send the invoice PDF to the customer's email.
    :param email: Description
    :type email: str
    :param pdf_url: Description
    :type pdf_url: str
    '''
    return f"Invoice sent to {email}"

@mcp.tool()
def check_payment_status(invoice_id: str):
    '''
    Check payment status for the given invoice ID.
    :param invoice_id: Description
    :type invoice_id: str
    '''
    return "UNPAID"

@mcp.tool()
def send_reminder(email: str, invoice_id: str):
    '''
    Send payment reminder for the given invoice ID to the customer's email.
    :param email: Description
    :type email: str
    :param invoice_id: Description
    :type invoice_id: str
    '''
    return f"Reminder sent for {invoice_id} to {email}"

@mcp.tool()
def analyze_billing_anomaly(invoice_data: dict):
    '''
    Analyze invoice data for potential anomalies.
    :param invoice_data: Description
    :type invoice_data: dict
    '''
    # Simple mock logic
    if invoice_data.get("total", 0) > 10000:
        return {"anomaly": True, "reason": "Unusually high amount"}
    return {"anomaly": False}

@mcp.tool()
def fetch_invoice_history(customer_id: str):
    '''
    Fetch past invoice history for a customer.
    :param customer_id: Description
    :type customer_id: str
    '''
    return [
        {"invoice_id": "INV-0990", "total": 6500},
        {"invoice_id": "INV-0995", "total": 7000}
    ]

@mcp.tool()
def resolve_dispute(invoice_id: str, resolution: str):
    '''
    Resolve dispute for the given invoice ID.
    :param invoice_id: Description
    :type invoice_id: str
    :param resolution: Description
    :type resolution: str
    '''
    return f"Dispute for {invoice_id} resolved with action: {resolution}"

if __name__ == "__main__":
    mcp.run()