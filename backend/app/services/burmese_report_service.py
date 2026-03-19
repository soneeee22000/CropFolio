"""One-page Burmese (Myanmar) PDF report generator for field agents.

Generates a single A4 page with:
- Township name and season in Burmese
- Crop allocation table with Burmese names
- Key metrics (income, risk reduction, catastrophic loss probability)
- Top 2 fertilizer recommendations per crop
- Soil profile summary
- Data confidence indicators

Uses Padauk font for Myanmar Unicode script rendering.
"""

from __future__ import annotations

import io
import logging
from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.api.v1.schemas.report import ReportRequest

logger = logging.getLogger(__name__)

BRAND_GREEN = "#1B7A4A"
BRAND_LIGHT_GREEN = "#E8F5E9"
BORDER_GREY = "#E8E6E1"
CONFIDENCE_COLORS = {
    "high": "#2E7D32",
    "medium": "#F57F17",
    "low": "#C62828",
}

FONTS_DIR = Path(__file__).resolve().parent.parent.parent / "assets" / "fonts"
PADAUK_REGISTERED = False


def _register_padauk() -> bool:
    """Register Padauk font for Myanmar script rendering.

    Returns:
        True if fonts were registered successfully, False otherwise.
    """
    global PADAUK_REGISTERED
    if PADAUK_REGISTERED:
        return True

    regular_path = FONTS_DIR / "Padauk-Regular.ttf"
    bold_path = FONTS_DIR / "Padauk-Bold.ttf"

    if not regular_path.exists():
        logger.warning("Padauk-Regular.ttf not found at %s", regular_path)
        return False

    pdfmetrics.registerFont(TTFont("Padauk", str(regular_path)))
    if bold_path.exists():
        pdfmetrics.registerFont(TTFont("Padauk-Bold", str(bold_path)))

    PADAUK_REGISTERED = True
    return True


def _build_burmese_styles() -> dict[str, ParagraphStyle]:
    """Create paragraph styles using Padauk font for Myanmar script."""
    has_padauk = _register_padauk()
    font_name = "Padauk" if has_padauk else "Helvetica"
    bold_font = "Padauk-Bold" if has_padauk else "Helvetica-Bold"

    return {
        "title": ParagraphStyle(
            "BurmeseTitle",
            fontName=bold_font,
            fontSize=18,
            spaceAfter=4,
            textColor=colors.HexColor(BRAND_GREEN),
        ),
        "subtitle": ParagraphStyle(
            "BurmeseSubtitle",
            fontName=font_name,
            fontSize=10,
            spaceAfter=8,
            textColor=colors.grey,
        ),
        "heading": ParagraphStyle(
            "BurmeseHeading",
            fontName=bold_font,
            fontSize=11,
            spaceAfter=4,
            spaceBefore=8,
            textColor=colors.HexColor(BRAND_GREEN),
        ),
        "body": ParagraphStyle(
            "BurmeseBody",
            fontName=font_name,
            fontSize=9,
            spaceAfter=4,
        ),
        "small": ParagraphStyle(
            "BurmeseSmall",
            fontName=font_name,
            fontSize=7,
            spaceAfter=2,
            textColor=colors.grey,
        ),
        "footer": ParagraphStyle(
            "BurmeseFooter",
            fontName=font_name,
            fontSize=7,
            textColor=colors.grey,
        ),
    }


def generate_burmese_report_pdf(
    data: ReportRequest,
    soil_data: dict | None = None,
    fertilizer_recs: list[dict] | None = None,
    crop_confidence: dict[str, str] | None = None,
) -> bytes:
    """Generate a one-page Burmese PDF recommendation report.

    Args:
        data: Report request with portfolio allocation and metrics.
        soil_data: Optional soil profile dict (pH, fertility, texture).
        fertilizer_recs: Optional list of fertilizer recommendations per crop.
        crop_confidence: Optional dict mapping crop_name -> confidence level.

    Returns:
        PDF file content as bytes.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=15 * mm,
        bottomMargin=12 * mm,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
    )

    styles = _build_burmese_styles()
    elements: list[object] = []

    _add_header(elements, styles, data)
    _add_allocation_table(elements, styles, data, crop_confidence)
    _add_key_metrics(elements, styles, data)

    if fertilizer_recs:
        _add_fertilizer_recs(elements, styles, fertilizer_recs)

    if soil_data:
        _add_soil_summary(elements, styles, soil_data)

    _add_confidence_legend(elements, styles)
    _add_footer(elements, styles)

    doc.build(elements)
    return buffer.getvalue()


def _add_header(
    elements: list[object],
    styles: dict[str, ParagraphStyle],
    data: ReportRequest,
) -> None:
    """Add Burmese header with township, season, and date."""
    elements.append(Paragraph("CropFolio Pro", styles["title"]))
    elements.append(
        Paragraph(
            "သီးနှံ ခွဲဝေစိုက်ပျိုးမှု အကြံပြုချက်",
            styles["subtitle"],
        )
    )

    season_mm = "မိုးရာသီ" if data.season == "monsoon" else "ဆောင်းရာသီ"
    date_str = datetime.now().strftime("%Y-%m-%d")

    info_text = (
        f"မြို့နယ် - {data.township_name} &nbsp;|&nbsp; "
        f"ရာသီ - {season_mm} &nbsp;|&nbsp; "
        f"ရက်စွဲ - {date_str}"
    )
    elements.append(Paragraph(info_text, styles["body"]))
    elements.append(Spacer(1, 6))


def _add_allocation_table(
    elements: list[object],
    styles: dict[str, ParagraphStyle],
    data: ReportRequest,
    crop_confidence: dict[str, str] | None = None,
) -> None:
    """Add crop allocation table with Burmese names and confidence."""
    elements.append(
        Paragraph("သီးနှံ ခွဲဝေမှု", styles["heading"])
    )

    header = ["သီးနှံ", "Crop", "ခွဲဝေမှု %", "ယုံကြည်မှု"]
    table_data = [header]
    for alloc in data.allocations:
        confidence = "—"
        if crop_confidence and alloc.crop_name in crop_confidence:
            conf_level = crop_confidence[alloc.crop_name]
            conf_labels = {"high": "မြင့်", "medium": "အလယ်", "low": "နိမ့်"}
            confidence = conf_labels.get(conf_level, "—")

        table_data.append([
            alloc.crop_name_mm,
            alloc.crop_name,
            f"{alloc.weight_pct:.1f}%",
            confidence,
        ])

    col_widths = [100, 90, 65, 55]
    table = Table(table_data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(BRAND_GREEN)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ("TOPPADDING", (0, 0), (-1, 0), 6),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 4),
        ("TOPPADDING", (0, 1), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor(BORDER_GREY)),
        ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("ALIGN", (3, 0), (3, -1), "CENTER"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
            colors.white, colors.HexColor("#F5F5F5"),
        ]),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 6))


def _add_key_metrics(
    elements: list[object],
    styles: dict[str, ParagraphStyle],
    data: ReportRequest,
) -> None:
    """Add key performance metrics in Burmese."""
    elements.append(
        Paragraph("အဓိက ကိန်းဂဏန်းများ", styles["heading"])
    )

    income_fmt = f"{data.expected_income:,.0f}"
    metrics = [
        [
            "မျှော်မှန်းဝင်ငွေ",
            f"{income_fmt} ကျပ်/ဟက်တာ",
        ],
        [
            "အန္တရာယ် လျှော့ချမှု",
            f"{data.risk_reduction_pct:.1f}%",
        ],
        [
            "ဆုံးရှုံးမှုကြီး ဖြစ်နိုင်ခြေ",
            f"တစ်မျိုးတည်း {data.prob_catastrophic_loss_monocrop:.1f}% → "
            f"ကွဲပြား {data.prob_catastrophic_loss_diversified:.1f}%",
        ],
    ]

    table = Table(metrics, colWidths=[130, 200])
    table.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor(BRAND_GREEN)),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor(BORDER_GREY)),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor(BRAND_LIGHT_GREEN)),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 6))


def _add_fertilizer_recs(
    elements: list[object],
    styles: dict[str, ParagraphStyle],
    fertilizer_recs: list[dict],
) -> None:
    """Add top 2 fertilizer recommendations per crop."""
    elements.append(
        Paragraph(
            "ဓာတ်မြေသြဇာ အကြံပြုချက်များ",
            styles["heading"],
        )
    )

    header = ["သီးနှံ", "ဓာတ်မြေသြဇာ", "ဖော်မြူလာ", "နှုန်း kg/ha"]
    table_data = [header]

    for rec in fertilizer_recs:
        crop_name = rec.get("crop_name_mm", rec.get("crop_name", ""))
        ferts = rec.get("fertilizers", [])[:2]
        for i, fert in enumerate(ferts):
            row_crop = crop_name if i == 0 else ""
            table_data.append([
                row_crop,
                fert.get("name_mm", fert.get("name", "")),
                fert.get("formulation", ""),
                str(fert.get("rate_kg_per_ha", "")),
            ])

    col_widths = [80, 100, 65, 65]
    table = Table(table_data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(BRAND_GREEN)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 5),
        ("TOPPADDING", (0, 0), (-1, 0), 5),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 3),
        ("TOPPADDING", (0, 1), (-1, -1), 3),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor(BORDER_GREY)),
        ("ALIGN", (2, 0), (-1, -1), "CENTER"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
            colors.white, colors.HexColor("#F5F5F5"),
        ]),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 6))


def _add_soil_summary(
    elements: list[object],
    styles: dict[str, ParagraphStyle],
    soil_data: dict,
) -> None:
    """Add soil profile summary."""
    elements.append(
        Paragraph("မြေဆီလွှာ အကျဉ်းချုပ်", styles["heading"])
    )

    ph_val = soil_data.get("ph_h2o", "—")
    fertility = soil_data.get("fertility_rating", "—")
    texture = soil_data.get("texture_class", "—")

    fertility_mm = {
        "high": "မြင့်",
        "moderate": "အလယ်အလတ်",
        "low": "နိမ့်",
    }

    soil_info = (
        f"pH: {ph_val} &nbsp;|&nbsp; "
        f"မြေသြဇာ: {fertility_mm.get(str(fertility), str(fertility))} &nbsp;|&nbsp; "
        f"မြေအမျိုးအစား: {texture}"
    )
    elements.append(Paragraph(soil_info, styles["body"]))
    elements.append(Spacer(1, 4))


def _add_confidence_legend(
    elements: list[object],
    styles: dict[str, ParagraphStyle],
) -> None:
    """Add data confidence legend."""
    legend = (
        "အချက်အလက် ယုံကြည်မှု: "
        '<font color="#2E7D32">မြင့် = WFP/FAOSTAT တိုက်ရိုက်</font> | '
        '<font color="#F57F17">အလယ် = proxy အချက်အလက်</font> | '
        '<font color="#C62828">နိမ့် = စောင့်ဆိုင်းဆဲ/ခန့်မှန်း</font>'
    )
    elements.append(Paragraph(legend, styles["small"]))
    elements.append(Spacer(1, 4))


def _add_footer(
    elements: list[object],
    styles: dict[str, ParagraphStyle],
) -> None:
    """Add Burmese footer."""
    elements.append(
        Paragraph(
            "CropFolio Pro မှ ထုတ်လုပ်သည် — မြန်မာ့စိုက်ပျိုးရေးအတွက် "
            "ရာသီဥတု ခံနိုင်ရည်ရှိ သီးနှံစီမံခန့်ခွဲမှု",
            styles["footer"],
        )
    )
