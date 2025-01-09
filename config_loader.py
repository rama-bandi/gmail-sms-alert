import configparser
import os

class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        config_path = 'config.ini'
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file {config_path} not found!")
            
        self.config.read(config_path)
        
        # Email settings
        self.EMAIL = {
            'sender_email': self.config['Email']['sender_email'],
            'max_results': self.config.getint('Email', 'max_results')
        }
        
        # Search settings
        self.SEARCH = {
            'search_term': self.config['Search']['search_term']
        }
        
        # SMS settings
        self.SMS = {
            'message_length': self.config.getint('SMS', 'message_length'),
            'phone_numbers_file': self.config['SMS']['phone_numbers_file']
        }
        
        # Carrier settings
        self.CARRIERS = dict(self.config['Carriers'])
        
        # Google API settings
        self.GOOGLE = {
            'scopes': self.config['Google']['scopes'].split(),  # Split on whitespace
            'credentials_file': self.config['Google']['credentials_file']
        }

# Create a singleton instance
config = Config() 