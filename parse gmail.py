from googleapiclient.discovery import build
from transformers import pipeline
from gmail import authenticate_gmail
from sendSMS import sendSMS
from bs4 import BeautifulSoup
import base64
from config_loader import config

def fetch_emails(service):
    max_results = config.EMAIL['max_results']
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=max_results).execute()
    messages = results.get('messages', [])
    
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        email_data = msg['payload']['headers']
        for values in email_data:
            if values['name'] == 'Subject':
                subject = values['value']
            if values['name'] == 'From':
                sender = values['value']
        
        print(f"From: {sender}")
        print(f"Subject: {subject}")
        
        # Analyze email content with AI
        if 'parts' in msg['payload']:
            for part in msg['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    email_body = part['body']['data']
                    email_body = base64.urlsafe_b64decode(email_body).decode('utf-8')
                    sentiment_analysis = pipeline("sentiment-analysis")
                    sentiment = sentiment_analysis(email_body)
                    print(f"Sentiment: {sentiment[0]['label']} ({sentiment[0]['score']:.2f})")
                    print("------")




def fetch_emails_for_search_term(service):
    """Fetch emails containing Search term in the body."""
    search_term = config.SEARCH['search_term']
    max_results = config.EMAIL['max_results']
    
    results = service.users().messages().list(userId='me', q=search_term, maxResults=max_results).execute()
    messages = results.get('messages', [])
    
    if not messages:
        print(f"No emails containing '{search_term}' found.")
        return
    
    message_length = config.SMS['message_length']
    
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        email_data = msg['payload']['headers']
        subject = next((header['value'] for header in email_data if header['name'] == 'Subject'), 'No Subject')
        sender = next((header['value'] for header in email_data if header['name'] == 'From'), 'Unknown Sender')
        
        print(f"From: {sender}")
        print(f"Subject: {subject}")
        
        email_body = get_email_body(msg['payload'])
        sms_message = f"New VFS Email:\nFrom: {sender}\nSubject: {subject}\nBody: {email_body[:message_length]}"
        sendSMS(sms_message, service)   

        
def get_email_body(payload):
    """Extract the email body from the payload, handling text/html MIME type."""
    if 'parts' in payload:
        # Iterate through all parts of the email
        for part in payload['parts']:
            if part['mimeType'] == 'text/html':
                # Decode the HTML content
                print("HTML content found")
                html_content = part['body']['data']
                html_content = base64.urlsafe_b64decode(html_content).decode('utf-8')
                soup = BeautifulSoup(html_content, 'html.parser')
                plain_text = soup.get_text()
                return plain_text
            elif part['mimeType'] == 'text/plain':
                print("Plain text found")
                plain_text = part['body']['data']
                plain_text = base64.urlsafe_b64decode(plain_text).decode('utf-8')
                return plain_text
        else:
            print("No email body found.")
    elif payload['mimeType'] == 'text/html':
        # If the email has no parts and is directly HTML
        html_content = payload['body']['data']
        html_content = base64.urlsafe_b64decode(html_content).decode('utf-8')
        soup = BeautifulSoup(html_content, 'html.parser')
        plain_text = soup.get_text()
        return plain_text
    return None
           # Extract email body
        

def main():
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)
    fetch_emails_for_search_term(service)

if __name__ == '__main__':
    main()