# 📧 CrewAI Gmail Integration

This project demonstrates Gmail integration with CrewAI for email classification and automated responses.

## 🚀 Quick Setup

### 1. Virtual Environment Setup
```bash
# Create and activate virtual environment
./setup_venv.sh

# Activate environment
source venv/bin/activate
```

### 2. Google API Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API
4. Create credentials (OAuth 2.0 Client ID)
5. Download the credentials file as `credentials.json`
6. Place `credentials.json` in this directory

### 3. Run the Project
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run email classification test
python crewai_mail_test.py

# Or run attack path analysis
python Attack_Paths.py
```

## 📁 Project Structure

```
crewai_gmail/
├── crewai_mail_test.py      # Main email classification script
├── Attack_Paths.py          # Attack path analysis
├── google_service_utils.py  # Google API utilities
├── tools.py                 # CrewAI tools for email operations
├── credentials.json         # Google API credentials (you need to add this)
├── requirements.txt         # Python dependencies
├── setup_venv.sh           # Virtual environment setup
└── logs/                   # Log files
```

## 🔧 Features

- **Email Classification**: Automatically classify emails using CrewAI agents
- **Gmail Integration**: Read and send emails through Gmail API
- **Attack Path Analysis**: Security-focused email analysis
- **Automated Responses**: Send automated email responses

## ⚙️ Configuration

### Environment Variables (Optional)
Create a `.env` file for additional configuration:
```
OPENAI_API_KEY=your_openai_key_here
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

### Google API Scopes
The project uses these Gmail API scopes:
- `https://www.googleapis.com/auth/gmail.readonly` - Read emails
- `https://www.googleapis.com/auth/gmail.send` - Send emails

## 🐛 Troubleshooting

### Common Issues

1. **Authentication Error**
   - Ensure `credentials.json` is in the project directory
   - Run the script once to complete OAuth flow

2. **Module Import Error**
   - Make sure virtual environment is activated
   - Check if all dependencies are installed: `pip list`

3. **Gmail API Quota Exceeded**
   - Check your Google Cloud Console for API usage limits
   - Enable billing if necessary for higher quotas

### Dependencies Issues
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Check installed packages
pip list | grep -E "(crewai|google|openai)"
```

## 📚 Usage Examples

### Basic Email Classification
```python
from crewai_mail_test import email_classifier
# The script will automatically fetch and classify unread emails
```

### Custom Email Analysis
```python
from Attack_Paths import attack_analysis_agent
# Run security-focused email analysis
```

## 🔒 Security Notes

- Keep `credentials.json` secure and never commit it to version control
- Use environment variables for sensitive configuration
- Review email permissions carefully when granting access

---

**📧 Ready to analyze your emails with AI!** Make sure to set up your Google credentials first.
