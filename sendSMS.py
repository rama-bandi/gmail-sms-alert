import smtplib
from email.mime.text import MIMEText
import csv
import base64
from config_loader import config

# Email credentials from config
SENDER_EMAIL = config.EMAIL['sender_email']

# Carrier gateways from config
CARRIER_GATEWAYS = config.CARRIERS

def create_message(sender, to, subject, message_text):
    """Create a MIME message for sending."""
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')}

def send_message(service, user_id, message):
    """Send an email using the Gmail API."""
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f"Message sent! Message ID: {message['id']}")
        return message
    except Exception as e:
        print(f"Failed to send message: {e}")
        return None

def send_sms_via_gmail(service, sender_email, recipient_number, carrier_gateway, message_text):
    """Send an SMS using the Gmail API."""
    recipient_email = f"{recipient_number}@{carrier_gateway}"
    message = create_message(sender_email, recipient_email, "", message_text)
    send_message(service, "me", message)

def read_phone_numbers(file_path):
    """Read phone numbers and carriers from a file."""
    phone_numbers = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            phone_numbers.append((row['phone_number'], row['carrier']))
    return phone_numbers

def sendSMS(message, service):
    # Get phone numbers file path from config
    file_path = config.SMS['phone_numbers_file']
    
    # Read phone numbers and carriers from the file
    phone_numbers = read_phone_numbers(file_path)
    

    # Send SMS to each phone number
    for number, carrier in phone_numbers:
        if carrier in CARRIER_GATEWAYS:
            send_sms_via_gmail(service, SENDER_EMAIL, number, CARRIER_GATEWAYS[carrier], message)
        else:
            print(f"Unsupported carrier '{carrier}' for phone number {number}.")

#if __name__ == '__main__':
#    main()