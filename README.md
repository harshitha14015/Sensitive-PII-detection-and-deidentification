# PII Detection and De-Identification Tool

A Streamlit-based web application for detecting and protecting Personally Identifiable Information (PII) in CSV datasets using validation algorithms and multiple de-identification techniques.

---

## Overview

This project provides a structured approach to handling sensitive data by integrating pattern-based detection, validation mechanisms, and privacy-preserving transformations. It supports both end users and administrators, along with performance evaluation and reporting capabilities.

---

## Features

### PII Detection
- Detects Aadhaar numbers, PAN cards, credit card numbers, email addresses, and phone numbers  
- Uses validation algorithms such as Verhoeff and Luhn  
- Implements regex-based pattern matching for accurate identification  

### De-Identification Techniques
- Masking: Partially hides sensitive information  
- Anonymization: Replaces data with random values  
- Pseudonymization: Generates consistent substitute values  
- Selective processing: Applies different techniques to specific fields  

### Authentication and Access Control
- User registration and login  
- Session management with persistence  
- Administrative panel for user and data management  

### Analytics and Reporting
- Performance metrics including Precision, Recall, F1-score, and Specificity  
- Confusion matrix evaluation  
- Exportable PDF reports and processed CSV files  

---

## Technology Stack

- Frontend: Streamlit  
- Backend: Python  
- Database: SQLite  
- Libraries: Pandas, NumPy, Regex, ReportLab  

---

## Project Structure
```
PII/
├── main.py
├── requirements.txt
├── config/
├── src/
│ ├── auth/
│ ├── detection/
│ ├── validation/
│ ├── deidentification/
│ ├── reports/
│ └── utils/
├── data/
├── tests/
```
---

## Installation

```bash
git clone https://github.com/your-username/pii-detection-tool.git
cd pii-detection-tool
pip install -r requirements.txt
streamlit run main.py
```

## Usage

### For Users
- Register and log in  
- Upload a CSV dataset  
- Select a de-identification method  
- Review processed data and evaluation metrics  
- Download the results  

### For Administrators
- Manage user accounts and datasets  
- Monitor system activity and logs  
- Perform maintenance operations  

---

## Security Features

- Strong password validation  
- Secure session handling  
- Data isolation between users  
- Administrative access control  

---

## Supported PII Types

- Aadhaar number (12-digit format with checksum validation)  
- PAN card (alphanumeric format with validation)  
- Credit card numbers (Luhn algorithm validation)  
- Email addresses (standard format validation)  
- Phone numbers (Indian mobile format)  

---

## Extensibility

- Add new PII patterns in `config/patterns.py`  
- Extend validation logic in `src/validation/`  
- Implement additional de-identification strategies  

---

## Testing

```bash
pytest tests/
```
---
## License

This project is provided for educational and research use.  
Any use of real-world data must comply with relevant data protection laws and regulations. The author is not responsible for misuse of this project.
