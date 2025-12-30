from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.colors import black, HexColor

file_path = "Monthly_Habit_Tracker_Landscape.pdf"

c = canvas.Canvas(file_path, pagesize=landscape(A4))
width, height = landscape(A4)

# Title
c.setFont("Helvetica-Bold", 20)
c.drawCentredString(width/2, height-1.5*cm, "MONTHLY HABIT & PRODUCTIVITY TRACKER")

# Subtitle
c.setFont("Helvetica", 11)
c.drawString(1.5*cm, height-2.7*cm, "Name: ____________________________")
c.drawString(width/2, height-2.7*cm, "Month: ____________________________")

y = height - 4*cm

def draw_section(title):
    global y
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1.5*cm, y, title)
    y -= 0.8*cm

def draw_habits(habits):
    global y
    c.setFont("Helvetica", 9)
    x_start = 1.5*cm
    box = 0.5*cm
    
    # Days row
    c.drawString(x_start, y, "Habit")
    for d in range(1, 32):
        c.drawString(x_start + 3*cm + (d-1)*box, y, str(d))
    y -= 0.6*cm
    
    for h in habits:
        c.drawString(x_start, y, h)
        for d in range(31):
            c.rect(x_start + 3*cm + d*box, y-0.2*cm, box, box)
        y -= 0.6*cm
    y -= 0.4*cm

# Sections
draw_section("🌅 Morning Routine")
draw_habits(["⏰ Wake up early", "🚿 Hygiene", "💧 Drink water", "🧘 Stretch / Meditation"])

draw_section("📚 Study / Work")
draw_habits(["📘 Core subject", "➕ Math practice", "✍️ Revision / Notes"])

draw_section("🏋️ Fitness & Health")
draw_habits(["🏃 Workout / Walk", "🍗 Protein intake", "🥗 Fruits & Veggies", "🚰 3L Water"])

draw_section("🧠 Skill / Self Growth")
draw_habits(["📖 Reading", "💻 Coding / Skill", "♟️ Chess / Brain game"])

draw_section("🌙 Night Routine")
draw_habits(["📵 Phone off early", "📝 Day review", "😴 Sleep on time"])

# Monthly Review
c.setFont("Helvetica-Bold", 14)
c.drawString(1.5*cm, y, "⭐ Monthly Review")
y -= 1*cm

c.setFont("Helvetica", 10)
c.drawString(1.5*cm, y, "Biggest win this month: _________________________________________________")
y -= 0.8*cm
c.drawString(1.5*cm, y, "One habit to improve next month: _______________________________________")

c.showPage()
c.save()

file_path
