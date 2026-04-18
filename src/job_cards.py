from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
import os

OUTPUT_PATH = '../job_cards/'

def generate_job_card(order):
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    filename = f"{OUTPUT_PATH}order_{order['order_id']}.pdf"

    c = canvas.Canvas(filename, pagesize=LETTER)
    width, height = LETTER

    # Header
    c.setFillColorRGB(0.17, 0.24, 0.31)
    c.rect(0, height - 80, width, 80, fill=True, stroke=False)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(40, height - 50, "PRODUCTION JOB CARD")

    # Order details
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(40, height - 120, f"Order ID:  {order['order_id']}")
    c.drawString(40, height - 150, f"Customer:  {order['customer']}")
    c.drawString(40, height - 180, f"Product:   {order['product']}")
    c.drawString(40, height - 210, f"Quantity:  {order['quantity']}")
    c.drawString(40, height - 240, f"Due Date:  {order['due_date']}")
    c.drawString(40, height - 270, f"Status:    {order['status']}")

    # Divider line
    c.setStrokeColorRGB(0.17, 0.24, 0.31)
    c.setLineWidth(2)
    c.line(40, height - 290, width - 40, height - 290)

    # Notes section
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, height - 320, "Notes:")
    c.setFont("Helvetica", 11)
    c.drawString(40, height - 340, "____________________________________________")
    c.drawString(40, height - 370, "____________________________________________")

    c.save()
    print(f"✅ Job card created: {filename}")

# Run it
from ingest import load_orders

df = load_orders('../data/orders.csv')

# Only generate cards for valid orders
valid_orders = df[~df['is_duplicate'] & ~df['missing_data']]

for _, order in valid_orders.iterrows():
    generate_job_card(order)

print(f"\n✅ Done! {len(valid_orders)} job cards created in the job_cards/ folder.")