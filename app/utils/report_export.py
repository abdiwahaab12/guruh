"""Report export helpers — CSV, Excel, PDF."""

from __future__ import annotations

import csv
import io
from datetime import datetime


def export_csv(rows: list[list[str]]) -> bytes:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(rows)
    return output.getvalue().encode("utf-8-sig")


def export_excel(rows: list[list[str]], sheet_name: str = "Report") -> bytes:
    try:
        from openpyxl import Workbook

        wb = Workbook()
        ws = wb.active
        ws.title = sheet_name[:31]
        for row in rows:
            ws.append(row)
        buf = io.BytesIO()
        wb.save(buf)
        return buf.getvalue()
    except ImportError:
        return export_csv(rows)


def export_pdf(title: str, rows: list[list[str]]) -> bytes:
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=landscape(A4))
        styles = getSampleStyleSheet()
        story = [
            Paragraph(title, styles["Title"]),
            Paragraph(f"Generated {datetime.utcnow().strftime('%d %b %Y %H:%M UTC')}", styles["Normal"]),
            Spacer(1, 12),
        ]
        if rows:
            table = Table(rows, repeatRows=1)
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0d6efd")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                        ("FONTSIZE", (0, 0), (-1, -1), 8),
                        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
                    ]
                )
            )
            story.append(table)
        doc.build(story)
        return buf.getvalue()
    except ImportError:
        lines = [title, ""] + [" | ".join(r) for r in rows]
        return "\n".join(lines).encode("utf-8")
