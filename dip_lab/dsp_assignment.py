import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def create_proposal_pdf(filename="Bangla_HTR_CRNN_Proposal.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    primary_color = colors.HexColor("#1A365D")  # Deep Navy
    secondary_color = colors.HexColor("#2B6CB0")  # Slate Blue
    body_color = colors.HexColor("#2D3748")  # Charcoal

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=primary_color,
        spaceAfter=4,
    )

    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#718096"),
        spaceAfter=12,
    )

    h1_style = ParagraphStyle(
        "SectionH1",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=6,
    )

    h2_style = ParagraphStyle(
        "SectionH2",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=secondary_color,
        spaceBefore=8,
        spaceAfter=4,
    )

    body_style = ParagraphStyle(
        "DocBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13.5,
        textColor=body_color,
        spaceAfter=6,
    )

    code_block_style = ParagraphStyle(
        "CodeBlock",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor("#1A202C"),
        backColor=colors.HexColor("#EDF2F7"),
        borderColor=colors.HexColor("#CBD5E0"),
        borderWidth=0.5,
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=6,
    )

    story = []

    # Title & Metadata
    story.append(
        Paragraph("PROJECT PROPOSAL: OFFLINE BANGLA HTR VIA CRNN-CTC", title_style)
    )
    story.append(
        Paragraph(
            "<b>Target Domain:</b> Document AI & Pattern Recognition &nbsp;|&nbsp; <b>Architecture:</b> VGG-BiLSTM-CTC &nbsp;|&nbsp; <b>Date:</b> September 2026",
            subtitle_style,
        )
    )
    story.append(
        HRFlowable(
            width="100%",
            thickness=1.5,
            color=primary_color,
            spaceBefore=0,
            spaceAfter=10,
        )
    )

    # 1. Executive Summary
    story.append(Paragraph("1. Executive Summary", h1_style))
    story.append(
        Paragraph(
            "Handwritten Text Recognition (HTR) for Bengali presents acute technical challenges due to structural complexities: the continuous horizontal upper line (<i>matra</i>), overlapping vowel diacritics (<i>kar</i>), consonant modifiers (<i>fola</i>), and complex conjunct characters (<i>juktakkhor</i>). Traditional OCR relying on explicit character segmentation fails systematically on cursive handwriting due to broken strokes and irregular kerning.",
            body_style,
        )
    )
    story.append(
        Paragraph(
            "This project builds an <b>end-to-end, offline Bangla Handwritten Text Recognition system</b> utilizing a <b>Convolutional Recurrent Neural Network (CRNN)</b> trained with <b>Connectionist Temporal Classification (CTC) loss</b>. The model bypasses discrete character segmentation, mapping cropped handwritten word images directly to UTF-8 Bengali text sequences, designed as an ingestion tool for downstream RAG and research agents.",
            body_style,
        )
    )

    # 2. Problem Statement
    story.append(Paragraph("2. Problem Formulation & Challenges", h1_style))
    story.append(
        Paragraph(
            "• <b>Absence of Discrete Boundaries:</b> Glyphs connect organically along the top <i>matra</i> bar and lower loops, rendering explicit bounding-box segmentation fragile.<br/>"
            "• <b>High Grapheme Cardinality:</b> Bengali consists of 11 vowels, 39 consonants, 10 diacritics, and over 250 compound ligatures, making single-character classification impractical.<br/>"
            "• <b>Non-Linear Script Order:</b> Visual glyph placement does not always mirror phonetic storage order (e.g., <i>E-kar</i> appears visually to the left of the base consonant it modifies).",
            body_style,
        )
    )

    # 3. Proposed Architecture
    story.append(
        Paragraph("3. Proposed Architecture & Theoretical Basis", h1_style)
    )
    pipeline_text = (
        "Input Image (1 x 32 x W)<br/>"
        "  │<br/>"
        "  ▼<br/>"
        "[Stage 1: VGG-Style CNN Backbone]  ──► 7 Conv Layers + BatchNorm + LeakyReLU (H reduced: 32 -> 1, W -> W/4)<br/>"
        "  │<br/>"
        "  ▼<br/>"
        "[Stage 2: 2-Layer Bidirectional LSTM] ──► Captures bidirectional grapheme dependencies (T = W/4 time steps)<br/>"
        "  │<br/>"
        "  ▼<br/>"
        "[Stage 3: Linear Projection Layer]  ──► Projects hidden states to vocabulary distribution + CTC Blank<br/>"
        "  │<br/>"
        "  ▼<br/>"
        "[Stage 4: CTCLoss / Best-Path Decode] ──► Sums over all alignment paths; collapses duplicates & removes blanks"
    )
    story.append(Paragraph(pipeline_text, code_block_style))

    story.append(
        Paragraph(
            "• <b>Why CNN Backbone:</b> Extracts hierarchical, shift-invariant visual features (strokes, loops) robust to ink variations and slant.<br/>"
            "• <b>Why Bidirectional LSTM:</b> Bengali diacritics modify preceding or trailing base characters; bidirectional passes evaluate both directions before committing to predictions.<br/>"
            "• <b>Why CTC Loss:</b> Eliminates manual character-level boundary labeling by marginalizing over all valid sequence alignments during optimization.",
            body_style,
        )
    )

    # 4. Dataset & Preprocessing
    story.append(Paragraph("4. Dataset & Preprocessing Strategy", h1_style))
    story.append(
        Paragraph(
            "• <b>Target Benchmark:</b> <b>BanglaWriting</b> (Mridha et al., 2021) comprising 260 writers, 21,234 word instances, and 5,470 unique vocabulary words with bounding-box ground truths.<br/>"
            "• <b>Image Normalization:</b> Grayscale conversion, CLAHE contrast equalization, aspect-ratio preserved resizing to fixed height H = 32 pixels, and zero-padding up to width W = 128 / 256 pixels.<br/>"
            "• <b>Data Augmentation:</b> Random affine shear (±7°), mild perspective transforms, and morphological dilation/erosion to simulate varying fountain pen nibs and writing speeds.",
            body_style,
        )
    )

    # 5. Evaluation Metrics & Success Criteria
    story.append(Paragraph("5. Evaluation Metrics & Target Benchmarks", h1_style))

    metric_table_data = [
        [
            Paragraph("<b>Metric</b>", body_style),
            Paragraph("<b>Formula / Definition</b>", body_style),
            Paragraph("<b>Success Threshold</b>", body_style),
        ],
        [
            Paragraph("<b>Character Error Rate (CER)</b>", body_style),
            Paragraph(
                "CER = (S + D + I) / N (Levenshtein edit distance)", body_style
            ),
            Paragraph("&le; 12.0% on test split", body_style),
        ],
        [
            Paragraph("<b>Word Error Rate (WER)</b>", body_style),
            Paragraph(
                "Exact whole-word transcription match percentage", body_style
            ),
            Paragraph("&le; 28.0% on test split", body_style),
        ],
        [
            Paragraph("<b>Inference Latency</b>", body_style),
            Paragraph("Wall-clock time per cropped word evaluation", body_style),
            Paragraph("&lt; 45 ms on standard CPU", body_style),
        ],
    ]

    t = Table(metric_table_data, colWidths=[1.7 * inch, 3.2 * inch, 1.8 * inch])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    story.append(t)
    story.append(Spacer(1, 8))

    # 6. Technical Stack
    story.append(Paragraph("6. Resource Requirements & Tech Stack", h1_style))
    story.append(
        Paragraph(
            "• <b>Framework:</b> PyTorch 2.x (<code>torch.nn.CTCLoss</code>), Torchvision<br/>"
            "• <b>Computer Vision:</b> OpenCV (cv2), Pillow (PIL), NumPy<br/>"
            "• <b>Evaluation:</b> <code>editdistance</code>, <code>jiwer</code><br/>"
            "• <b>Compute Requirements:</b> 1x NVIDIA T4 / RTX 3060 GPU (~3 hours training) or free Google Colab tier.",
            body_style,
        )
    )

    doc.build(story)
    print(f"[✓] Successfully generated proposal PDF: {filename}")


if __name__ == "__main__":
    create_proposal_pdf()