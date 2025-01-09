# Gmail SMS Notifier

This application monitors your Gmail inbox for specific emails and sends SMS notifications when matching emails are found.

## Features
- Monitors Gmail inbox for specific search terms
- Sends SMS notifications via email-to-SMS gateways
- Supports multiple carriers (AT&T, Verizon, T-Mobile, Google Voice)
- Configurable search terms and notification settings
- Handles both HTML and plain text emails

## Prerequisites
- Python 3.7+
- Gmail account
- Google Cloud Platform project with Gmail API enabled

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd gmail-sms-notifier
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up configuration files**
   - Copy template files to create your configurations:
     ```bash
     cp config.ini.template config.ini
     cp phone_numbers.txt.template phone_numbers.txt
     ```
   - Edit `config.ini` with your settings
   - Update `phone_numbers.txt` with your phone numbers and carriers

4. **Set up Google Credentials**
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project or select existing project
   - Enable Gmail API
   - Create OAuth 2.0 credentials
   - Download credentials and save as `google-credentials.json`

5. **Configure Settings**
   - Update `config.ini` with your preferences:
     - Email settings
     - Search terms
     - SMS settings
     - Carrier configurations
   - Update `phone_numbers.txt` with recipient information

## Usage

Run the application: