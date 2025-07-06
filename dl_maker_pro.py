import tkinter as tk
from tkinter import messagebox
from pdf417 import encode, render_image
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from PIL import Image
from io import BytesIO
import datetime

# === GUI Window Setup ===
window = tk.Tk()
window.title("DL Maker Pro")
window.geometry("500x900")

# === DL Fields ===
fields = {
    "First Name": tk.StringVar(),
    "Middle Name": tk.StringVar(),
    "Last Name": tk.StringVar(),
    "Date of Birth (YYYYMMDD)": tk.StringVar(),
    "DL Number": tk.StringVar(),
    "Class": tk.StringVar(),
    "Gender (1=Male, 2=Female)": tk.StringVar(),
    "Eye Color": tk.StringVar(),
    "Height (cm)": tk.StringVar(),
    "Weight (lbs)": tk.StringVar(),
    "Address": tk.StringVar(),
    "City": tk.StringVar(),
    "State": tk.StringVar(),
    "ZIP Code": tk.StringVar(),
    "Issue Date (YYYYMMDD)": tk.StringVar(),
    "Expiration Date (YYYYMMDD)": tk.StringVar(),
    "Original Issue Date": tk.StringVar(),
    "Document Discriminator": tk.StringVar(),
    "Audit Info": tk.StringVar(),
    "Inventory Control No": tk.StringVar(),
    "Production Date": tk.StringVar(),
    "Country": tk.StringVar()
}

# === Form Layout ===
row = 0
for label, var in fields.items():
    tk.Label(window, text=label).grid(row=row, column=0, padx=10, pady=4, sticky="w")
    tk.Entry(window, textvariable=var, width=35).grid(row=row, column=1, padx=10)
    row += 1

# === Barcode Generator Function ===
def generate_barcode():
    try:
        values = {label: var.get().upper() for label, var in fields.items()}
        first = values["First Name"].replace(" ", "_")
        last = values["Last Name"].replace(" ", "_")
        today = datetime.datetime.now().strftime("%Y%m%d")
        pdf_filename = f"{first}{last}_DL{today}.pdf"

        barcode_data = f"""
@
ANSI 636026080102DL00410288ZA03290015DLDAQ{values['DL Number']}
DCS{values['Last Name']}
DAC{values['First Name']}
DAD{values['Middle Name']}
DBD{values['Issue Date (YYYYMMDD)']}
DBB{values['Date of Birth (YYYYMMDD)']}
DBA{values['Expiration Date (YYYYMMDD)']}
DDD{values['Original Issue Date']}
DBC{values['Gender (1=Male, 2=Female)']}
DAU{values['Height (cm)']}
DAZ{values['Weight (lbs)']} lb
DAY{values['Eye Color']}
DAG{values['Address']}
DAI{values['City']}
DAJ{values['State']}
DAK{values['ZIP Code']}
DCF{values['Document Discriminator']}
DCG{values['Country']}
DCHClass {values['Class']}
DCLNONE
DCI{values['State']}
DCJ{values['Audit Info']}
DCK{values['Inventory Control No']}
DDB{values['Production Date']}
DDC{values['State']}
"""

        codes = encode(barcode_data.strip(), columns=6, security_level=5)
        img = render_image(codes, scale=3, ratio=3, padding=10)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        image = ImageReader(buffer)

        c = canvas.Canvas(pdf_filename, pagesize=letter)
        c.drawString(72, 760, "Driver's License Barcode")
        c.drawImage(image, 72, 720, width=76 * mm, height=25 * mm)
        c.save()

        messagebox.showinfo("✅ Success", f"Saved PDF:\n{pdf_filename}")
    except Exception as e:
        messagebox.showerror("❌ Error", f"{e}")

tk.Button(window, text="Generate Barcode", command=generate_barcode,
          bg="green", fg="white", height=2, width=40).grid(row=row, columnspan=2, pady=20)

window.mainloop()
