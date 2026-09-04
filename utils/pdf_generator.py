"""
Generates PDF chalans (fee receipts) and member list reports.
Uses fpdf2 — pure python, no system dependencies, works on Streamlit Cloud.
"""

from fpdf import FPDF
from datetime import date


ORANGE = (240, 149, 90)
PINK = (224, 100, 110)
DARK = (74, 74, 74)


class ChalanPDF(FPDF):
    def __init__(self, gym_name):
        super().__init__()
        self.gym_name = gym_name

    def header(self):
        self.set_fill_color(*ORANGE)
        self.rect(0, 0, 210, 25, "F")
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 18)
        self.set_xy(10, 7)
        self.cell(0, 10, self.gym_name, align="L")
        self.set_font("Helvetica", "", 11)
        self.set_xy(10, 16)
        self.cell(0, 6, "Fee Chalan / Receipt", align="L")
        self.ln(20)


def generate_chalan_pdf(gym_name: str, fee_row) -> bytes:
    """fee_row is the SQLAlchemy row from get_fee_by_chalan (has fee + member fields)."""
    pdf = ChalanPDF(gym_name)
    pdf.add_page()
    pdf.set_text_color(*DARK)
    pdf.set_font("Helvetica", "", 11)
    pdf.ln(5)

    def row(label, value):
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(50, 8, label)
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 8, str(value))
        pdf.ln(8)

    row("Chalan No:", fee_row.chalan_no)
    row("Date:", str(fee_row.paid_date))
    row("Member Name:", fee_row.full_name)
    row("Phone:", fee_row.phone or "-")
    row("Membership Type:", fee_row.membership_type or "-")
    row("Fee For:", f"{fee_row.month} {fee_row.year}")
    row("Payment Method:", fee_row.payment_method)
    row("Status:", fee_row.status)

    pdf.ln(4)
    pdf.set_draw_color(*ORANGE)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)

    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*PINK)
    pdf.cell(0, 10, f"Total Paid: Rs. {float(fee_row.amount):,.2f}")
    pdf.ln(15)

    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 6, f"Generated on {date.today()} — Thank you for training with us!")

    return bytes(pdf.output())


def generate_members_report_pdf(gym_name: str, df) -> bytes:
    pdf = ChalanPDF(gym_name)
    pdf.add_page()
    pdf.set_text_color(*DARK)
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Members Report")
    pdf.ln(10)

    col_widths = [10, 45, 30, 30, 30, 25]
    headers = ["ID", "Name", "Phone", "Type", "Slot", "Status"]

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(*ORANGE)
    pdf.set_text_color(255, 255, 255)
    for w, h in zip(col_widths, headers):
        pdf.cell(w, 8, h, border=1, fill=True, align="C")
    pdf.ln()

    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*DARK)
    for _, r in df.iterrows():
        values = [str(r["id"]), str(r["full_name"])[:25], str(r["phone"] or "-"),
                   str(r["membership_type"]), str(r["time_slot"]), str(r["status"])]
        for w, v in zip(col_widths, values):
            pdf.cell(w, 7, v, border=1)
        pdf.ln()

    return bytes(pdf.output())


def generate_fee_history_pdf(gym_name: str, df) -> bytes:
    pdf = ChalanPDF(gym_name)
    pdf.add_page()
    pdf.set_text_color(*DARK)
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Fee / Chalan History Report")
    pdf.ln(10)

    col_widths = [28, 40, 25, 30, 25, 20]
    headers = ["Chalan No", "Member", "Amount", "Month/Year", "Method", "Status"]

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(*ORANGE)
    pdf.set_text_color(255, 255, 255)
    for w, h in zip(col_widths, headers):
        pdf.cell(w, 8, h, border=1, fill=True, align="C")
    pdf.ln()

    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*DARK)
    for _, r in df.iterrows():
        values = [str(r["chalan_no"]), str(r["full_name"])[:22], f"Rs.{float(r['amount']):,.0f}",
                   f"{r['month']} {r['year']}", str(r["payment_method"]), str(r["status"])]
        for w, v in zip(col_widths, values):
            pdf.cell(w, 7, v, border=1)
        pdf.ln()

    return bytes(pdf.output())
