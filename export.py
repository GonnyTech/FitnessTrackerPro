from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
import pandas as pd

def export_to_pdf(filename, pesi, allenamenti):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    story = []

    # Titolo
    story.append(Paragraph("Report Fitness", styles['h1']))
    story.append(Spacer(1, 0.2*inch))

    # Tabella Pesi
    if pesi:
        story.append(Paragraph("Andamento Peso", styles['h2']))
        df_pesi = pd.DataFrame([vars(p) for p in pesi])
        df_pesi = df_pesi.sort_values('data', ascending=False)
        data = [df_pesi.columns.to_list()] + df_pesi.values.tolist()
        
        t = Table(data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        story.append(t)
        story.append(Spacer(1, 0.2*inch))

    # Tabella Allenamenti
    if allenamenti:
        story.append(Paragraph("Dettaglio Allenamenti", styles['h2']))
        df_all = pd.DataFrame([vars(a) for a in allenamenti])
        df_all = df_all.sort_values('data', ascending=False)
        # Riordina e rinomina colonne
        cols = ['data', 'sport', 'durata', 'calorie', 'battito', 'vasche_risc', 'vasche_sess', 'note']
        df_all = df_all[[c for c in cols if c in df_all.columns]]
        df_all.columns = [c.replace('_',' ').title() for c in df_all.columns]
        
        data = [df_all.columns.to_list()] + df_all.values.tolist()
        
        t = Table(data, colWidths=[doc.width/len(df_all.columns)]*len(df_all.columns))
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.lightcyan),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('WORDWRAP', (0,0), (-1,-1), 'CJK')
        ]))
        story.append(t)

    doc.build(story) 