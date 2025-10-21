# LinkedIn Easy Apply Automation

A minimal end-to-end workflow for automating LinkedIn Easy Apply job applications using Playwright. This tool handles login, job search, data extraction, and basic form filling.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Features](#features)
- [Limitations](#limitations)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)

## Introduction

This LinkedIn Easy Apply automation tool is designed to streamline your job application process by automatically applying to jobs that have the "Easy Apply" feature on LinkedIn. The tool uses Playwright for browser automation and focuses on a minimal viable product (MVP) approach.

### Key Capabilities

- 🔐 Automatic LinkedIn login
- 🔍 Job search with customizable terms and locations
- 📋 Job listing extraction and filtering
- 📝 Easy Apply form filling
- 📊 Application tracking with CSV logging
- 📸 Error screenshots for debugging

## Installation

### Prerequisites

- Python 3.11.6 or higher
- Chrome/Chromium browser
- LinkedIn account with Easy Apply access

### Setup Steps

1. **Install Playwright browsers:**
   ```bash
   playwright install chromium
   ```

2. **Verify installation:**
   ```bash
   python -c "from playwright.sync_api import sync_playwright; print('Playwright installed successfully')"
   ```

3. **Install project dependencies:**
   ```bash
   pip install -e .
   ```

## Configuration

### 1. Update LinkedIn Credentials

Edit `zlm/workflow/linkedin_config.py`:

```python
# LinkedIn credentials - REQUIRED
LINKEDIN_EMAIL = "your.email@example.com"
LINKEDIN_PASSWORD = "your_password"
```

### 2. Configure Job Search Parameters

```python
# Job search parameters
SEARCH_TERMS = ["Software Engineer", "Python Developer", "Data Scientist"]
SEARCH_LOCATION = "United States"  # or "India", "Chicago, Illinois", etc.
MAX_APPLICATIONS = 5  # Maximum applications per run
```

### 3. Set Personal Information

```python
# Personal information for Easy Apply forms
PHONE_NUMBER = "+1234567890"
YEARS_OF_EXPERIENCE = "5"
REQUIRE_VISA = "No"  # "Yes" or "No"
DEFAULT_RESUME_PATH = "/path/to/your/resume.pdf"
```

### 4. Browser Settings

```python
# Browser settings
HEADLESS = False  # Set True to run in background
BROWSER_TIMEOUT = 10000  # 10 seconds
```

### 5. Output Configuration

```python
# Output settings
OUTPUT_DIR = "output/linkedin_applications"
CSV_FILE = "applied_jobs.csv"
FAILED_CSV = "failed_jobs.csv"
```

## Usage

### Basic Usage

1. **Configure your settings** in `linkedin_config.py`

2. **Run the automation:**
   ```bash
   python -m zlm.workflow.linkedin_auto_apply
   ```

3. **Check results** in the `output/linkedin_applications/` directory:
   - `applied_jobs.csv` - Successfully applied jobs
   - `failed_jobs.csv` - Failed applications with error details
   - `screenshots/` - Error screenshots for debugging

### Advanced Usage

```python
from zlm.workflow.linkedin_auto_apply import LinkedInAutoApply

# Create automation instance
automation = LinkedInAutoApply()

# Run automation
success = automation.run_automation()

if success:
    print("Automation completed successfully!")
else:
    print("Automation failed. Check logs for details.")
```

### Example Output

```
🚀 Starting LinkedIn Easy Apply Automation
==================================================
🔐 Logging into LinkedIn...
✅ Successfully logged into LinkedIn
🔍 Searching for jobs: Software Engineer
📋 Found 15 job listings
🎯 8 jobs have Easy Apply

📝 Applying to: Senior Software Engineer at TechCorp
✅ Application 1 completed

📝 Applying to: Python Developer at StartupXYZ
✅ Application 2 completed

==================================================
📊 AUTOMATION SUMMARY
==================================================
✅ Successfully applied: 2 jobs
❌ Failed applications: 0 jobs
📁 Output directory: output/linkedin_applications
```

## Features

### Current Features (MVP)

- ✅ **LinkedIn Login**: Automatic login with email/password
- ✅ **Job Search**: Search jobs by title and location
- ✅ **Job Filtering**: Only processes jobs with Easy Apply
- ✅ **Form Filling**: Automatically fills common form fields:
  - Phone number
  - Years of experience
  - Visa sponsorship requirements
  - Resume upload
- ✅ **Multi-step Forms**: Handles multi-page Easy Apply forms
- ✅ **Application Tracking**: CSV logging of all applications
- ✅ **Error Handling**: Screenshots and detailed error logging
- ✅ **Browser Automation**: Uses Playwright for reliable automation

### Form Field Detection

The tool automatically detects and fills:

- **Text Inputs**: Phone numbers, experience years, etc.
- **Select Dropdowns**: Experience levels, locations, etc.
- **Radio Buttons**: Yes/No questions, visa requirements
- **Checkboxes**: Terms and conditions, agreements
- **File Uploads**: Resume/CV uploads

### Question Answering

Common questions are automatically answered:

| Question Type | Default Answer |
|---------------|----------------|
| Phone number | From config |
| Years of experience | From config |
| Visa sponsorship | From config |
| Work authorization | "Yes" |
| Willing to relocate | "No" |
| Open to remote work | "Yes" |

## Limitations

### Current Limitations

- ❌ **No AI Integration**: Cannot answer custom questions intelligently
- ❌ **Limited Search Terms**: Processes one search term at a time
- ❌ **Basic Form Filling**: Only handles common, predictable questions
- ❌ **No Resume Customization**: Uses single resume for all applications
- ❌ **No Cover Letter Generation**: No personalized cover letters
- ❌ **Manual Configuration**: Requires manual setup of personal information

### Known Issues

- LinkedIn may detect automation (use responsibly)
- Some forms may have unexpected field types
- Network issues can cause timeouts
- LinkedIn UI changes may break selectors

## Troubleshooting

### Common Issues

#### 1. Login Failed
```
❌ Login failed - could not find profile elements
```

**Solutions:**
- Verify credentials in `linkedin_config.py`
- Check if LinkedIn requires 2FA
- Try logging in manually first
- Check for LinkedIn security prompts

#### 2. No Jobs Found
```
❌ No job listings found
```

**Solutions:**
- Verify search terms are valid
- Check if location is correct
- Try broader search terms
- Check LinkedIn job search manually

#### 3. Easy Apply Button Not Found
```
❌ Easy Apply button not found for this job
```

**Solutions:**
- Not all jobs have Easy Apply
- Job may have already been applied to
- LinkedIn UI may have changed
- Check job listing manually

#### 4. Form Filling Errors
```
❌ Error filling form fields
```

**Solutions:**
- Check if resume file exists and is accessible
- Verify personal information in config
- Review error screenshots in `screenshots/` directory
- Try with different job listings

### Debug Mode

Enable debug mode by setting `HEADLESS = False` in config to see the browser in action.

### Logs and Screenshots

- **CSV Logs**: Check `applied_jobs.csv` and `failed_jobs.csv`
- **Screenshots**: Error screenshots saved in `screenshots/` directory
- **Console Output**: Detailed logging in terminal

## Future Enhancements

### Planned Features

- 🤖 **AI Integration**: Use LLMs to answer custom questions
- 📄 **Resume Customization**: Generate tailored resumes per job
- 📝 **Cover Letter Generation**: Create personalized cover letters
- 🔍 **Advanced Search**: Multiple search terms, filters, and locations
- 🔄 **Retry Logic**: Automatic retry for failed applications
- 🎯 **Smart Filtering**: Skip jobs based on criteria
- 📊 **Analytics**: Application success rates and insights
- 🔐 **Security**: Enhanced anti-detection measures

### Integration Opportunities

- **Resume Generation**: Integrate with existing `AutoApplyModel`
- **Job Matching**: Use existing job details extraction
- **Cover Letters**: Leverage existing cover letter generation
- **Metrics**: Apply existing similarity calculations

### Advanced Features

- **Scheduling**: Run automation at specific times
- **Notifications**: Email/SMS alerts for results
- **Dashboard**: Web interface for monitoring
- **API**: REST API for external integrations

## Support

For issues and questions:

1. Check the troubleshooting section above
2. Review error logs and screenshots
3. Test with different job listings
4. Verify configuration settings

## Contributing

This is an MVP implementation. Future contributions welcome for:

- Enhanced form field detection
- Better error handling
- Additional question types
- Performance improvements
- Documentation updates

---

**Note**: Use this tool responsibly and in accordance with LinkedIn's Terms of Service. The tool is for personal use only and should not be used for commercial purposes or to spam applications.
