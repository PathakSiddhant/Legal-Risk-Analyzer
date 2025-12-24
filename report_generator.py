from fpdf import FPDF
import io

class PDFReport(FPDF):
    def header(self):
        # Logo text
        self.set_font('Arial', 'B', 16)
        self.set_text_color(50, 50, 200) # Professional Blue
        self.cell(0, 10, 'LexiSafe AI - Risk Assessment Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf_report(filename, risks):
    """
    Generates a professional PDF report from the risks dictionary.
    """
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # --- TITLE SECTION ---
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0)
    pdf.cell(0, 10, f"Contract Analyzed: {filename}", 0, 1)
    pdf.ln(5)
    
    # --- SUMMARY METRICS ---
    h, m, l = len(risks['High']), len(risks['Medium']), len(risks['Low'])
    
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 10, f"Summary: {h} Critical Risks, {m} Warnings, {l} Safe Clauses", 0, 1)
    pdf.ln(5)
    
    # --- RISK DETAILS FUNCTION ---
    def add_section(title, items, color_r, color_g, color_b):
        if not items: return
        
        # Section Header
        pdf.set_font("Arial", 'B', 12)
        pdf.set_text_color(color_r, color_g, color_b)
        pdf.cell(0, 10, title.upper(), 0, 1)
        pdf.set_text_color(0) # Reset to black
        
        # Items
        pdf.set_font("Arial", '', 10)
        for item in items:
            # Clause Title
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(0, 8, f"- {item['title']}", 0, 1)
            
            # Explanation
            pdf.set_font("Arial", '', 10)
            pdf.multi_cell(0, 5, f"Analysis: {item['expl']}")
            
            # Recommendation
            pdf.set_font("Arial", 'I', 9)
            pdf.set_text_color(80, 80, 80) # Grey
            pdf.multi_cell(0, 5, f"Recommendation: {item['fix']}")
            
            pdf.ln(3) # Space between items
            pdf.set_text_color(0) # Reset
        
        pdf.ln(5) # Space between sections

    # --- ADD SECTIONS ---
    add_section("Critical Risks (High Priority)", risks['High'], 255, 75, 75)   # Red
    add_section("Warnings (Medium Priority)", risks['Medium'], 255, 165, 0)     # Orange
    add_section("Safe Clauses", risks['Low'], 0, 180, 100)                      # Green
    
    # --- RETURN BYTES ---
    return pdf.output(dest='S').encode('latin-1')