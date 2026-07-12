#!/usr/bin/env python3
"""Generate a Europass-style CV PDF for Amalbek Bekpulatov.

Data sourced from his LinkedIn profile (linkedin.com/in/amalbek-bekpulatov)
and existing CV. Layout follows the classic Europass template: a narrow
label column on the left and content on the right, Europass blue accents,
and the standard section order (Personal information, Work experience,
Education and training, Personal skills, Additional information).

Usage:  python3 generate_europass_cv.py [output.pdf]
"""

import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

import os

PHOTO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "photo.jpg")

EUROPASS_BLUE = colors.HexColor("#0E4194")
LIGHT_BLUE = colors.HexColor("#D5E3F0")
GREY = colors.HexColor("#595959")

LABEL_W = 4.6 * cm
PAGE_W = A4[0] - 2 * 1.5 * cm
CONTENT_W = PAGE_W - LABEL_W

S = {
    "label": ParagraphStyle(
        "label", fontName="Helvetica", fontSize=8, leading=10,
        textColor=EUROPASS_BLUE, alignment=TA_LEFT, spaceBefore=0,
    ),
    "section": ParagraphStyle(
        "section", fontName="Helvetica-Bold", fontSize=11, leading=13,
        textColor=EUROPASS_BLUE,
    ),
    "name": ParagraphStyle(
        "name", fontName="Helvetica-Bold", fontSize=20, leading=24,
        textColor=EUROPASS_BLUE,
    ),
    "headline": ParagraphStyle(
        "headline", fontName="Helvetica-Oblique", fontSize=10, leading=13,
        textColor=GREY,
    ),
    "body": ParagraphStyle(
        "body", fontName="Helvetica", fontSize=9, leading=12,
    ),
    "jobtitle": ParagraphStyle(
        "jobtitle", fontName="Helvetica-Bold", fontSize=10, leading=13,
    ),
    "dates": ParagraphStyle(
        "dates", fontName="Helvetica", fontSize=8.5, leading=11,
        textColor=GREY,
    ),
    "small": ParagraphStyle(
        "small", fontName="Helvetica", fontSize=8, leading=10,
        textColor=GREY,
    ),
}


def row(label, flowables, top_pad=2):
    """One Europass row: blue label on the left, content on the right."""
    if not isinstance(flowables, list):
        flowables = [flowables]
    t = Table(
        [[Paragraph(label, S["label"]), flowables]],
        colWidths=[LABEL_W, CONTENT_W],
    )
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, -1), 0),
        ("LEFTPADDING", (1, 0), (1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), top_pad),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LINEAFTER", (0, 0), (0, -1), 0.75, LIGHT_BLUE),
    ]))
    return t


def section(title):
    return [
        Spacer(1, 10),
        row(f"<b>{title.upper()}</b>", HRFlowable(
            width="100%", thickness=1.2, color=EUROPASS_BLUE,
            spaceBefore=6, spaceAfter=0,
        )),
        Spacer(1, 4),
    ]


def bullets(items):
    return [
        Paragraph(f"&bull;&nbsp;&nbsp;{i}", S["body"]) for i in items
    ]


def experience(dates_place, title, employer, duties):
    content = [
        Paragraph(title, S["jobtitle"]),
        Paragraph(employer, S["small"]),
        Spacer(1, 2),
    ] + bullets(duties)
    return row(dates_place, content, top_pad=6)


def education(dates, title, institution, extra=None, eqf=None):
    content = [
        Paragraph(title, S["jobtitle"]),
        Paragraph(institution, S["small"]),
    ]
    if extra:
        content += [Spacer(1, 2), Paragraph(extra, S["body"])]
    if eqf:
        content += [Paragraph(f"EQF level: {eqf}", S["small"])]
    return row(dates, content, top_pad=6)


def lang_table():
    hdr = ParagraphStyle("hdr", parent=S["small"], alignment=1,
                         textColor=EUROPASS_BLUE)
    cell = ParagraphStyle("cell", parent=S["body"], alignment=1)
    lang = ParagraphStyle("lang", parent=S["body"], fontName="Helvetica-Bold")
    data = [
        ["", Paragraph("UNDERSTANDING", hdr), "", Paragraph("SPEAKING", hdr),
         "", Paragraph("WRITING", hdr)],
        ["", Paragraph("Listening", hdr), Paragraph("Reading", hdr),
         Paragraph("Spoken interaction", hdr),
         Paragraph("Spoken production", hdr), ""],
        [Paragraph("English", lang)] + [Paragraph(x, cell)
                                        for x in ("C1", "C1", "B2", "B2", "C1")],
        [Paragraph("German", lang)] + [Paragraph(x, cell)
                                       for x in ("B1", "B1", "A2", "A2", "B1")],
        [Paragraph("Turkish", lang)] + [Paragraph(x, cell)
                                        for x in ("B1", "B1", "B1", "B1", "B1")],
    ]
    w = CONTENT_W - 10
    t = Table(data, colWidths=[w * 0.2] + [w * 0.16] * 5)
    t.setStyle(TableStyle([
        ("SPAN", (1, 0), (2, 0)),
        ("SPAN", (3, 0), (4, 0)),
        ("SPAN", (5, 0), (5, 1)),
        ("GRID", (0, 0), (-1, -1), 0.5, LIGHT_BLUE),
        ("BACKGROUND", (0, 0), (-1, 1), colors.HexColor("#EEF4FA")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def build(path):
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=1.5 * cm, rightMargin=1.5 * cm,
        topMargin=1.4 * cm, bottomMargin=1.4 * cm,
        title="Europass CV - Amalbek Bekpulatov",
        author="Amalbek Bekpulatov",
    )
    e = []

    name_block = [
        Paragraph("Amalbek Bekpulatov", S["name"]),
        Spacer(1, 2),
        Paragraph(
            "Outsourcing Specialist @ Uztelecom &nbsp;|&nbsp; "
            "International Business Management", S["headline"]),
    ]
    if os.path.exists(PHOTO):
        photo = Image(PHOTO, width=3.2 * cm, height=3.2 * cm)
        header = Table(
            [[name_block, photo]],
            colWidths=[CONTENT_W - 10 - 3.4 * cm, 3.4 * cm],
        )
        header.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
        ]))
        name_block = [header]
    e.append(row("Curriculum Vitae<br/><font size=8>Europass</font>",
                 name_block))

    e += section("Personal information")
    e.append(row("Address", Paragraph("Tashkent, Uzbekistan", S["body"])))
    e.append(row("Telephone", Paragraph("(+998) 90 127 11 91", S["body"])))
    e.append(row("E-mail", Paragraph(
        '<link href="mailto:bekpulatov02@icloud.com" color="#0E4194">'
        "bekpulatov02@icloud.com</link>", S["body"])))
    e.append(row("LinkedIn", Paragraph(
        '<link href="https://linkedin.com/in/amalbek-bekpulatov" '
        'color="#0E4194">linkedin.com/in/amalbek-bekpulatov</link>',
        S["body"])))
    e.append(row("Date of birth", Paragraph("04/09/2004", S["body"])))
    e.append(row("Nationality", Paragraph("Uzbek", S["body"])))

    e += section("Work experience")
    e.append(experience(
        "October 2025 – Present<br/>Tashkent, Uzbekistan",
        "Outsourcing Specialist — International Outsource Department",
        "Contact Center LLC (Uztelecom), full-time, on-site",
        [
            "Primary point of contact for foreign partners: international "
            "client communication and support requests handled to "
            "professional standards.",
            "Multilingual customer service (English, Russian, Uzbek) with "
            "high satisfaction and resolution rates.",
            "Coordination of cross-departmental workflows to optimise "
            "service delivery for international clients.",
            "Representation of the department in correspondence with "
            "international stakeholders.",
        ]))
    e.append(experience(
        "March 2025 – July 2025<br/>Gulistan, Uzbekistan",
        "Intern Assistant — International Relations Department",
        "Sirdaryo Regional Department of Investments, Trade and Industry",
        [
            "Supported organisational and administrative tasks; assisted in "
            "coordinating events, meetings and delegation visits at "
            "government level.",
            "Contributed to documentation, reporting and communication "
            "processes in English and Russian.",
            "Gained experience in teamwork, project support and "
            "intercultural interaction.",
        ]))
    e.append(experience(
        "February 2024 – July 2024<br/>Tashkent, Uzbekistan",
        "Call Center Operator",
        "Beeline Uzbekistan",
        [
            "Provided customer support via phone, resolving inquiries "
            "efficiently and meeting performance targets for call handling, "
            "response time and service quality.",
            "Assisted clients with mobile services, tariffs and technical "
            "troubleshooting; processed requests, payments and service "
            "activations with accuracy.",
            "Ensured high customer satisfaction through clear, polite, "
            "solution-oriented communication.",
        ]))
    e.append(experience(
        "June 2023 – August 2023<br/>Tashkent, Uzbekistan",
        "Administrator — Front Desk & Operations",
        "Safarov's Family Hostel",
        [
            "Managed daily front-desk operations, including guest check-in "
            "and check-out for international travellers.",
            "Handled reservations, inquiries and customer support in "
            "multiple languages; maintained records, payments and basic "
            "accounting.",
            "Coordinated housekeeping and maintenance to ensure high "
            "service standards; resolved guest issues promptly.",
        ]))

    e += section("Education and training")
    e.append(education(
        "September 2022 – June 2026",
        "Bachelor's degree — International Business Management",
        "Tashkent State University of Economics, Tashkent (Uzbekistan) — "
        "double-degree programme with IMC Krems University of Applied "
        "Sciences (Austria)",
        "Dual-accredited programme combining Uzbek and Austrian "
        "higher-education standards in international business.",
        "6",
    ))
    e.append(education(
        "September 2024 – February 2025",
        "Academic exchange — International Management Studies "
        "(Baltic Sea Region)",
        "Hochschule Stralsund — University of Applied Sciences, "
        "Stralsund (Germany)",
        "DAAD scholarship recipient; 30 ECTS. Studied international "
        "management in a European context; participated in International "
        "Exchange Programme activities and local sports teams.",
        "6",
    ))
    e.append(education(
        "September 2022 – June 2023",
        "Foundation Degree",
        "IMC Krems University of Applied Sciences, Krems (Austria)",
        None,
        "5",
    ))
    e.append(education(
        "September 2011 – June 2022",
        "High School Diploma",
        "Secondary School No. 5, Gulistan (Uzbekistan)",
        None,
        "4",
    ))

    e += section("Personal skills")
    e.append(row("Mother tongue(s)", Paragraph(
        "<b>Uzbek, Russian</b>", S["body"])))
    e.append(row("Other language(s)", [
        lang_table(),
        Spacer(1, 2),
        Paragraph("Levels: A1/A2 — Basic user; B1/B2 — Independent user; "
                  "C1/C2 — Proficient user (CEFR)", S["small"]),
    ], top_pad=6))
    e.append(row("Communication skills", Paragraph(
        "Multilingual client support in five languages; cross-cultural "
        "communication developed through work with international partners, "
        "a DAAD exchange semester in Germany and front-desk roles serving "
        "international guests.", S["body"]), top_pad=6))
    e.append(row("Organisational skills", Paragraph(
        "Office administration and coordination; event and travel "
        "logistics; records, reporting and documentation; time management "
        "and calm prioritisation of parallel tasks.", S["body"]), top_pad=6))
    e.append(row("Digital skills", Paragraph(
        "Microsoft Office Suite (Word, Excel, PowerPoint, Outlook, "
        "OneNote); strong presentation and analytical skills.",
        S["body"]), top_pad=6))
    e.append(row("Driving licence", Paragraph("Category B", S["body"]),
                 top_pad=6))

    e += section("Additional information")
    e.append(row("Honours and awards", Paragraph(
        "DAAD Scholarship Recipient — funded exchange semester at "
        "Hochschule Stralsund, Germany (2024–2025).", S["body"])))
    e.append(row("Work authorisation<br/>and mobility", Paragraph(
        "EU-recognised Austrian degree (IMC Krems) supporting German "
        "skilled-worker immigration routes; Chancenkarte (Opportunity "
        "Card) application in progress. Open to relocation (Vienna, "
        "Austria and other EU locations).", S["body"]), top_pad=6))
    e.append(row("Interests", Paragraph(
        "Guitar performance (acoustic and electric); football; "
        "intercultural exchange; international relations.", S["body"]),
        top_pad=6))
    e.append(row("References", Paragraph(
        "Available upon request.", S["body"]), top_pad=6))

    doc.build(e)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else \
        "Amalbek_Bekpulatov_Europass_CV.pdf"
    build(out)
    print(f"Written {out}")
