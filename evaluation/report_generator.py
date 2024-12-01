# evaluation/report_generator.py
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os

class ReportGenerator:
    def generate_pdf_report(self, results, pdf_path="results/simulation_report.pdf"):
        """
        Generate a detailed PDF report with simulation results and visualizations.
        
        :param results: Dictionary containing protocol metrics
        :param pdf_path: Output path for the PDF report
        """
        # Create DataFrame
        data = []
        for protocol, metrics in results.items():
            data.append({
                "Protocol": protocol,
                "Encryption Time (s)": metrics.get("Encryption Time (s)", 0),
                "Decryption Time (s)": metrics.get("Decryption Time (s)", 0),
                "Energy Consumption (J)": metrics.get("Energy Consumption (J)", 0),
                "Packet Size (bytes)": metrics.get("Packet Size (bytes)", 0),
                "Network Lifetime (cycles)": metrics.get("Network Lifetime (cycles)", 0)
            })

        df = pd.DataFrame(data)

        # Initialize PDF
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter

        # Title
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(width / 2, height - 50, "WSN Protocol Simulation Report")

        # Introduction
        c.setFont("Helvetica", 12)
        text = c.beginText(50, height - 80)
        intro = "This report presents the simulation results of various secure and energy-efficient protocols implemented for Wireless Sensor Networks (WSNs). The protocols evaluated include OpenWSN and DASH7 integrated with different encryption algorithms: AES, SPECK, PRESENT, and Selective AES."
        for line in intro.splitlines():
            text.textLine(line)
        c.drawText(text)

        # Add Metrics Table
        c.showPage()
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "Simulation Metrics")

        # Create a simple table using ReportLab
        from reportlab.platypus import Table, TableStyle
        from reportlab.lib import colors

        table_data = [df.columns.tolist()] + df.values.tolist()
        table = Table(table_data, repeatRows=1)
        table_style = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
        ])
        table.setStyle(table_style)

        # Position the table
        table_width, table_height = table.wrap(0, 0)
        table.drawOn(c, 50, height - 100 - table_height)

        # Add Visualizations
        c.showPage()
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "Visualizations")

        # List of plots to include
        plot_files = [
            "encryption_time.png",
            "decryption_time.png",
            "energy_consumption.png",
            "packet_size.png",
            "network_longevity.png",
            "energy_vs_encryption_time.png",
            "metrics_heatmap.png"
        ]

        y_position = height - 100
        for plot in plot_files:
            plot_path = os.path.join("results", plot)
            if os.path.exists(plot_path):
                # Resize image to fit the page
                img = ImageReader(plot_path)
                img_width, img_height = img.getSize()
                aspect = img_height / float(img_width)
                img_display_width = width - 100
                img_display_height = img_display_width * aspect
                if y_position - img_display_height < 50:
                    c.showPage()
                    y_position = height - 50
                c.drawImage(plot_path, 50, y_position - img_display_height, width=img_display_width, height=img_display_height)
                y_position -= (img_display_height + 30)

        # Save PDF
        c.save()
        print(f"Report generated at {pdf_path}")
