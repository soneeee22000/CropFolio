"""PDF report generation service for CropFolio recommendations."""

from __future__ import annotations

import io
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.api.v1.schemas.report import ReportRequest
from app.domain.ai_prompts import AiNarrative

BRAND_GREEN = "#1B7A4A"
BORDER_GREY = "#E8E6E1"


def generate_report_pdf(
    data: ReportRequest,
    narrative: AiNarrative | None = None,
) -> bytes:
    """Generate a PDF recommendation report.

    Args:
        data: Report request with portfolio allocation and metrics.
        narrative: Optional AI-generated narrative sections.

    Returns:
        PDF file content as bytes.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=25 * mm,
        bottomMargin=20 * mm,
        leftMargin=25 * mm,
        rightMargin=25 * mm,
    )

    styles = _build_styles()
    elements: list[object] = []

    _add_header(elements, styles, data)
    _add_allocation_table(elements, styles, data)
    _add_key_metrics(elements, styles, data)

    if narrative is not None:
        _add_ai_insights(elements, styles, narrative)

    _add_footer(elements, styles)

    doc.build(elements)
    return buffer.getvalue()


def _build_styles() -> dict[str, ParagraphStyle]:
    """Create all paragraph styles for the report."""
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "ReportTitle", parent=base["Title"],
            fontSize=22, spaceAfter=6,
        ),
        "subtitle": ParagraphStyle(
            "ReportSubtitle", parent=base["Normal"],
            fontSize=12, textColor=colors.grey, spaceAfter=20,
        ),
        "heading": ParagraphStyle(
            "ReportHeading", parent=base["Heading2"],
            fontSize=14, spaceAfter=10, spaceBefore=16,
        ),
        "body": ParagraphStyle(
            "ReportBody", parent=base["Normal"],
            fontSize=11, spaceAfter=8,
        ),
        "footer": ParagraphStyle(
            "Footer", parent=base["Normal"],
            fontSize=9, textColor=colors.grey,
        ),
    }


def _add_header(
    elements: list[object],
    styles: dict[str, ParagraphStyle],
    data: ReportRequest,
) -> None:
    """Add title and township info header."""
    elements.append(Paragraph("CropFolio", styles["title"]))
    elements.append(
        Paragraph("Crop Portfolio Recommendation Report", styles["subtitle"])
    )
    elements.append(
        Paragraph(f"Township: {data.township_name}", styles["body"])
    )
    season_label = "Monsoon" if data.season == "monsoon" else "Dry"
    elements.append(Paragraph(f"Season: {season_label}", styles["body"]))
    elements.append(
        Paragraph(
            f"Generated: {datetime.now().strftime('%B %d, %Y')}",
            styles["body"],
        )
    )
    elements.append(Spacer(1, 12))


def _add_allocation_table(
    elements: list[object],
    styles: dict[str, ParagraphStyle],
    data: ReportRequest,
) -> None:
    """Add the crop allocation table."""
    elements.append(
        Paragraph("Recommended Crop Allocation", styles["heading"])
    )

    table_data = [["Crop", "Burmese", "Allocation"]]
    for alloc in data.allocations:
        table_data.append([
            alloc.crop_name,
            alloc.crop_name_mm,
            f"{alloc.weight_pct:.1f}%",
        ])

    table = Table(table_data, colWidths=[150, 120, 80])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(BRAND_GREEN)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("TOPPADDING", (0, 0), (-1, 0), 10),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
        ("TOPPADDING", (0, 1), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor(BORDER_GREY)),
        ("ALIGN", (-1, 0), (-1, -1), "CENTER"),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 16))


def _add_key_metrics(
    elements: list[object],
    styles: dict[str, ParagraphStyle],
    data: ReportRequest,
) -> None:
    """Add key metrics section."""
    elements.append(Paragraph("Key Metrics", styles["heading"]))
    income_fmt = f"{data.expected_income:,.0f} MMK/ha"
    elements.append(
        Paragraph(f"Expected Income: {income_fmt}", styles["body"])
    )
    elements.append(
        Paragraph(
            f"Risk Reduction: {data.risk_reduction_pct:.1f}%",
            styles["body"],
        )
    )
    elements.append(
        Paragraph(
            f"Catastrophic Loss Probability: "
            f"{data.prob_catastrophic_loss_monocrop:.1f}% (monocrop) vs "
            f"{data.prob_catastrophic_loss_diversified:.1f}% (diversified)",
            styles["body"],
        )
    )
    elements.append(Spacer(1, 20))


def _add_ai_insights(
    elements: list[object],
    styles: dict[str, ParagraphStyle],
    narrative: AiNarrative,
) -> None:
    """Add AI-powered insights section from Gemini narrative."""
    elements.append(
        Paragraph("AI-Powered Insights", styles["heading"])
    )
    elements.append(
        Paragraph(narrative.executive_summary, styles["body"])
    )
    elements.append(Spacer(1, 8))

    elements.append(
        Paragraph("Climate Risk Analysis", styles["heading"])
    )
    elements.append(
        Paragraph(narrative.risk_narrative, styles["body"])
    )
    elements.append(Spacer(1, 8))

    _add_recommendation_table(elements, styles, narrative)

    elements.append(
        Paragraph("Seasonal Calendar", styles["heading"])
    )
    elements.append(
        Paragraph(
            narrative.seasonal_calendar_summary, styles["body"]
        )
    )
    elements.append(Spacer(1, 12))


def _add_recommendation_table(
    elements: list[object],
    styles: dict[str, ParagraphStyle],
    narrative: AiNarrative,
) -> None:
    """Add crop recommendations table from AI narrative."""
    if not narrative.crop_recommendations:
        return

    elements.append(
        Paragraph("Crop Recommendations", styles["heading"])
    )

    table_data = [["Crop", "Recommendation", "Plant", "Harvest"]]
    for rec in narrative.crop_recommendations:
        table_data.append([
            rec.crop_name,
            Paragraph(rec.recommendation, styles["body"]),
            rec.planting_month,
            rec.harvest_month,
        ])

    table = Table(table_data, colWidths=[60, 250, 55, 55])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(BRAND_GREEN)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
        ("TOPPADDING", (0, 1), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor(BORDER_GREY)),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))


def _add_footer(
    elements: list[object],
    styles: dict[str, ParagraphStyle],
) -> None:
    """Add footer note."""
    elements.append(
        Paragraph(
            "Generated by CropFolio — Portfolio Theory for "
            "Climate-Resilient Farming in Myanmar",
            styles["footer"],
        )
    )
