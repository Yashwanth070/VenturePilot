import io
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.colors import HexColor

def markdown_to_platypus(text):
    """A very simple converter from markdown to ReportLab Platypus Paragraphs."""
    styles = getSampleStyleSheet()
    
    # Custom styles
    h1_style = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=20, spaceAfter=14, textColor=HexColor('#1f6feb'))
    h2_style = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=16, spaceAfter=10, textColor=HexColor('#58a6ff'))
    h3_style = ParagraphStyle('H3', parent=styles['Heading3'], fontSize=14, spaceAfter=8, textColor=HexColor('#a371f7'))
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=11, spaceAfter=6, leading=14)
    bullet_style = ParagraphStyle('Bullet', parent=styles['Normal'], fontSize=11, spaceAfter=6, leading=14, leftIndent=20)
    
    story = []
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            story.append(Spacer(1, 6))
            continue
            
        # Bold text (simple replacement for reportlab)
        line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
        
        if line.startswith('### '):
            story.append(Paragraph(line[4:], h3_style))
        elif line.startswith('## '):
            story.append(Paragraph(line[3:], h2_style))
        elif line.startswith('# '):
            story.append(Paragraph(line[2:], h1_style))
        elif line.startswith('- ') or line.startswith('* '):
            # Bullet point
            bullet_text = f"• {line[2:]}"
            story.append(Paragraph(bullet_text, bullet_style))
        else:
            story.append(Paragraph(line, body_style))
            
    return story

def generate_startup_report(data):
    """Generates a PDF report from the startup analysis data."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    
    story = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Title'], fontSize=28, spaceAfter=20, textColor=HexColor('#0d1117'))
    
    # Title Page
    story.append(Paragraph("VenturePilot Analysis Report", title_style))
    story.append(Spacer(1, 20))
    
    input_data = data.get('input_data', {})
    
    # Overview
    overview_text = f"""
    ## Startup Overview
    **Name:** {input_data.get('details', '').split('Industry')[0].replace('Name:', '').strip()}
    **Industry:** {input_data.get('Industry', '')}
    **Target Audience:** {input_data.get('details', '').split('Revenue:')[0].split('Target:')[-1].strip() if 'Target:' in input_data.get('details', '') else 'N/A'}
    **Revenue Model:** {input_data.get('Revenue_Model', '')}
    """
    story.extend(markdown_to_platypus(overview_text))
    story.append(Spacer(1, 20))
    
    # Prediction
    pred = data.get('prediction', {})
    story.extend(markdown_to_platypus(f"## ML Success Prediction\n**Score:** {pred.get('success_probability', 0)}%\n**Method:** {pred.get('method', '')}"))
    story.append(Spacer(1, 20))
    
    # Insights
    sections = [
        ("Executive Pitch", data.get('pitch', '')),
        ("SWOT Analysis", data.get('swot', '')),
        ("Competitor Analysis", data.get('competitors', '')),
        ("Business Model Canvas", data.get('bmc', '')),
        ("Strategic Roadmap", data.get('roadmap', '')),
        ("Funding Strategy", data.get('funding', ''))
    ]
    
    for title, content in sections:
        if content and content != 'Generation failed.':
            story.extend(markdown_to_platypus(f"## {title}\n{content}"))
            story.append(Spacer(1, 20))
    
    doc.build(story)
    buffer.seek(0)
    return buffer
