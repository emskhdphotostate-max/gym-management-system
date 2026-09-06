"""
Generates PDF chalans (fee receipts) and member list reports.
Uses fpdf2 — pure python, no system dependencies, works on Streamlit Cloud.
"""

from fpdf import FPDF
from datetime import date


# Premium Color Palette
PRIMARY = (99, 102, 241)      # Indigo
SECONDARY = (236, 72, 153)    # Pink
ACCENT = (14, 165, 233)       # Sky Blue
DARK = (15, 23, 42)           # Slate Dark
GRAY = (71, 85, 105)          # Slate Gray
LIGHT_BG = (241, 245, 249)    # Light Gray
SUCCESS = (34, 197, 94)       # Green


def safe_text(value) -> str:
    """fpdf2's default core fonts only support Latin-1. Any character outside that
    (curly quotes, em-dashes, Urdu/Arabic script, emoji, etc.) would crash PDF
    generation. This converts anything unsupported into a safe '?' instead of failing."""
    return str(value).encode("latin-1", "replace").decode("latin-1")


class ChalanPDF(FPDF):
    def __init__(self, gym_name):
        super().__init__()
        self.gym_name = gym_name

    def header(self):
        # Premium gradient-style header with modern design
        # Top accent bar
        self.set_fill_color(*PRIMARY)
        self.rect(0, 0, 210, 4, "F")

        # Main header area
        self.set_fill_color(248, 250, 252)
        self.rect(0, 4, 210, 35, "F")

        # Gym name - large and bold
        self.set_text_color(*DARK)
        self.set_font("Helvetica", "B", 22)
        self.set_xy(15, 12)
        self.cell(0, 8, safe_text(self.gym_name), align="L")

        # Subtitle with modern badge
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*PRIMARY)
        self.set_xy(15, 24)
        self.cell(0, 6, "PAYMENT RECEIPT", align="L")

        # Professional divider line
        self.set_draw_color(*PRIMARY)
        self.set_line_width(0.8)
        self.line(15, 38, 195, 38)

        self.ln(35)


def generate_chalan_pdf(gym_name: str, fee_row) -> bytes:
    """fee_row is the SQLAlchemy row from get_fee_by_chalan (has fee + member fields)."""
    pdf = ChalanPDF(gym_name)
    pdf.add_page()
    pdf.ln(8)

    # Chalan number and date in premium boxes (side by side)
    pdf.set_fill_color(*LIGHT_BG)

    # Left box - Chalan No
    pdf.set_xy(15, pdf.get_y())
    pdf.set_fill_color(241, 245, 249)
    pdf.rect(15, pdf.get_y(), 85, 18, "F")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*GRAY)
    pdf.set_xy(15, pdf.get_y() + 3)
    pdf.cell(85, 5, "RECEIPT NO.", align="L")
    pdf.set_xy(15, pdf.get_y() + 5)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(*DARK)
    pdf.cell(85, 5, safe_text(fee_row.chalan_no), align="L")

    # Right box - Date
    pdf.set_xy(110, pdf.get_y() - 10)
    pdf.set_fill_color(241, 245, 249)
    pdf.rect(110, pdf.get_y(), 85, 18, "F")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*GRAY)
    pdf.set_xy(110, pdf.get_y() + 3)
    pdf.cell(85, 5, "DATE", align="L")
    pdf.set_xy(110, pdf.get_y() + 5)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(*DARK)
    pdf.cell(85, 5, safe_text(fee_row.paid_date), align="L")

    pdf.ln(25)

    # Member details section with modern card design
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*PRIMARY)
    pdf.cell(0, 6, "MEMBER INFORMATION", align="L")
    pdf.ln(8)

    # White card background for member info
    pdf.set_fill_color(255, 255, 255)
    pdf.rect(15, pdf.get_y(), 180, 58, "D")
    pdf.set_draw_color(226, 232, 240)

    y_start = pdf.get_y()

    def info_row(label, value, y_pos):
        pdf.set_xy(20, y_pos)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*GRAY)
        pdf.cell(60, 6, label, align="L")
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*DARK)
        pdf.cell(0, 6, safe_text(value), align="L")

    info_row("Member ID:", fee_row.member_code or "-", y_start + 5)
    info_row("Member Name:", fee_row.full_name, y_start + 13)
    info_row("Phone Number:", fee_row.phone or "-", y_start + 21)
    info_row("Membership Type:", fee_row.membership_type or "-", y_start + 29)
    info_row("Fee Period:", f"{fee_row.month} {fee_row.year}", y_start + 37)
    info_row("Payment Method:", fee_row.payment_method, y_start + 45)

    pdf.ln(66)

    # Payment summary section with highlighted amount box
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*PRIMARY)
    pdf.cell(0, 6, "PAYMENT SUMMARY", align="L")
    pdf.ln(10)

    # Large amount box with gradient-like effect
    pdf.set_fill_color(*PRIMARY)
    pdf.rect(15, pdf.get_y(), 180, 28, "F")

    # Amount display
    pdf.set_xy(15, pdf.get_y() + 5)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(180, 5, "TOTAL AMOUNT PAID", align="C")
    pdf.set_xy(15, pdf.get_y() + 5)
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(180, 8, f"Rs. {float(fee_row.amount):,.2f}", align="C")

    pdf.ln(32)

    # Status badge
    pdf.set_xy(15, pdf.get_y())
    pdf.set_fill_color(*SUCCESS)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(30, 7, f" {safe_text(fee_row.status)} ", align="C", fill=True)

    pdf.ln(20)

    # Footer with thank you message
    pdf.set_draw_color(*LIGHT_BG)
    pdf.set_line_width(0.3)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(8)

    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 5, f"Generated on {date.today()}", align="C")
    pdf.ln(5)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*PRIMARY)
    pdf.cell(0, 5, "Thank you for training with us!", align="C")
    pdf.ln(3)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 5, "This is a computer-generated receipt and does not require a signature.", align="C")

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
        values = [safe_text(r["id"]), safe_text(str(r["full_name"])[:25]), safe_text(r["phone"] or "-"),
                   safe_text(r["membership_type"]), safe_text(r["time_slot"]), safe_text(r["status"])]
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
        values = [safe_text(r["chalan_no"]), safe_text(str(r["full_name"])[:22]), f"Rs.{float(r['amount']):,.0f}",
                   safe_text(f"{r['month']} {r['year']}"), safe_text(r["payment_method"]), safe_text(r["status"])]
        for w, v in zip(col_widths, values):
            pdf.cell(w, 7, v, border=1)
        pdf.ln()

    return bytes(pdf.output())
