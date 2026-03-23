# PII Detection Project - Installation Guide

## Prerequisites

Before installing this project, ensure you have the following installed on your computer:

### Required Software
- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **pip** (Python package installer) - Usually comes with Python

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: At least 500MB free space
- **Internet Connection**: Required for downloading dependencies

## Installation Steps

### Step 1: Clone the Repository

Open a terminal/command prompt and run:

```bash
git clone https://github.com/hitheshsa/PII_detection.git
cd PII_detection
```

### Step 2: Create a Virtual Environment (Recommended)

#### On Windows:
```bash
python -m venv pii_env
pii_env\Scripts\activate
```

#### On macOS/Linux:
```bash
python3 -m venv pii_env
source pii_env/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

If you encounter any issues, try upgrading pip first:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Verify Installation

Check if all required packages are installed:
```bash
pip list
```

You should see packages like:
- streamlit
- pandas
- matplotlib
- reportlab
- bcrypt
- re (built-in)
- sqlite3 (built-in)

## Running the Application

### Start the Application

```bash
streamlit run main.py
```

### Access the Application

1. After running the command, you'll see output similar to:
   ```
   Local URL: http://localhost:8501
   Network URL: http://192.168.x.x:8501
   ```

2. Open your web browser and navigate to: `http://localhost:8501`

3. The PII Detection application will load in your browser

## First Time Setup

### Create Admin Account
1. When you first run the application, you'll need to create an admin account
2. Click on "Create Admin Account" 
3. Fill in the required details:
   - Username
   - Password
   - Email
   - Full Name

### Login
1. Use your admin credentials to log in
2. You'll have access to all features including the admin panel

## Features Available

Once logged in, you can:

- **Upload Files**: Upload CSV, TXT, or DOCX files for PII detection
- **Detect PII**: Automatically identify personally identifiable information
- **De-identify Data**: Mask, anonymize, or pseudonymize detected PII
- **Generate Reports**: Create PDF reports of the detection results
- **View Metrics**: See detection statistics and visualizations
- **Admin Panel**: Manage users and view system logs (admin only)

## Troubleshooting

### Common Issues and Solutions

#### Issue: "streamlit: command not found"
**Solution**: Make sure you've activated your virtual environment and installed the requirements

#### Issue: "Module not found" errors
**Solution**: 
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

#### Issue: Port already in use
**Solution**: 
```bash
streamlit run main.py --server.port 8502
```

#### Issue: Permission denied on Windows
**Solution**: Run the command prompt as Administrator

#### Issue: Database locked error
**Solution**: Make sure no other instance of the application is running

### Python Version Issues

If you have multiple Python versions:

#### Windows:
```bash
py -3.8 -m venv pii_env
# or
python3.8 -m venv pii_env
```

#### macOS/Linux:
```bash
python3.8 -m venv pii_env
# or
/usr/bin/python3.8 -m venv pii_env
```

## Project Structure

```
PII_detection/
├── main.py                 # Main Streamlit application
├── requirements.txt        # Python dependencies
├── install.md             # This installation guide
├── README.md              # Project documentation
├── .gitignore             # Git ignore rules
├── config/                # Configuration files
│   ├── __init__.py
│   ├── patterns.py        # PII detection patterns
│   └── database.py        # Database configuration
├── src/                   # Source code modules
│   ├── __init__.py
│   ├── auth/              # Authentication module
│   ├── detection/         # PII detection logic
│   ├── validation/        # Data validation
│   ├── deidentification/  # Data de-identification
│   ├── reports/           # PDF report generation
│   ├── ui/                # User interface components
│   └── utils/             # Utility functions
├── data/                  # Data directory (created automatically)
├── tests/                 # Test files
└── users.db               # SQLite database (created automatically)
```

## Updating the Application

To get the latest updates:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## Uninstalling

To remove the application:

1. Deactivate the virtual environment:
   ```bash
   deactivate
   ```

2. Delete the project folder:
   ```bash
   rm -rf PII_detection  # Linux/macOS
   rmdir /s PII_detection  # Windows
   ```

3. Delete the virtual environment:
   ```bash
   rm -rf pii_env  # Linux/macOS
   rmdir /s pii_env  # Windows
   ```

## Development Setup

If you want to contribute or modify the code:

### Install Development Dependencies
```bash
pip install pytest black flake8 mypy
```

### Run Tests
```bash
python -m pytest tests/
```

### Code Formatting
```bash
black src/ main.py
```

### Type Checking
```bash
mypy src/
```

## Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Ensure all prerequisites are met
3. Verify your Python version: `python --version`
4. Check if all dependencies are installed: `pip list`
5. Look for error messages in the terminal

## Security Notes

- The application uses SQLite database for user management
- Passwords are hashed using bcrypt
- Uploaded files are processed locally (not sent to external servers)
- Session management is handled securely
- Make sure to use strong passwords for admin accounts

## Performance Tips

- For large files (>10MB), processing may take longer
- Close unused browser tabs to free up memory
- Use the latest version of Python for better performance
- Consider increasing system RAM for processing very large datasets

---

**Note**: This application processes sensitive data locally on your machine. No data is transmitted to external servers, ensuring privacy and security of your PII detection operations.
