from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib import colors

# ===========================
# 🎨 ART & DESIGN CONFIG
# ===========================
FILE_NAME = "Monthly_Habit_Tracker_Landscape.pdf"

# Colors (Modern & Minimalist)
COLOR_PRIMARY = colors.HexColor("#2C3E50")    # Dark Slate Blue
COLOR_ACCENT = colors.HexColor("#1ABC9C")     # Turquoise / Teal
COLOR_BG_ALT = colors.HexColor("#F7F9F9")     # Very Light Grey
COLOR_GRID = colors.HexColor("#BDC3C7")       # Silver
COLOR_TEXT_MAIN = colors.HexColor("#2C3E50")
COLOR_TEXT_LIGHT = colors.HexColor("#7F8C8D")

HABIT_SECTIONS = {
    "🌅 Morning Routine": ["⏰ Wake Up Early", "🚿 Hygiene (Brush/Bath)", "💧 Morning Hydration", "🧘 Stretch / Meditate"],
    "📚 Study / Work": ["📘 Core Subject Focus", "➕ Math Practice", "✍️ Revision / Notes"],
    "🏋️ Fitness & Health": ["🏃 Workout / Walk", "🍗 Protein Intake", "🥗 Eat Fruits & Veggies", "🚰 Drink 3 Litres Water"],
    "🧠 Skill / Self Growth": ["📖 Clean Reading", "💻 Coding / Skills", "♟️ Chess / Brain Games"],
    "🌙 Night Routine": ["📵 No Phone (Early)", "📝 Day Review & Plan", "😴 Sleep on Time"]
}

# ===========================
# 📐 LAYOUT CONFIG (COMPACT FOR A4)
# ===========================
PAGE_W, PAGE_H = landscape(A4) # 29.7cm x 21cm
MARGIN_X = 1.0 * cm
MARGIN_Y = 1.0 * cm

# Content Area
CONTENT_W = PAGE_W - (2 * MARGIN_X)
CONTENT_H = PAGE_H - (2 * MARGIN_Y)

# Grid Geometry
DAYS = 31
HABIT_COL_WIDTH = 5.5 * cm
DAY_COL_WIDTH = (CONTENT_W - HABIT_COL_WIDTH) / DAYS
ROW_HEIGHT = 0.5 * cm         # Tighter rows to fit everything
SECTION_SPACING = 0.3 * cm    # Space between sections

def draw_border(c):
    """Draws a double decorative border around the page"""
    c.setStrokeColor(COLOR_PRIMARY)
    c.setLineWidth(3)
    c.rect(MARGIN_X - 0.2*cm, MARGIN_Y - 0.2*cm, CONTENT_W + 0.4*cm, CONTENT_H + 0.4*cm)
    
    c.setStrokeColor(COLOR_ACCENT)
    c.setLineWidth(1)
    c.rect(MARGIN_X - 0.4*cm, MARGIN_Y - 0.4*cm, CONTENT_W + 0.8*cm, CONTENT_H + 0.8*cm)

def draw_header(c, y):
    """Draws a compact but stylish header"""
    # Title Background
    c.setFillColor(COLOR_PRIMARY)
    c.roundRect(MARGIN_X, y, CONTENT_W, 1.2*cm, 4, fill=1, stroke=0)
    
    # Title Text
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.white)
    c.drawCentredString(PAGE_W/2, y + 0.4*cm, "MONTHLY HABIT & PRODUCTIVITY TRACKER")
    
    # Month / Name inputs (Floating on right/left just below title)
    y -= 0.8 * cm
    c.setFillColor(COLOR_TEXT_MAIN)
    c.setFont("Helvetica", 10)
    
    # Left: Name
    c.drawString(MARGIN_X, y, "Name: ______________________")
    
    # Right: Month
    c.drawRightString(PAGE_W - MARGIN_X, y, "Month: ______________________")
    
    return y - 0.5 * cm

def draw_grid_header(c, y):
    """Draws the day numbers row"""
    # Header strip bg
    c.setFillColor(COLOR_ACCENT)
    c.rect(MARGIN_X, y, CONTENT_W, ROW_HEIGHT, fill=1, stroke=0)
    
    # "Habit" Label
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(MARGIN_X + 0.2*cm, y + 0.15*cm, "HABIT / GOAL")
    
    # Day Numbers
    c.setFont("Helvetica", 8)
    for d in range(1, DAYS + 1):
        x_pos = MARGIN_X + HABIT_COL_WIDTH + ((d-1) * DAY_COL_WIDTH)
        # Vertical line for grid
        c.setStrokeColor(colors.white)
        c.setLineWidth(0.5)
        if d > 1:
            c.line(x_pos, y, x_pos, y + ROW_HEIGHT)
        
        c.drawCentredString(x_pos + DAY_COL_WIDTH/2, y + 0.15*cm, str(d))
        
    return y - ROW_HEIGHT

def draw_section(c, y, title, habits):
    """Draws a habit section"""
    # Section Title (Small caps style)
    if y < 2*cm: # Safety check for page break
        pass 
        
    c.setFillColor(COLOR_TEXT_MAIN)
    c.setFont("Helvetica-Bold", 9)
    # Background for section header (Subtle)
    c.setFillColor(colors.HexColor("#EAECEE"))
    c.rect(MARGIN_X, y, CONTENT_W, ROW_HEIGHT, fill=1, stroke=0)
    c.setFillColor(COLOR_TEXT_MAIN)
    c.drawString(MARGIN_X + 0.2*cm, y + 0.15*cm, title.upper())
    
    y -= ROW_HEIGHT
    
    # Draw Habits
    c.setFont("Helvetica", 8)
    c.setLineWidth(0.5)
    
    for i, habit in enumerate(habits):
        # Alternating row color
        if i % 2 == 0:
            c.setFillColor(colors.white)
        else:
            c.setFillColor(COLOR_BG_ALT)
        c.rect(MARGIN_X, y, CONTENT_W, ROW_HEIGHT, fill=1, stroke=0)
        
        # Habit Name
        c.setFillColor(colors.black)
        c.drawString(MARGIN_X + 0.2*cm, y + 0.15*cm, habit)
        
        # Vertical Grid Lines
        c.setStrokeColor(COLOR_GRID)
        for d in range(DAYS + 1):
            x_pos = MARGIN_X + HABIT_COL_WIDTH + (d * DAY_COL_WIDTH)
            c.line(x_pos, y, x_pos, y + ROW_HEIGHT)
            
        y -= ROW_HEIGHT
        
    return y 

def draw_footer(c, y):
    """Draws summary boxes at the bottom"""
    # Make sure we have enough space, or adjust y
    # Footer area height approx 2.5cm
    
    footer_start_y = MARGIN_Y # Bottom margin
    
    # Separator Line
    c.setStrokeColor(COLOR_ACCENT)
    c.setLineWidth(1.5)
    c.line(MARGIN_X, y, PAGE_W - MARGIN_X, y)
    
    y -= 0.3 * cm
    
    # Three Blocks: Quote/Stats | Win | Improve
    
    box_w = (CONTENT_W - 1*cm) / 3
    box_h = 2.0 * cm
    
    # Helper to draw a fancy box
    def draw_review_box(x, title, subtitle):
        c.setStrokeColor(COLOR_GRID)
        c.setLineWidth(1)
        c.roundRect(x, y - box_h, box_w, box_h, 4, stroke=1, fill=0)
        
        # Header for box
        c.setFillColor(COLOR_PRIMARY)
        c.roundRect(x, y - 0.5*cm, box_w, 0.5*cm, 4, fill=1, stroke=0) # Top strip
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(x + box_w/2, y - 0.35*cm, title)
        
        # Content placeholder
        c.setFillColor(COLOR_TEXT_LIGHT)
        c.setFont("Helvetica-Oblique", 8)
        c.drawCentredString(x + box_w/2, y - 1.2*cm, subtitle)
        # Line for writing
        c.setStrokeColor(COLOR_GRID)
        c.line(x + 0.5*cm, y - 1.5*cm, x + box_w - 0.5*cm, y - 1.5*cm)

    draw_review_box(MARGIN_X, "💡 MOTIVATION", "Paste a sticker or write a quote")
    draw_review_box(MARGIN_X + box_w + 0.5*cm, "🏆 BIGGEST WIN", "What went well?")
    draw_review_box(MARGIN_X + 2*box_w + 1.0*cm, "📈 TO IMPROVE", "Focus for next month")

def create_beautiful_tracker():
    c = canvas.Canvas(FILE_NAME, pagesize=landscape(A4))
    
    draw_border(c)
    
    # Top starting position
    current_y = PAGE_H - MARGIN_Y - 1.2*cm # Account for border padding
    
    current_y = draw_header(c, current_y)
    current_y -= 0.2 * cm # Spacing
    
    current_y = draw_grid_header(c, current_y)
    
    for section_name, habits in HABIT_SECTIONS.items():
        current_y = draw_section(c, current_y, section_name, habits)
    
    # Footer
    # Check if we have space, otherwise push slightly
    if current_y < MARGIN_Y + 2.5*cm:
        print("Warning: Content might be tight!")
        
    draw_footer(c, current_y - 0.5*cm)
    
    c.showPage()
    c.save()
    print(f"✨ Artistic PDF Generated: {FILE_NAME}")

if __name__ == "__main__":
    create_beautiful_tracker()
