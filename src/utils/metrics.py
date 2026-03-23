"""
Accuracy Metrics Calculation Module
"""

def compute_accuracy(metrics):
    """Compute comprehensive accuracy metrics for PII detection"""
    accuracy_summary = {}
    
    for key, m in metrics.items():
        total = m["TP"] + m["TN"] + m["FP"] + m["FN"]
        
        if total == 0:
            accuracy_summary[key] = {
                "accuracy": 0.0,
                "precision": 0.0,
                "recall": 0.0,
                "f1_score": 0.0,
                "specificity": 0.0,
                "total_samples": 0
            }
            continue
        
        # Basic accuracy
        accuracy = (m["TP"] + m["TN"]) / total * 100
        
        # Precision: TP / (TP + FP)
        precision = (m["TP"] / (m["TP"] + m["FP"]) * 100) if (m["TP"] + m["FP"]) > 0 else 0
        
        # Recall (Sensitivity): TP / (TP + FN)
        recall = (m["TP"] / (m["TP"] + m["FN"]) * 100) if (m["TP"] + m["FN"]) > 0 else 0
        
        # F1 Score: 2 * (precision * recall) / (precision + recall)
        f1_score = (2 * (precision * recall) / (precision + recall)) if (precision + recall) > 0 else 0
        
        # Specificity: TN / (TN + FP)
        specificity = (m["TN"] / (m["TN"] + m["FP"]) * 100) if (m["TN"] + m["FP"]) > 0 else 0
        
        accuracy_summary[key] = {
            "accuracy": round(accuracy, 2),
            "precision": round(precision, 2),
            "recall": round(recall, 2),
            "f1_score": round(f1_score, 2),
            "specificity": round(specificity, 2),
            "total_samples": total,
            "tp": m["TP"],
            "tn": m["TN"],
            "fp": m["FP"],
            "fn": m["FN"]
        }
    
    return accuracy_summary

def compute_overall_accuracy(metrics):
    """Compute overall system accuracy across all PII types"""
    total_tp = sum(m["TP"] for m in metrics.values())
    total_tn = sum(m["TN"] for m in metrics.values())
    total_fp = sum(m["FP"] for m in metrics.values())
    total_fn = sum(m["FN"] for m in metrics.values())
    
    total_samples = total_tp + total_tn + total_fp + total_fn
    
    if total_samples == 0:
        return {
            "overall_accuracy": 0.0,
            "overall_precision": 0.0,
            "overall_recall": 0.0,
            "overall_f1_score": 0.0,
            "overall_specificity": 0.0,
            "total_samples": 0
        }
    
    # Overall metrics
    overall_accuracy = (total_tp + total_tn) / total_samples * 100
    overall_precision = (total_tp / (total_tp + total_fp) * 100) if (total_tp + total_fp) > 0 else 0
    overall_recall = (total_tp / (total_tp + total_fn) * 100) if (total_tp + total_fn) > 0 else 0
    overall_f1_score = (2 * (overall_precision * overall_recall) / (overall_precision + overall_recall)) if (overall_precision + overall_recall) > 0 else 0
    overall_specificity = (total_tn / (total_tn + total_fp) * 100) if (total_tn + total_fp) > 0 else 0
    
    return {
        "overall_accuracy": round(overall_accuracy, 2),
        "overall_precision": round(overall_precision, 2),
        "overall_recall": round(overall_recall, 2),
        "overall_f1_score": round(overall_f1_score, 2),
        "overall_specificity": round(overall_specificity, 2),
        "total_samples": total_samples,
        "total_tp": total_tp,
        "total_tn": total_tn,
        "total_fp": total_fp,
        "total_fn": total_fn
    }

def get_accuracy_grade(accuracy_score):
    """Convert accuracy score to letter grade"""
    if accuracy_score >= 95:
        return "A+ (Excellent)"
    elif accuracy_score >= 90:
        return "A (Very Good)"
    elif accuracy_score >= 85:
        return "B+ (Good)"
    elif accuracy_score >= 80:
        return "B (Satisfactory)"
    elif accuracy_score >= 75:
        return "C+ (Average)"
    elif accuracy_score >= 70:
        return "C (Below Average)"
    elif accuracy_score >= 60:
        return "D (Poor)"
    else:
        return "F (Fail)"

def analyze_accuracy_trends(accuracy_data):
    """Analyze accuracy trends and provide insights"""
    insights = []
    
    # Find best performing PII type
    best_pii = max(accuracy_data.items(), key=lambda x: x[1]["accuracy"])
    insights.append(f"Best performing PII type: {best_pii[0]} ({best_pii[1]['accuracy']}% accuracy)")
    
    # Find worst performing PII type
    worst_pii = min(accuracy_data.items(), key=lambda x: x[1]["accuracy"])
    insights.append(f"Needs improvement: {worst_pii[0]} ({worst_pii[1]['accuracy']}% accuracy)")
    
    # Check for high false positive rates
    high_fp = [k for k, v in accuracy_data.items() if v["fp"] > v["tp"]]
    if high_fp:
        insights.append(f"High false positive rate: {', '.join(high_fp)}")
    
    # Check for high false negative rates
    high_fn = [k for k, v in accuracy_data.items() if v["fn"] > v["tp"]]
    if high_fn:
        insights.append(f"High false negative rate: {', '.join(high_fn)}")
    
    return insights
