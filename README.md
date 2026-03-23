# PII Detection and De-identification Tool

A comprehensive Streamlit-based web application for detecting and de-identifying Personally Identifiable Information (PII) in CSV datasets.

## Features

- **PII Detection**: Automatic detection of various PII types including:
  - Aadhaar numbers (with Verhoeff checksum validation)
  - PAN cards (with check digit validation)
  - Credit cards (with Luhn algorithm validation)
  - Email addresses (with RFC 5322 compliance)
  - Phone numbers (Indian format)

- **De-identification Methods**:
  - **Masking**: Hide parts of PII (e.g., XXXX-XXXX-XXXX-1234)
  - **Anonymization**: Replace with random strings
  - **Pseudo-anonymization**: Replace with consistent fake values
  - **Selective**: Apply field-specific de-identification rules

- **Authentication System**:
  - User registration and login
  - Session management with persistent login
  - Admin panel for user and data management

- **Accuracy Analysis**:
  - Comprehensive metrics (Precision, Recall, F1-Score, Specificity)
  - Confusion matrix analysis
  - Detailed performance visualization

- **Reporting**:
  - PDF accuracy reports
  - CSV export of de-identified data
  - Data visualization charts

## Project Structure

```
PII/
├── main.py                 # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── config/                # Configuration files
│   ├── __init__.py
│   ├── patterns.py        # PII detection patterns
│   └── database.py        # Database configuration
├── src/                   # Source code modules
│   ├── __init__.py
│   ├── auth/             # Authentication module
│   │   ├── __init__.py
│   │   ├── database.py   # Database operations
│   │   ├── sessions.py   # Session management
│   │   ├── data_logging.py # Data logging
│   │   └── validation.py # Password validation
│   ├── detection/        # PII detection module
│   │   ├── __init__.py
│   │   └── detector.py   # PII detection logic
│   ├── validation/       # PII validation module
│   │   ├── __init__.py
│   │   ├── algorithms.py # Validation algorithms
│   │   └── validators.py # PII validators
│   ├── deidentification/ # De-identification module
│   │   ├── __init__.py
│   │   ├── masking.py    # Masking functions
│   │   ├── anonymization.py # Anonymization functions
│   │   ├── pseudonymization.py # Pseudo-anonymization
│   │   └── deidentifier.py # Main de-identification handler
│   ├── reports/          # Report generation module
│   │   ├── __init__.py
│   │   └── pdf_generator.py # PDF report generation
│   ├── ui/              # User interface components
│   │   ├── __init__.py
│   │   ├── login.py     # Login page components
│   │   ├── admin_panel.py # Admin panel components
│   │   └── styling.py   # UI styling and CSS
│   └── utils/           # Utility modules
│       ├── __init__.py
│       ├── metrics.py   # Accuracy metrics calculation
│       └── data_processor.py # Data processing utilities
├── data/                # Data directory (created automatically)
├── tests/              # Test files directory
└── config/             # Configuration files
```

## Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run main.py
   ```

## Usage

### For Regular Users

1. **Account Creation**: Register with a strong password meeting the security requirements
2. **Login**: Access the application with your credentials
3. **Upload Data**: Upload CSV files containing data to be analyzed
4. **Choose Method**: Select your preferred de-identification method
5. **Review Results**: Examine the de-identified data and accuracy metrics
6. **Download**: Get your processed data and accuracy reports

### For Administrators

1. **Login**: Use admin credentials to access the admin panel
2. **User Management**: View, manage, and delete user accounts
3. **Data Management**: Monitor uploaded and processed data
4. **Access Logs**: Review user activity logs
5. **System Maintenance**: Clean up old data and logs

## Security Features

- **Password Validation**: Enforced strong password requirements
- **Session Management**: Secure session tokens with expiration
- **Data Isolation**: User data is properly isolated and tracked
- **Admin Controls**: Comprehensive administrative oversight

## PII Types Supported

### Aadhaar Numbers
- 12-digit format with optional separators
- Verhoeff checksum validation
- Must start with digits 2-9

### PAN Cards
- 10-character alphanumeric format
- Entity type validation
- Check digit verification

### Credit Cards
- 13-19 digit numbers with optional separators
- Luhn algorithm validation
- Support for various card formats

### Email Addresses
- RFC 5322 compliant validation
- Domain and local part verification
- Comprehensive format checking

### Phone Numbers
- Indian 10-digit mobile format
- Must start with digits 6-9
- Validates against standard patterns

## Configuration

### Database Settings
- SQLite database for user management
- Configurable session expiry
- Automatic directory creation

### Pattern Customization
- Regex patterns in `config/patterns.py`
- Easy addition of new PII types
- Configurable validation rules

## Development

### Adding New PII Types

1. Add regex pattern to `config/patterns.py`
2. Implement validation in `src/validation/validators.py`
3. Add de-identification methods in respective modules
4. Update type mapping in configuration

### Testing

- Unit tests can be added in the `tests/` directory
- Test different PII types and validation scenarios
- Verify accuracy metrics calculations

## License

This project is developed for educational and research purposes. Please ensure compliance with data protection regulations when using with real data.

## Support

For issues, feature requests, or questions, please refer to the project documentation or contact the development team.
