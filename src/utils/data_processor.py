"""
Data Processing Module
Handles DataFrame processing and PII detection/anonymization
"""
import pandas as pd
from config.patterns import patterns
from detection.detector import detect_pii, any_true_pii
from validation.validators import is_valid_pii
from deidentification.deidentifier import deidentify_value

def process_dataframe_with_report(df, pii_to_mask, report, metrics):
    """
    Processes a chunk of the dataframe and updates global report and metrics.
    """
    df_anonymized, df_pseudonymized = df.copy(), df.copy()
    identified_data, deidentified_data = pd.DataFrame(index=df.index, columns=df.columns), pd.DataFrame(index=df.index, columns=df.columns)

    for col in df.columns:
        for i, cell in enumerate(df[col].astype(str).str.strip()):
            # Fixed the error by ensuring the pattern object is used correctly.
            detected_flags = {key: bool(patterns[key].search(cell)) for key in patterns.keys()}
            
            actual_flags = {k:v if k in pii_to_mask else False for k,v in detected_flags.items()}

            for key in actual_flags:
                if actual_flags[key]: report[f"{key}_found"] += 1
                if actual_flags[key] and detected_flags[key]: metrics[key]["TP"] += 1
                elif not actual_flags[key] and detected_flags[key]: metrics[key]["FP"] += 1
                elif not actual_flags[key] and not detected_flags[key]: metrics[key]["TN"] += 1
                elif actual_flags[key] and not detected_flags[key]: metrics[key]["FN"] += 1

            # Anonymization
            anon_cell = cell
            if actual_flags.get("aadhaar"): 
                from deidentification.masking import mask_aadhaar
                anon_cell = mask_aadhaar(cell)
            elif actual_flags.get("pan"): 
                from deidentification.masking import mask_pan
                anon_cell = mask_pan(cell)
            elif actual_flags.get("credit_card"):
                from deidentification.masking import mask_credit_card
                anon_cell = mask_credit_card(cell)
            elif actual_flags.get("email"): 
                from deidentification.masking import mask_email
                anon_cell = mask_email(cell)
            elif actual_flags.get("phone"): 
                from deidentification.masking import mask_phone
                anon_cell = mask_phone(cell)
            
            df_anonymized.at[i, col] = anon_cell

            # Pseudonymization
            pseudo_cell = cell
            if any(actual_flags.values()):
                from deidentification.pseudonymization import pseudo_anonymize
                for key in actual_flags:
                    if actual_flags[key]:
                        pseudo_cell = pseudo_anonymize(cell, key)
                        break
            df_pseudonymized.at[i, col] = pseudo_cell
            
            identified_data.at[i, col] = cell if any(actual_flags.values()) else ""
            deidentified_data.at[i, col] = anon_cell if any(actual_flags.values()) else ""
            
    return df_anonymized, df_pseudonymized, identified_data, deidentified_data, report, metrics
