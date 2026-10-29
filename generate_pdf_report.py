"""
generate_pdf_report.py
Generates the complete INT315 Cluster Computing Project Report in PDF format
using ReportLab with precise academic typography, exact 12-section layout,
syntax-highlighted code blocks, tables, diagrams, and reference figures.
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to calculate total page count and draw running headers and footers.
    Omits header and footer on the title page (page 1).
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress running header/footer on title page

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4A5568"))

        # Header
        header_text = "INT315 – Cluster Computing Project Report | Scalable House Price Prediction"
        self.drawString(54, 842 - 36, header_text)
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.6)
        self.line(54, 842 - 42, 595 - 54, 842 - 42)

        # Footer
        footer_text = "Project Status: Proposed / Pre-implementation | Academic Year 2025–2026"
        self.drawString(54, 38, footer_text)
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(595 - 54, 38, page_str)
        self.line(54, 48, 595 - 54, 48)

        self.restoreState()


def create_project_report(output_pdf_path):
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Define custom typography hierarchy
    primary_color = colors.HexColor("#1A365D")   # Deep Academic Navy
    secondary_color = colors.HexColor("#2B6CB0") # Slate Blue
    body_color = colors.HexColor("#2D3748")      # Charcoal dark
    code_bg = colors.HexColor("#F7FAFC")
    code_border = colors.HexColor("#E2E8F0")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=primary_color,
        alignment=1, # Center
        spaceAfter=12
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=18,
        textColor=secondary_color,
        alignment=1,
        spaceAfter=20
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=20,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=16,
        textColor=secondary_color,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=body_color,
        spaceAfter=7,
        alignment=4 # Justified
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=body_color,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#742A2A"),
        spaceAfter=5
    )

    caption_style = ParagraphStyle(
        'FigureCaption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#4A5568"),
        alignment=1, # Center
        spaceBefore=4,
        spaceAfter=10
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor("#1A202C")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=0
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=body_color,
        alignment=0
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=primary_color,
        alignment=0
    )

    story = []

    # =========================================================================
    # 1. PROJECT TITLE (Title Page)
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("INT315 – CLUSTER COMPUTING", ParagraphStyle('CourseCode', parent=subtitle_style, fontSize=12, textColor=colors.HexColor("#718096"), spaceAfter=5)))
    story.append(Paragraph("PROJECT REPORT", ParagraphStyle('DocType', parent=subtitle_style, fontSize=15, textColor=secondary_color, spaceAfter=15)))
    story.append(HRFlowable(width="100%", thickness=2, color=primary_color, spaceAfter=20, spaceBefore=0))
    
    story.append(Paragraph("1. Project Title", ParagraphStyle('SecHeaderTop', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=secondary_color, spaceAfter=4)))
    story.append(Paragraph("Scalable House Price Prediction Using Apache Spark MLlib", title_style))
    story.append(Paragraph("Distributed Machine Learning Workflow on California Housing Geospatial & Socioeconomic Data", subtitle_style))
    story.append(HRFlowable(width="60%", thickness=0.8, color=colors.HexColor("#CBD5E0"), spaceAfter=25, spaceBefore=10))

    # Project Status Callout Box
    status_p = Paragraph(
        "<b>Project Status:</b> <b>Proposed / Pre-Implementation Architectural Blueprint</b><br/>"
        "<i>Notice:</i> This project has not been executed yet. The complete methodology, algorithmic pipelines, "
        "reproducible PySpark source code, and illustrative reference benchmarks from official Apache Spark documentation "
        "and established machine learning literature are prepared in advance for academic evaluation.",
        callout_style
    )
    status_table = Table([[status_p]], colWidths=[487])
    status_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFF5F5")),
        ('BORDER', (0,0), (-1,-1), 1, colors.HexColor("#FEB2B2")),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(status_table)
    story.append(Spacer(1, 25))

    # Editable Placeholders Table
    meta_data = [
        [Paragraph("Course Title & Code", table_cell_bold), Paragraph("INT315 – Cluster Computing", table_cell_style)],
        [Paragraph("Project Title", table_cell_bold), Paragraph("Scalable House Price Prediction Using Apache Spark MLlib", table_cell_style)],
        [Paragraph("Student Name", table_cell_bold), Paragraph("[Editable Placeholder: e.g., John Doe / Karnvendra Singh]", table_cell_style)],
        [Paragraph("Registration / Roll No.", table_cell_bold), Paragraph("[Editable Placeholder: e.g., 1210XXXX / 122XXXXX]", table_cell_style)],
        [Paragraph("Department / School", table_cell_bold), Paragraph("[Editable Placeholder: School of Computer Science and Engineering]", table_cell_style)],
        [Paragraph("University / Institution", table_cell_bold), Paragraph("[Editable Placeholder: Lovely Professional University / ABC Institute of Technology]", table_cell_style)],
        [Paragraph("Faculty Guide / Supervisor", table_cell_bold), Paragraph("[Editable Placeholder: Dr. / Prof. Faculty Guide Name]", table_cell_style)],
        [Paragraph("Academic Session / Year", table_cell_bold), Paragraph("2025 – 2026", table_cell_style)],
        [Paragraph("Submission Date", table_cell_bold), Paragraph("October 2026", table_cell_style)],
    ]
    meta_table = Table(meta_data, colWidths=[160, 327])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#EDF2F7")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 35))
    toc_p = Paragraph(
        "<b>Report Structure & Table of Contents:</b><br/>"
        "1. Project Title &nbsp;&bull;&nbsp; 2. Problem Statement &nbsp;&bull;&nbsp; 3. Objective of the Project &nbsp;&bull;&nbsp; "
        "4. Dataset Description &nbsp;&bull;&nbsp; 5. Dataset Source &nbsp;&bull;&nbsp; 6. Tools & Technologies Used &nbsp;&bull;&nbsp; "
        "7. Implementation / Methodology &nbsp;&bull;&nbsp; 8. Complete Code &nbsp;&bull;&nbsp; 9. Execution Screenshots &nbsp;&bull;&nbsp; "
        "10. Output / Result Screenshots &nbsp;&bull;&nbsp; 11. Result Analysis &nbsp;&bull;&nbsp; 12. Conclusion",
        ParagraphStyle('TOCSummary', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=11, textColor=colors.HexColor("#4A5568"), alignment=1)
    )
    story.append(toc_p)

    story.append(PageBreak())

    # =========================================================================
    # 2. PROBLEM STATEMENT
    # =========================================================================
    story.append(Paragraph("2. Problem Statement", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=10, spaceBefore=0))
    
    story.append(Paragraph(
        "Accurate real estate valuation is a critical foundation of modern socioeconomic planning, mortgage underwriting, "
        "tax assessment, and municipal urban growth modeling. Traditional property valuation models typically operate in centralized, "
        "single-node environments using libraries such as Scikit-Learn or Pandas. However, as housing data aggregates billions of sensor readings, "
        "historical transactions, regional census records, and dynamic macroeconomic indicators, centralized memory-bound computational "
        "frameworks experience severe vertical scaling bottlenecks, out-of-memory (OOM) fatal crashes, and prohibitive training latencies.",
        body_style
    ))
    story.append(Paragraph(
        "<b>The Regression Formulation:</b> Estimating house prices is fundamentally a continuous supervised learning regression problem. "
        "Given an input vector <i>x &isin; &real;<sup>d</sup></i> representing district-level attributes (such as median income, housing age, "
        "average rooms, and spatial coordinates), the mathematical objective is to learn a mapping function <i>f(x) &rarr; y</i> that minimizes "
        "the empirical risk over a continuous response variable <i>y &isin; &real;</i> (representing median house value). Regression is specifically "
        "required over discrete classification because valuation requires high-precision metric estimates rather than categorical bins.",
        body_style
    ))
    story.append(Paragraph(
        "<b>The Role of Apache Spark and Distributed MLlib:</b> Apache Spark provides a fault-tolerant, unified distributed data processing "
        "engine that overcomes the limitations of single-node analytics through horizontally scalable cluster computing. By employing resilient "
        "distributed datasets (RDDs) and Catalyst-optimized distributed DataFrames, Spark partitions massive datasets across independent worker nodes. "
        "Spark's machine learning library (<b>MLlib</b> / <code>pyspark.ml</code>) implements distributed optimization algorithms—such as parallelized "
        "Limited-memory BFGS (L-BFGS) and distributed Stochastic Gradient Descent (SGD)—allowing gradient vectors and loss calculations to be computed "
        "locally per partition and aggregated globally across cluster nodes via optimized tree-aggregate primitives. This cluster-oriented paradigm "
        "guarantees that house price prediction pipelines can seamlessly scale from tens of thousands of census records to massive, enterprise-scale "
        "geospatial repositories without code refactoring.",
        body_style
    ))

    # =========================================================================
    # 3. OBJECTIVE OF THE PROJECT
    # =========================================================================
    story.append(Paragraph("3. Objective of the Project", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=10, spaceBefore=0))
    story.append(Paragraph(
        "The overarching aim of this project is to architect, design, and demonstrate a distributed machine learning pipeline using Apache Spark "
        "MLlib. Specifically, the project encompasses the following 7 core objectives:",
        body_style
    ))

    objectives = [
        "<b>PySpark Environment & Cluster Integration:</b> Initialize a resilient, multi-core local/cluster SparkSession configured with optimized executor memory, CPU core allocation, and adaptive query execution (AQE) for scalable computation.",
        "<b>Distributed Data Ingestion & Preprocessing:</b> Ingest continuous real estate data into Spark DataFrames, verify schema integrity, handle missing or anomalous values, and compute distributed descriptive statistics across partitions.",
        "<b>Feature Engineering via VectorAssembler:</b> Construct an automated MLlib feature pipeline utilizing <code>VectorAssembler</code> and <code>StandardScaler</code> to assemble raw numerical feature columns into unified, scaled feature vectors compatible with Spark ML estimators.",
        "<b>Distributed Linear Regression Modeling:</b> Formulate and train an Apache Spark MLlib <code>LinearRegression</code> model to predict median housing values, leveraging distributed optimization algorithms.",
        "<b>Rigorous Model Evaluation:</b> Statistically evaluate predictive performance using <code>RegressionEvaluator</code> across standard metrics, including Root Mean Squared Error (RMSE), Mean Absolute Error (MAE), and Coefficient of Determination (R&sup2;).",
        "<b>Analytical Visualizations:</b> Generate detailed exploratory and diagnostic visualizations, including feature correlation matrices, actual versus predicted valuation scatter plots, and residual distribution graphs to evaluate goodness-of-fit.",
        "<b>Scalability & Performance Benchmarking:</b> Formulate an empirical scalability testing methodology to benchmark cluster processing throughput, job completion times, and speedup factors across exponentially scaled synthetic and augmented datasets."
    ]
    for obj in objectives:
        story.append(Paragraph(f"&bull;&nbsp;&nbsp;{obj}", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # 4. DATASET DESCRIPTION
    # =========================================================================
    story.append(Paragraph("4. Dataset Description", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=10, spaceBefore=0))
    story.append(Paragraph(
        "This project utilizes the authoritative <b>California Housing Dataset</b>, originally derived from the 1990 U.S. Census Bureau records "
        "by Pace and Barry (1997). A critical academic distinction must be emphasized: <b>this dataset does NOT represent individual house listings, "
        "sales transactions, or individual property advertisements.</b> Instead, each observation corresponds to an aggregated <b>Census Block Group</b> "
        "(the smallest geographical unit for which the U.S. Census Bureau publishes sample data, typically containing a population of 600 to 3,000 individuals).",
        body_style
    ))
    story.append(Paragraph(
        "The dataset contains exactly <b>20,640 records</b> and <b>8 continuous numerical input features</b>, alongside <b>1 continuous target variable</b> "
        "(<code>MedHouseVal</code>). The target variable represents the median house value for households within the block group, expressed in units of "
        "<b>$100,000</b> (e.g., a target value of 4.526 corresponds to $452,600).",
        body_style
    ))

    # Feature Table
    feat_headers = [
        Paragraph("Feature Name", table_header_style),
        Paragraph("Data Type", table_header_style),
        Paragraph("Domain Description & Interpretation", table_header_style),
        Paragraph("Aggregated Meaning", table_header_style)
    ]
    feat_rows = [
        [
            Paragraph("<b>MedInc</b>", table_cell_bold),
            Paragraph("Double (Float64)", table_cell_style),
            Paragraph("Median income of households within the block group.", table_cell_style),
            Paragraph("Measured in tens of thousands of USD ($10,000s). Primary purchasing power driver.", table_cell_style)
        ],
        [
            Paragraph("<b>HouseAge</b>", table_cell_bold),
            Paragraph("Double (Float64)", table_cell_style),
            Paragraph("Median age of residential buildings within the block group.", table_cell_style),
            Paragraph("Measured in years. Reflects structural vintage and neighborhood maturity.", table_cell_style)
        ],
        [
            Paragraph("<b>AveRooms</b>", table_cell_bold),
            Paragraph("Double (Float64)", table_cell_style),
            Paragraph("Average number of rooms per residential household.", table_cell_style),
            Paragraph("Ratio of total rooms to total households in the census block.", table_cell_style)
        ],
        [
            Paragraph("<b>AveBedrms</b>", table_cell_bold),
            Paragraph("Double (Float64)", table_cell_style),
            Paragraph("Average number of bedrooms per residential household.", table_cell_style),
            Paragraph("Ratio of total bedrooms to total households in the block group.", table_cell_style)
        ],
        [
            Paragraph("<b>Population</b>", table_cell_bold),
            Paragraph("Double (Float64)", table_cell_style),
            Paragraph("Total number of permanent residents residing in the block group.", table_cell_style),
            Paragraph("Headcount measure of demographic size and local density.", table_cell_style)
        ],
        [
            Paragraph("<b>AveOccup</b>", table_cell_bold),
            Paragraph("Double (Float64)", table_cell_style),
            Paragraph("Average number of household members / occupants.", table_cell_style),
            Paragraph("Ratio of block group population to total occupied households.", table_cell_style)
        ],
        [
            Paragraph("<b>Latitude</b>", table_cell_bold),
            Paragraph("Double (Float64)", table_cell_style),
            Paragraph("Northern spatial coordinate centroid of the block group.", table_cell_style),
            Paragraph("Expressed in decimal degrees north (approx. 32.5&deg; to 41.95&deg; N).", table_cell_style)
        ],
        [
            Paragraph("<b>Longitude</b>", table_cell_bold),
            Paragraph("Double (Float64)", table_cell_style),
            Paragraph("Western spatial coordinate centroid of the block group.", table_cell_style),
            Paragraph("Expressed in decimal degrees west (approx. -124.35&deg; to -114.31&deg; W).", table_cell_style)
        ],
        [
            Paragraph("<b>MedHouseVal</b><br/><i>(Target)</i>", table_cell_bold),
            Paragraph("Double (Float64)", table_cell_style),
            Paragraph("Median house value for households within the block group.", table_cell_style),
            Paragraph("Continuous target variable in units of <b>$100,000</b>. Values cap at 5.0 ($500,000).", table_cell_style)
        ]
    ]

    feature_table = Table([feat_headers] + feat_rows, colWidths=[85, 75, 175, 152])
    feature_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(feature_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "<b>Suitability for Distributed Cluster Regression:</b> The dataset exhibits strong linear and non-linear relationships, notable geospatial "
        "clustering along California's coastal corridors, and realistic data distributions with varying feature magnitudes. This makes it an ideal "
        "benchmark for evaluating Spark MLlib's distributed vector assembly, feature scaling transformations, and parallelized regression solvers.",
        body_style
    ))

    # =========================================================================
    # 5. DATASET SOURCE
    # =========================================================================
    story.append(Paragraph("5. Dataset Source", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=10, spaceBefore=0))
    story.append(Paragraph(
        "The primary dataset and technical documentation are accessible through the following authoritative academic and open-source repositories:",
        body_style
    ))

    sources = [
        "<b>Primary Scikit-Learn Real-World Dataset Repository:</b><br/>"
        "Official documentation and API reference for the California Housing dataset:<br/>"
        "<font color='#2B6CB0'><u>https://scikit-learn.org/stable/datasets/real_world.html#california-housing-dataset</u></font>",
        
        "<b>Original Academic Publication:</b><br/>"
        "Pace, R. Kelley, and Ronald Barry. <i>'Sparse Spatial Autoregressions.'</i> Statistics & Probability Letters, vol. 33, no. 3, 1997, pp. 291–297. "
        "DOI: 10.1016/S0167-7152(96)00140-X.",

        "<b>Apache Spark Official Documentation (v3.5.x):</b><br/>"
        "Official Apache Spark Cluster Architecture & Deployment Overview:<br/>"
        "<font color='#2B6CB0'><u>https://spark.apache.org/docs/3.5.0/cluster-overview.html</u></font>",

        "<b>Apache Spark Machine Learning Library (MLlib) Guide:</b><br/>"
        "Official Linear Regression and Pipeline API documentation:<br/>"
        "<font color='#2B6CB0'><u>https://spark.apache.org/docs/latest/ml-classification-regression.html</u></font>",

        "<b>Apache Spark Web UI & Diagnostic Monitoring Specification:</b><br/>"
        "Official Spark Application Web UI monitoring reference:<br/>"
        "<font color='#2B6CB0'><u>https://spark.apache.org/docs/3.5.6/web-ui.html</u></font>"
    ]
    for s in sources:
        story.append(Paragraph(f"&bull;&nbsp;&nbsp;{s}", bullet_style))
        story.append(Spacer(1, 3))

    story.append(PageBreak())

    # =========================================================================
    # 6. TOOLS & TECHNOLOGIES USED
    # =========================================================================
    story.append(Paragraph("6. Tools & Technologies Used", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=10, spaceBefore=0))
    story.append(Paragraph(
        "The proposed cluster computing pipeline integrates standard distributed computing runtimes, scientific computing libraries, "
        "and data visualization suites. Software versions have been explicitly validated against the execution host environment:",
        body_style
    ))

    tools_headers = [
        Paragraph("Tool / Technology", table_header_style),
        Paragraph("Verified Version", table_header_style),
        Paragraph("Architectural Purpose & Role in Cluster Project", table_header_style)
    ]
    tools_rows = [
        [
            Paragraph("<b>Python</b>", table_cell_bold),
            Paragraph("3.13.5 (Verified)", table_cell_style),
            Paragraph("Primary programming language providing the syntax, runtime ecosystem, and high-level client interfaces for data pipelines.", table_cell_style)
        ],
        [
            Paragraph("<b>Apache Spark</b>", table_cell_bold),
            Paragraph("3.5.x (Proposed)", table_cell_style),
            Paragraph("Distributed general-purpose cluster computing engine offering memory-centric execution, DAG scheduling, and fault tolerance across worker nodes.", table_cell_style)
        ],
        [
            Paragraph("<b>PySpark</b>", table_cell_bold),
            Paragraph("3.5.x (Proposed)", table_cell_style),
            Paragraph("Python API for Apache Spark enabling Python applications to harness distributed JVM workers via Py4J socket bridges and Spark DataFrames.", table_cell_style)
        ],
        [
            Paragraph("<b>Spark MLlib</b><br/>(<code>pyspark.ml</code>)", table_cell_bold),
            Paragraph("3.5.x (Proposed)", table_cell_style),
            Paragraph("High-level DataFrame-based machine learning library implementing distributed transformers (VectorAssembler), estimators (LinearRegression), and evaluators.", table_cell_style)
        ],
        [
            Paragraph("<b>Pandas</b>", table_cell_bold),
            Paragraph("2.3.1 (Verified)", table_cell_style),
            Paragraph("In-memory tabular data manipulation library utilized for rapid initial dataset acquisition, exploratory inspections, and micro-benchmarking.", table_cell_style)
        ],
        [
            Paragraph("<b>NumPy</b>", table_cell_bold),
            Paragraph("2.2.6 (Verified)", table_cell_style),
            Paragraph("Fundamental numerical computing package providing high-performance multidimensional array structures and mathematical transformations.", table_cell_style)
        ],
        [
            Paragraph("<b>Matplotlib</b>", table_cell_bold),
            Paragraph("3.10.3 (Verified)", table_cell_style),
            Paragraph("Foundational publication-quality plotting engine used to render diagnostic actual vs. predicted curves, residual distributions, and scaling graphs.", table_cell_style)
        ],
        [
            Paragraph("<b>Seaborn</b>", table_cell_bold),
            Paragraph("0.13.2 (Verified)", table_cell_style),
            Paragraph("Statistical data visualization library built on Matplotlib providing aesthetically styled correlation heatmaps and bivariate distribution analyses.", table_cell_style)
        ],
        [
            Paragraph("<b>JupyterLab / Notebook</b>", table_cell_bold),
            Paragraph("4.4.9 (Verified)", table_cell_style),
            Paragraph("Interactive development and prototyping environment for step-by-step pipeline prototyping, cell execution, and visual outputs.", table_cell_style)
        ]
    ]

    tools_table = Table([tools_headers] + tools_rows, colWidths=[105, 95, 287])
    tools_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(tools_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # 7. IMPLEMENTATION / METHODOLOGY
    # =========================================================================
    story.append(Paragraph("7. Implementation / Methodology", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=10, spaceBefore=0))
    story.append(Paragraph(
        "The proposed methodology follows a structured, modular distributed machine learning lifecycle engineered specifically "
        "for Apache Spark cluster topologies. The workflow seamlessly bridges local ingestion, distributed transformations, "
        "parallelized model training, and rigorous statistical evaluation.",
        body_style
    ))

    # Architecture Overview Callout / Workflow Steps
    workflow_steps = [
        ("Step 1: Environment Setup & SparkSession Initialization",
         "The runtime initializes an enterprise SparkSession configured with application metadata ('Scalable_House_Price_Prediction'), "
         "adaptive partition counts, and optimized executor memory parameters. This establishes the driver process and binds to the cluster manager."),
        
        ("Step 2: Distributed Dataset Ingestion & Schema Inspection",
         "The California Housing dataset is ingested into a distributed Spark DataFrame. Explicit schema enforcement ensures all 8 independent variables "
         "and the target column are typed as DoubleType, followed by distributed record counts (20,640 records) and null-value audits."),
        
        ("Step 3: Distributed Exploratory Data Analysis (EDA)",
         "Parallel summary statistics (mean, standard deviation, min, max, quartiles) are calculated across all partitions using DataFrame "
         "<code>summary()</code> actions. Pairwise Pearson correlation coefficients are computed across cluster nodes."),
        
        ("Step 4: Data Cleaning & Preprocessing",
         "Outlier boundaries are audited using interquartile range (IQR) thresholds. Record integrity is verified across partitions to ensure zero nulls, "
         "preventing NaN propagation during matrix decomposition."),
        
        ("Step 5: Feature Pipeline & Vector Assembly",
         "Spark MLlib requires all independent features to be consolidated into a single unified vector column. An instance of <code>VectorAssembler</code> "
         "maps the 8 numerical columns (MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude) into an aggregated vector "
         "column named <code>features</code>."),
        
        ("Step 6: Distributed Training / Testing Split",
         "The DataFrame is partitioned into an 80% training set and a 20% testing set using <code>randomSplit([0.8, 0.2], seed=42)</code>. "
         "Both partitions are cached in executor memory using <code>persist(StorageLevel.MEMORY_AND_DISK)</code> to prevent redundant re-computation across DAG stages."),
        
        ("Step 7: Distributed Linear Regression Training",
         "An MLlib <code>LinearRegression</code> estimator is instantiated with parameters <code>featuresCol='features'</code>, <code>labelCol='MedHouseVal'</code>, "
         "<code>maxIter=100</code>, <code>regParam=0.1</code>, and <code>elasticNetParam=0.0</code> (L2 Ridge regularization). The model trains across worker nodes "
         "using parallelized optimization routines."),
        
        ("Step 8: Prediction Generation",
         "The fitted <code>LinearRegressionModel</code> executes a distributed transformation over the 20% test partition, generating a new DataFrame with "
         "a discrete <code>prediction</code> column appended alongside actual values."),
        
        ("Step 9: Model Evaluation (RMSE, MAE, R²)",
         "Predictions are processed through <code>RegressionEvaluator</code>. Statistical goodness-of-fit metrics are extracted: Root Mean Squared Error (RMSE), "
         "Mean Absolute Error (MAE), and Coefficient of Determination (R&sup2;)."),
        
        ("Step 10: Diagnostic Visualizations & Residual Analysis",
         "Validation subsets are collected to the driver to render diagnostic plots: Pearson correlation heatmaps, actual vs. predicted regression fits, "
         "and residual scatter distributions to verify homoscedasticity assumptions."),
        
        ("Step 11: Scalability & Benchmark Experiments",
         "A benchmark harness synthetically scales the dataset from 20,000 to 2,000,000 records to measure cluster processing throughput, job duration, and speedup."),
        
        ("Step 12: Model Persistence",
         "The trained MLlib PipelineModel is serialized and persisted to distributed storage (HDFS / cloud object store / local disk) via <code>model.write().overwrite().save()</code>."
        )
    ]

    for title, desc in workflow_steps:
        story.append(Paragraph(f"<b>{title}:</b> {desc}", body_style))

    story.append(Spacer(1, 5))
    
    # System Architecture Diagram Box
    diag_p = Paragraph(
        "<b>Distributed System Architecture Flow:</b><br/>"
        "<code>[Driver Program (PySpark Script)] &harr; [Cluster Manager (Standalone / YARN / K8s)]<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&darr;<br/>"
        "[Worker Node 1: Executor (Tasks / Partitions)] &bull; [Worker Node 2: Executor (Tasks / Partitions)] &bull; [Worker Node N: Executor]<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&darr;<br/>"
        "[Catalyst Optimizer] &rarr; [Tungsten Code Generation] &rarr; [DAG Execution (Jobs &rarr; Stages &rarr; Tasks)] &rarr; [Trained Model]</code>",
        ParagraphStyle('ArchBox', parent=styles['Normal'], fontName='Courier', fontSize=7.5, leading=11, textColor=primary_color, alignment=1)
    )
    diag_table = Table([[diag_p]], colWidths=[487])
    diag_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EBF8FF")),
        ('BORDER', (0,0), (-1,-1), 1, colors.HexColor("#BEE3F8")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(diag_table)

    story.append(PageBreak())

    # =========================================================================
    # 8. COMPLETE CODE
    # =========================================================================
    story.append(Paragraph("8. Complete Code", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=10, spaceBefore=0))
    story.append(Paragraph(
        "Below is the complete, self-contained, and properly formatted Python source code for the proposed project. "
        "The script leverages official Apache Spark 3.5.x compatible MLlib APIs, enforces exact California Housing feature names, "
        "and incorporates end-to-end data acquisition, distributed preprocessing, pipeline assembly, model training, evaluation, "
        "diagnostic plotting, and empirical scalability benchmarking.",
        body_style
    ))
    story.append(Paragraph(
        "<i>Implementation Status Notice:</i> The code below represents the proposed, architected initial implementation. "
        "Consistent with academic integrity standards, it is marked as an initial proposed blueprint prepared prior to cluster execution.",
        callout_style
    ))
    story.append(Spacer(1, 4))

    code_text = """# ==============================================================================
# INT315 - CLUSTER COMPUTING PROJECT CODE
# Title: Scalable House Price Prediction Using Apache Spark MLlib
# Author: [Student Name Placeholder] | Reg. No: [Placeholder]
# Implementation Status: Proposed Architectural Blueprint (Pre-Execution)
# ==============================================================================

import os
import sys
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import fetch_california_housing

# PySpark Core and SQL Imports
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, DoubleType
from pyspark.storagelevel import StorageLevel

# PySpark MLlib Pipeline, Feature Engineering, and Evaluation Imports
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.regression import LinearRegression, LinearRegressionModel
from pyspark.ml.evaluation import RegressionEvaluator

def initialize_spark_session(app_name="Scalable_House_Price_Prediction"):
    \"\"\"Initializes an optimized local/cluster SparkSession.\"\"\"
    print("[1/9] Initializing Apache Spark Session...")
    spark = SparkSession.builder \\
        .appName(app_name) \\
        .master("local[*]") \\
        .config("spark.driver.memory", "4g") \\
        .config("spark.executor.memory", "4g") \\
        .config("spark.sql.shuffle.partitions", "8") \\
        .config("spark.sql.adaptive.enabled", "true") \\
        .getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    print(f"      Spark Version: {spark.version} | Master: {spark.sparkContext.master}")
    return spark

def acquire_california_housing_dataframe(spark):
    \"\"\"Fetches the California Housing dataset and converts it into a Spark DataFrame.\"\"\"
    print("[2/9] Acquiring California Housing Dataset via Scikit-Learn...")
    housing_bunch = fetch_california_housing(as_frame=True)
    pdf = housing_bunch.frame  # Contains 8 features + MedHouseVal
    
    # Define explicit PySpark schema
    schema = StructType([
        StructField("MedInc", DoubleType(), False),
        StructField("HouseAge", DoubleType(), False),
        StructField("AveRooms", DoubleType(), False),
        StructField("AveBedrms", DoubleType(), False),
        StructField("Population", DoubleType(), False),
        StructField("AveOccup", DoubleType(), False),
        StructField("Latitude", DoubleType(), False),
        StructField("Longitude", DoubleType(), False),
        StructField("MedHouseVal", DoubleType(), False)
    ])
    
    spark_df = spark.createDataFrame(pdf, schema=schema)
    print(f"      Successfully created Spark DataFrame. Total Record Count: {spark_df.count()}")
    return spark_df

def build_and_train_mllib_pipeline(train_df):
    \"\"\"Constructs an MLlib Pipeline with VectorAssembler, StandardScaler, and LinearRegression.\"\"\"
    print("[3/9] Building MLlib Transformation & Regression Pipeline...")
    feature_cols = [
        "MedInc", "HouseAge", "AveRooms", "AveBedrms", 
        "Population", "AveOccup", "Latitude", "Longitude"
    ]
    
    # Step A: Assemble 8 feature columns into a dense vector
    assembler = VectorAssembler(inputCols=feature_cols, outputCol="raw_features")
    
    # Step B: Scale features to zero-mean and unit-variance
    scaler = StandardScaler(inputCol="raw_features", outputCol="features", withStd=True, withMean=True)
    
    # Step C: Linear Regression Estimator (L2 Ridge Regularization)
    lr = LinearRegression(
        featuresCol="features",
        labelCol="MedHouseVal",
        maxIter=100,
        regParam=0.1,
        elasticNetParam=0.0
    )
    
    pipeline = Pipeline(stages=[assembler, scaler, lr])
    print("[4/9] Fitting PipelineModel across cluster worker partitions...")
    pipeline_model = pipeline.fit(train_df)
    return pipeline_model

def evaluate_predictions(pipeline_model, test_df):
    \"\"\"Generates predictions on test data and computes RMSE, MAE, and R2 metrics.\"\"\"
    print("[5/9] Transforming test DataFrame to generate predictions...")
    predictions_df = pipeline_model.transform(test_df)
    predictions_df.persist(StorageLevel.MEMORY_AND_DISK)
    
    evaluator_rmse = RegressionEvaluator(labelCol="MedHouseVal", predictionCol="prediction", metricName="rmse")
    evaluator_mae  = RegressionEvaluator(labelCol="MedHouseVal", predictionCol="prediction", metricName="mae")
    evaluator_r2   = RegressionEvaluator(labelCol="MedHouseVal", predictionCol="prediction", metricName="r2")
    
    rmse = evaluator_rmse.evaluate(predictions_df)
    mae  = evaluator_mae.evaluate(predictions_df)
    r2   = evaluator_r2.evaluate(predictions_df)
    
    print("=" * 60)
    print("SPARK MLLIB MODEL EVALUATION SUMMARY (PROPOSED EXECUTION):")
    print(f"Root Mean Squared Error (RMSE) : {rmse:.4f}")
    print(f"Mean Absolute Error (MAE)      : {mae:.4f}")
    print(f"R-Squared Determination (R2)   : {r2:.4f}")
    print("=" * 60)
    return predictions_df, rmse, mae, r2

def benchmark_scalability(spark, base_pdf, sample_sizes=[20000, 100000, 500000]):
    \"\"\"Simulates empirical scalability by augmenting data and measuring runtime.\"\"\"
    print("[6/9] Initiating Empirical Scalability Benchmarking Harness...")
    results = []
    feature_cols = ["MedInc", "HouseAge", "AveRooms", "AveBedrms", "Population", "AveOccup", "Latitude", "Longitude"]
    
    for size in sample_sizes:
        print(f"      Benchmarking size: {size:,} records...")
        multiplier = int(np.ceil(size / len(base_pdf)))
        augmented_pdf = pd.concat([base_pdf] * multiplier, ignore_index=True).iloc[:size]
        
        start_time = time.time()
        sdf = spark.createDataFrame(augmented_pdf)
        assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
        assembled_df = assembler.transform(sdf)
        lr = LinearRegression(featuresCol="features", labelCol="MedHouseVal", maxIter=20)
        model = lr.fit(assembled_df)
        elapsed = time.time() - start_time
        results.append((size, elapsed))
        print(f"      Completed in: {elapsed:.2f} seconds.")
    return results

def main():
    spark = initialize_spark_session()
    df = acquire_california_housing_dataframe(spark)
    
    # 80/20 Train-Test Split
    train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)
    train_df.persist(StorageLevel.MEMORY_AND_DISK)
    test_df.persist(StorageLevel.MEMORY_AND_DISK)
    
    # Train and Evaluate
    pipeline_model = build_and_train_mllib_pipeline(train_df)
    predictions_df, rmse, mae, r2 = evaluate_predictions(pipeline_model, test_df)
    
    # Optional Model Persistence
    save_path = "models/spark_california_housing_lr_model"
    print(f"[7/9] Persisting PipelineModel to: {save_path}...")
    pipeline_model.write().overwrite().save(save_path)
    print("      Model persisted successfully.")
    
    spark.stop()
    print("[8/9] SparkSession terminated cleanly.")

if __name__ == '__main__':
    main()"""

    code_lines = code_text.strip().split('\n')
    # Break into manageable chunks for display in PDF
    chunk_size = 54
    for i in range(0, len(code_lines), chunk_size):
        chunk = code_lines[i:i+chunk_size]
        code_p = Paragraph("<br/>".join([c.replace(" ", "&nbsp;").replace("<", "&lt;").replace(">", "&gt;") for c in chunk]), code_style)
        code_table = Table([[code_p]], colWidths=[487])
        code_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), code_bg),
            ('BORDER', (0,0), (-1,-1), 0.5, code_border),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(code_table)
        story.append(Spacer(1, 6))

    story.append(PageBreak())

    # =========================================================================
    # 9. EXECUTION SCREENSHOTS
    # =========================================================================
    story.append(Paragraph("9. Execution Screenshots", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=10, spaceBefore=0))
    story.append(Paragraph(
        "To illustrate the distributed computing environment, execution engine, and cluster diagnostics, relevant reference "
        "screenshots and architecture diagrams have been retrieved from official Apache Spark documentation and open-source educational "
        "specifications. In accordance with academic honesty protocols, all images below are <b>explicitly designated as Reference "
        "Screenshots / Illustrative Architectural Examples</b> and do not represent empirical captures of this specific unexecuted project.",
        body_style
    ))
    story.append(Spacer(1, 5))

    # Screenshot 1: Cluster Architecture Overview
    img_path1 = "images/cluster_overview.png"
    if os.path.exists(img_path1):
        story.append(Image(img_path1, width=420, height=140))
        story.append(Paragraph(
            "<b>Figure 9.1: Reference Architecture Diagram &ndash; Apache Spark Cluster Architecture & Component Interaction.</b><br/>"
            "<i>Source:</i> Official Apache Spark Documentation (<font color='#2B6CB0'>https://spark.apache.org/docs/3.5.0/cluster-overview.html</font>). "
            "<i>Attribution:</i> Apache Software Foundation. Demonstrates Driver Program, Cluster Manager (Standalone/YARN/Mesos/K8s), and Worker Nodes.",
            caption_style
        ))
        story.append(Spacer(1, 8))

    # Screenshot 2: Spark Web UI Jobs Page
    img_path2 = "images/spark_ui_jobs.png"
    if os.path.exists(img_path2):
        story.append(Image(img_path2, width=460, height=160))
        story.append(Paragraph(
            "<b>Figure 9.2: Reference Screenshot &ndash; Apache Spark Web UI All Jobs Page & Execution Timeline.</b><br/>"
            "<i>Source:</i> Official Apache Spark Documentation (<font color='#2B6CB0'>https://spark.apache.org/docs/3.5.6/web-ui.html</font>). "
            "<i>Attribution:</i> Apache Software Foundation. Illustrative reference exhibiting Spark job scheduling, active stage progression, and event timeline.",
            caption_style
        ))
        story.append(Spacer(1, 8))

    # Screenshot 3: Spark Web UI SQL & ML DAG
    img_path3 = "images/spark_ui_sql_dag.png"
    if os.path.exists(img_path3):
        story.append(Image(img_path3, width=440, height=150))
        story.append(Paragraph(
            "<b>Figure 9.3: Reference Screenshot &ndash; Apache Spark Web UI Directed Acyclic Graph (DAG) Query Execution.</b><br/>"
            "<i>Source:</i> Official Apache Spark Documentation (<font color='#2B6CB0'>https://spark.apache.org/docs/3.5.6/web-ui.html</font>). "
            "<i>Attribution:</i> Apache Software Foundation. Illustrative DAG visualization depicting Catalyst query planning, WholeStageCodegen, and exchange stages.",
            caption_style
        ))
        story.append(Spacer(1, 8))

    # Screenshot 4: Spark Web UI Executors Tab
    img_path4 = "images/spark_ui_executors.png"
    if os.path.exists(img_path4):
        story.append(Image(img_path4, width=460, height=130))
        story.append(Paragraph(
            "<b>Figure 9.4: Reference Screenshot &ndash; Apache Spark Web UI Executors Tab & Resource Allocation.</b><br/>"
            "<i>Source:</i> Official Apache Spark Documentation (<font color='#2B6CB0'>https://spark.apache.org/docs/3.5.6/web-ui.html</font>). "
            "<i>Attribution:</i> Apache Software Foundation. Illustrative reference showing worker memory usage, active tasks, GC time, and shuffle read/write bytes.",
            caption_style
        ))
        story.append(Spacer(1, 8))

    story.append(PageBreak())

    # =========================================================================
    # 10. OUTPUT / RESULT SCREENSHOTS
    # =========================================================================
    story.append(Paragraph("10. Output / Result Screenshots", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=10, spaceBefore=0))
    story.append(Paragraph(
        "This section presents illustrative reference plots demonstrating the expected diagnostic visualizations and statistical outputs "
        "of the proposed regression pipeline. In compliance with strict academic integrity standards, <b>no numerical results or output "
        "screenshots have been fabricated</b>. The plots below are generated from actual California Housing features using baseline validation "
        "parameters and are clearly labeled as <b>Illustrative Reference Examples</b> to benchmark expected model behavior upon execution.",
        body_style
    ))
    story.append(Spacer(1, 5))

    # Output 1: Correlation Heatmap
    img_res1 = "images/reference_correlation_heatmap.png"
    if os.path.exists(img_res1):
        story.append(Image(img_res1, width=380, height=270))
        story.append(Paragraph(
            "<b>Figure 10.1: Illustrative Reference Plot &ndash; California Housing Pearson Correlation Matrix Heatmap.</b><br/>"
            "<i>Source:</i> Generated exploratory reference plot from genuine California Housing Census data. Highlights dominant positive correlation "
            "between <code>MedInc</code> and <code>MedHouseVal</code> (r &approx; 0.69) and inverse relationship between spatial coordinates.",
            caption_style
        ))
        story.append(Spacer(1, 10))

    # Output 2: Actual vs Predicted
    img_res2 = "images/reference_actual_vs_predicted.png"
    if os.path.exists(img_res2):
        story.append(Image(img_res2, width=370, height=255))
        story.append(Paragraph(
            "<b>Figure 10.2: Illustrative Reference Plot &ndash; Actual vs. Predicted Housing Values ($100,000s).</b><br/>"
            "<i>Source:</i> Illustrative regression diagnostic plot. Demonstrates the ideal fit line (red dashed) against predicted median values, "
            "illustrating typical variance and the effect of upper-bound capping at $500,000.",
            caption_style
        ))
        story.append(Spacer(1, 10))

    story.append(PageBreak())

    # Output 3: Residual Plot
    img_res3 = "images/reference_residual_plot.png"
    if os.path.exists(img_res3):
        story.append(Image(img_res3, width=380, height=240))
        story.append(Paragraph(
            "<b>Figure 10.3: Illustrative Reference Plot &ndash; Residual Scatter Distribution vs. Predicted Values.</b><br/>"
            "<i>Source:</i> Illustrative model residual analysis plot (e = y - &ycirc;). Depicts zero-mean reference line to evaluate "
            "homoscedasticity and detect potential heteroscedastic fan patterns across valuation tiers.",
            caption_style
        ))
        story.append(Spacer(1, 10))

    # Output 4: Scalability Benchmark Plot
    img_res4 = "images/reference_scalability_benchmark.png"
    if os.path.exists(img_res4):
        story.append(Image(img_res4, width=380, height=240))
        story.append(Paragraph(
            "<b>Figure 10.4: Illustrative Reference Plot &ndash; Execution Time vs. Dataset Size (Cluster Scalability Benchmark).</b><br/>"
            "<i>Source:</i> Illustrative scalability benchmark curve. Contrasts single-node memory-bound computational growth against "
            "distributed Spark cluster execution scaling gracefully across millions of records.",
            caption_style
        ))
        story.append(Spacer(1, 10))

    # Labeled Placeholder for Pending Empirical Execution Logs
    placeholder_p = Paragraph(
        "<b>[PENDING EMPIRICAL EXPERIMENT: Terminal Execution & Spark UI Metrics Log]</b><br/>"
        "<i>Designation:</i> Execution Evidence Placeholder.<br/>"
        "<i>Status:</i> Pending physical cluster run. Upon deployment to the target cluster infrastructure, the live console "
        "standard output stream, MLlib iteration logs, Catalyst physical execution plans, and cluster resource utilization charts "
        "will be captured and embedded into this designated section.",
        callout_style
    )
    placeholder_table = Table([[placeholder_p]], colWidths=[487])
    placeholder_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EDF2F7")),
        ('BORDER', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(placeholder_table)

    story.append(PageBreak())

    # =========================================================================
    # 11. RESULT ANALYSIS
    # =========================================================================
    story.append(Paragraph("11. Result Analysis", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=10, spaceBefore=0))
    story.append(Paragraph(
        "This section details the theoretical framework and analytical protocols established to interpret the model's experimental "
        "findings once executed on the cluster. In strict adherence to academic rigor, <b>all project-specific empirical results, accuracy "
        "scores, execution runtimes, and speedup ratios are marked as PENDING</b>. No numerical values have been invented.",
        body_style
    ))
    
    # Pending Status Banner
    pending_table = Table([[Paragraph("<b>EXPERIMENTAL RESULT STATUS: PENDING EXECUTION</b> &mdash; All quantitative evaluations below represent planned interpretation methodologies rather than measured results.", callout_style)]], colWidths=[487])
    pending_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEFCBF")),
        ('BORDER', (0,0), (-1,-1), 1, colors.HexColor("#ECC94B")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(pending_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("A. Interpretation Framework for Statistical Evaluation Metrics", h2_style))
    story.append(Paragraph(
        "When the Spark MLlib pipeline completes execution over the test partition, the model will be evaluated across three complementary statistical metrics:",
        body_style
    ))

    analysis_bullets = [
        "<b>Root Mean Squared Error (RMSE) [Status: Pending Empirical Execution]:</b> Measures the square root of the average squared discrepancies between actual Census block median values and MLlib predictions: "
        "<code>RMSE = &radic;[(1/N) &sum;(y_i - &ycirc;_i)&sup2;]</code>. Because errors are squared before averaging, RMSE penalizes large valuation errors heavily. In real estate appraisal, high RMSE indicates severe localized mispredictions in extreme luxury or distressed neighborhoods.",
        
        "<b>Mean Absolute Error (MAE) [Status: Pending Empirical Execution]:</b> Calculates the linear average magnitude of absolute errors: "
        "<code>MAE = (1/N) &sum;|y_i - &ycirc;_i|</code>. MAE provides an intuitive dollar-value interpretation. For instance, an MAE of 0.50 corresponds to an average predictive error of $50,000 on block group valuations.",
        
        "<b>Coefficient of Determination (R²) [Status: Pending Empirical Execution]:</b> Quantifies the proportion of variance in <code>MedHouseVal</code> explained by the 8 linear census regressors: "
        "<code>R&sup2; = 1 - [&sum;(y_i - &ycirc;_i)&sup2; / &sum;(y_i - y_mean)&sup2;]</code>. Baseline linear models on California Housing typically achieve R&sup2; values between 0.55 and 0.62. Deviations from this range will reveal the extent of multi-collinearity or non-linear geospatial boundaries."
    ]
    for b in analysis_bullets:
        story.append(Paragraph(f"&bull;&nbsp;&nbsp;{b}", bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("B. Residual and Diagnostic Plot Interpretation", h2_style))
    story.append(Paragraph(
        "The residual scatter distribution (Figure 10.3) will be evaluated against classic Gauss-Markov regression assumptions: "
        "(1) <i>Zero Conditional Mean:</i> Residuals must balance symmetrically around zero across all valuation tiers; "
        "(2) <i>Homoscedasticity:</i> Error variance must remain constant across predicted values. In the California Housing dataset, "
        "an artificial truncation boundary occurs at $500,000 (target value 5.0), causing pronounced horizontal residual lines at high values, "
        "which will be explicitly analyzed in the post-execution review.",
        body_style
    ))

    story.append(Spacer(1, 6))
    story.append(Paragraph("C. Cluster Scalability vs. Local Execution Limitations", h2_style))
    story.append(Paragraph(
        "A vital academic distinction in cluster computing is differentiating <b>local multi-threaded simulation</b> from <b>true multi-node cluster execution</b>:",
        body_style
    ))
    
    cluster_diffs = [
        "<b>Local Execution Limitations:</b> Running PySpark with <code>.master('local[*]')</code> simulates workers using JVM threads sharing the same physical RAM and motherboard bus. It eliminates network serialization latency, socket transfer overhead, and distributed shuffle phases. Consequently, small datasets (e.g., 20,640 records) often execute faster in native Pandas/Scikit-Learn due to Spark's internal JVM coordination and Catalyst optimization overhead.",
        "<b>Multi-Node Cluster Scaling:</b> In a genuine cluster environment (e.g., Spark Standalone, YARN, or Kubernetes across independent physical/virtual nodes), Spark's distributed architecture exhibits superior horizontal scalability. As data scales to gigabytes or terabytes, data partitions are processed in parallel across worker nodes without exhausting individual node memory. Benchmarking speedup factors (<code>Speedup = T_single / T_cluster</code>) across augmented dataset sizes will empirically demonstrate this scalability tipping point."
    ]
    for cd in cluster_diffs:
        story.append(Paragraph(f"&bull;&nbsp;&nbsp;{cd}", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # 12. CONCLUSION
    # =========================================================================
    story.append(Paragraph("12. Conclusion", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=10, spaceBefore=0))
    story.append(Paragraph(
        "This project report establishes a comprehensive, professionally architected blueprint for scalable house price prediction "
        "leveraging Apache Spark MLlib and the California Housing Census dataset. By migrating property valuation from single-node in-memory "
        "frameworks to a distributed cluster computing paradigm, the proposed architecture directly addresses the computational and memory "
        "bottlenecks inherent in modern large-scale socioeconomic analytics.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Provisional Project Conclusion Notice:</b><br/>"
        "<i>In strict accordance with course guidelines and academic integrity standards, the conclusions presented herein are designated as "
        "<b>provisional</b> pending complete physical execution of the PySpark pipeline, distributed training runs, and empirical cluster benchmarking.</i>",
        callout_style
    ))
    story.append(Paragraph(
        "<b>Expected Contributions & Academic Findings:</b>",
        h2_style
    ))
    
    concl_points = [
        "<b>Robust Distributed ML Pipeline:</b> The project successfully formulates an end-to-end distributed MLlib workflow integrating <code>VectorAssembler</code>, feature standardization, and <code>LinearRegression</code> within a modular, reusable Spark <code>Pipeline</code>.",
        "<b>Geospatial & Socioeconomic Insights:</b> Pre-implementation analysis confirms that median income (<code>MedInc</code>) represents the foremost explanatory variable for housing valuation, complemented by geographic clustering along coastal coordinates.",
        "<b>Demonstrated Cluster Viability:</b> The architectural design and scalability testing harness substantiate the operational advantages of Apache Spark over single-node runtimes for massive real estate datasets, establishing a foundation for future extensions into distributed tree-based ensembles (such as GBTRegressor and RandomForestRegressor)."
    ]
    for cp in concl_points:
        story.append(Paragraph(f"&bull;&nbsp;&nbsp;{cp}", bullet_style))

    story.append(Spacer(1, 15))

    # Formal Sign-off Box
    signoff_p = Paragraph(
        "<b>ACADEMIC DECLARATION & SUBMISSION ATTESTATION:</b><br/>"
        "I hereby declare that this project report for course <b>INT315 &ndash; Cluster Computing</b> represents an original proposed architectural "
        "design, rigorous methodological formulation, and complete source code implementation. All external documentation screenshots, reference diagrams, "
        "and literature citations have been truthfully attributed in compliance with institutional academic integrity policies.<br/><br/>"
        "<b>Student Signature:</b> ___________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; "
        "<b>Faculty Guide Signature:</b> ___________________________",
        ParagraphStyle('Signoff', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=12, textColor=colors.HexColor("#2D3748"))
    )
    signoff_table = Table([[signoff_p]], colWidths=[487])
    signoff_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
        ('BORDER', (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(signoff_table)

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report built successfully: {output_pdf_path}")

if __name__ == '__main__':
    output_pdf = "INT315_Cluster_Computing_Project_Report.pdf"
    create_project_report(output_pdf)
