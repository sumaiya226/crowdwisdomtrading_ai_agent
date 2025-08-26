from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors
import datetime

def build_pdf_report(summary: dict, outpath: str, youtube_ids=None):
    doc = SimpleDocTemplate(outpath, pagesize=A4,
                            rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>CrowdWisdomTrading — Sentiment Summary</b>", styles["Title"]))
    story.append(Paragraph(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), styles["Normal"]))
    story.append(Spacer(1, 12))

    headers = ["User", "Avg Sentiment", "Top Tickers (dir • conf)"]
    rows = [headers]
    for u in summary["users_processed"]:
        res = summary["results"][u]
        avg = round(res["avg_sentiment"], 3)
        top = ", ".join([f'{t["ticker"]} {t["direction"]} • {t["confidence"]}' for t in res.get("tickers", [])[:5]])
        rows.append([u, avg, top or "-"])

    tbl = Table(rows, colWidths=[5*cm, 4*cm, 8*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("ALIGN", (1,1), (-1,-1), "LEFT"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 14))

    if youtube_ids:
        story.append(Paragraph("<b>YouTube RAG Highlights</b>", styles["Heading2"]))
        story.append(Paragraph("Included video IDs: " + ", ".join(youtube_ids), styles["Normal"]))
        story.append(Paragraph("RAG themes (example): AI earnings, chip demand, macro outlook.", styles["Normal"]))
        story.append(Spacer(1, 12))

    if summary.get("errors"):
        story.append(Paragraph("<b>Errors</b>", styles["Heading2"]))
        for u, e in summary["errors"].items():
            story.append(Paragraph(f"{u}: {e}", styles["Code"]))
        story.append(Spacer(1, 12))

    doc.build(story)