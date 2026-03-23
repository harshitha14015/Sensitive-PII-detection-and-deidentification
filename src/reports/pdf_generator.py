"""
PDF Report Generation Module
Handles creation of comprehensive PDF reports
"""
import time
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from auth.database import get_ist_time

def generate_accuracy_report_pdf(metrics, pii_detection_summary, username):
    """Generate a comprehensive accuracy report PDF"""
    
    # Calculate comprehensive metrics
    total_samples = metrics['TP'] + metrics['TN'] + metrics['FP'] + metrics['FN']
    accuracy = (metrics['TP'] + metrics['TN']) / total_samples if total_samples > 0 else 0
    precision = metrics['TP'] / (metrics['TP'] + metrics['FP']) if (metrics['TP'] + metrics['FP']) > 0 else 0
    recall = metrics['TP'] / (metrics['TP'] + metrics['FN']) if (metrics['TP'] + metrics['FN']) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    specificity = metrics['TN'] / (metrics['TN'] + metrics['FP']) if (metrics['TN'] + metrics['FP']) > 0 else 0
    error_rate = (metrics['FP'] + metrics['FN']) / total_samples if total_samples > 0 else 0
    
    # Create PDF filename
    accuracy_report_pdf = f"Accuracy_Report_{username}_{int(time.time())}.pdf"
    
    # Create PDF document
    doc = SimpleDocTemplate(accuracy_report_pdf, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []
    
    # Title
    elements.append(Paragraph("PII Detection Accuracy Report", styles["Title"]))
    elements.append(Spacer(1, 12))
    
    # Report metadata
    elements.append(Paragraph(f"Generated for: {username}", styles["Normal"]))
    elements.append(Paragraph(f"Generated on: {get_ist_time()}", styles["Normal"]))
    elements.append(Paragraph(f"Report Type: Accuracy Analysis", styles["Normal"]))
    elements.append(Spacer(1, 20))
    
    # Executive Summary
    elements.append(Paragraph("Executive Summary", styles["Heading2"]))
    elements.append(Paragraph(f"This report provides a comprehensive analysis of PII detection accuracy for the processed dataset. The system analyzed {total_samples:,} data points and achieved an overall accuracy of {accuracy:.2%}.", styles["Normal"]))
    elements.append(Spacer(1, 12))
    
    # Key Metrics Section
    elements.append(Paragraph("Key Performance Metrics", styles["Heading2"]))
    
    # Create metrics table
    metrics_data = [
        ['Metric', 'Value', 'Description'],
        ['Overall Accuracy', f"{accuracy:.2%}", 'Percentage of correct predictions'],
        ['Precision', f"{precision:.2%}", 'True positive rate'],
        ['Recall (Sensitivity)', f"{recall:.2%}", 'Detection rate for actual PII'],
        ['Specificity', f"{specificity:.2%}", 'True negative rate'],
        ['F1-Score', f"{f1_score:.2%}", 'Balanced measure of precision and recall'],
        ['Error Rate', f"{error_rate:.2%}", 'Percentage of incorrect predictions'],
        ['Total Samples', f"{total_samples:,}", 'Total data points analyzed']
    ]
    
    metrics_table = Table(metrics_data, colWidths=[2.5*inch, 1.5*inch, 3*inch])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.1725, 0.2392, 0.3137)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), "LEFT"),
        ('FONTNAME', (0, 0), (-1, 0), "Helvetica-Bold"),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.Color(0.9255, 0.9412, 0.9451)),
        ('FONTNAME', (0, 1), (-1, -1), "Helvetica"),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.Color(0.7412, 0.7647, 0.7804)),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elements.append(metrics_table)
    elements.append(Spacer(1, 20))
    
    # Confusion Matrix Section
    elements.append(Paragraph("Confusion Matrix Analysis", styles["Heading2"]))
    
    confusion_data = [
        ['', 'Predicted PII', 'Predicted Non-PII'],
        ['Actual PII', f"{metrics['TP']}", f"{metrics['FN']}"],
        ['Actual Non-PII', f"{metrics['FP']}", f"{metrics['TN']}"]
    ]
    
    confusion_table = Table(confusion_data, colWidths=[2*inch, 2*inch, 2*inch])
    confusion_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.1725, 0.2392, 0.3137)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), "CENTER"),
        ('FONTNAME', (0, 0), (-1, 0), "Helvetica-Bold"),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.Color(0.9255, 0.9412, 0.9451)),
        ('FONTNAME', (0, 1), (-1, -1), "Helvetica"),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.Color(0.7412, 0.7647, 0.7804)),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elements.append(confusion_table)
    elements.append(Spacer(1, 12))
    
    # Confusion Matrix Explanation
    elements.append(Paragraph("Confusion Matrix Legend:", styles["Heading3"]))
    elements.append(Paragraph(f"• True Positives (TP): {metrics['TP']} - Correctly identified PII instances", styles["Normal"]))
    elements.append(Paragraph(f"• True Negatives (TN): {metrics['TN']} - Correctly identified non-PII instances", styles["Normal"]))
    elements.append(Paragraph(f"• False Positives (FP): {metrics['FP']} - Incorrectly flagged non-PII as PII", styles["Normal"]))
    elements.append(Paragraph(f"• False Negatives (FN): {metrics['FN']} - Missed actual PII instances", styles["Normal"]))
    elements.append(Spacer(1, 20))
    
    # PII Detection Summary
    if pii_detection_summary:
        elements.append(Paragraph("PII Detection Summary", styles["Heading2"]))
        
        total_detections = sum(pii_detection_summary.values())
        elements.append(Paragraph(f"Total PII instances detected: {total_detections}", styles["Normal"]))
        elements.append(Paragraph(f"Columns containing PII: {len(pii_detection_summary)}", styles["Normal"]))
        elements.append(Spacer(1, 12))
        
        # PII Detection by Column Table
        elements.append(Paragraph("PII Detections by Column", styles["Heading3"]))
        
        pii_data = [['Column', 'PII Count']]
        for column, count in sorted(pii_detection_summary.items(), key=lambda x: x[1], reverse=True):
            pii_data.append([column, str(count)])
        
        pii_table = Table(pii_data, colWidths=[4*inch, 2*inch])
        pii_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.1725, 0.2392, 0.3137)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), "LEFT"),
            ('FONTNAME', (0, 0), (-1, 0), "Helvetica-Bold"),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.Color(0.9255, 0.9412, 0.9451)),
            ('FONTNAME', (0, 1), (-1, -1), "Helvetica"),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.Color(0.7412, 0.7647, 0.7804)),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(pii_table)
        elements.append(Spacer(1, 20))
    
    # Performance Analysis
    elements.append(Paragraph("Performance Analysis", styles["Heading2"]))
    
    if accuracy >= 0.95:
        performance_text = "Excellent Performance: The PII detection system is performing exceptionally well with high accuracy across all metrics."
    elif accuracy >= 0.90:
        performance_text = "Very Good Performance: The system is performing well with high accuracy and reliable detection."
    elif accuracy >= 0.85:
        performance_text = "Good Performance: The system is performing adequately with room for minor improvements."
    elif accuracy >= 0.80:
        performance_text = "Satisfactory Performance: The system meets basic requirements but could benefit from optimization."
    else:
        performance_text = "Needs Improvement: The system requires optimization to improve detection accuracy."
    
    elements.append(Paragraph(performance_text, styles["Normal"]))
    elements.append(Spacer(1, 12))
    
    # Recommendations
    elements.append(Paragraph("Recommendations", styles["Heading2"]))
    
    recommendations = []
    
    if precision < 0.80:
        recommendations.append("• Consider refining detection patterns to reduce false positives")
    
    if recall < 0.80:
        recommendations.append("• Improve detection patterns to catch more PII instances")
    
    if f1_score < 0.80:
        recommendations.append("• Balance precision and recall for optimal performance")
    
    if total_samples < 100:
        recommendations.append("• Test with larger datasets for more statistically significant results")
    
    if not recommendations:
        recommendations.append("• Continue monitoring performance with regular testing")
        recommendations.append("• Consider expanding to additional PII types if needed")
    
    for rec in recommendations:
        elements.append(Paragraph(rec, styles["Normal"]))
    
    elements.append(Spacer(1, 20))
    
    # Footer
    elements.append(Paragraph("Report Generated by PII De-Identification Tool", styles["Normal"]))
    elements.append(Paragraph(f"Generated on: {get_ist_time()}", styles["Normal"]))
    
    # Build PDF
    doc.build(elements)
    
    return accuracy_report_pdf
