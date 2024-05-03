import streamlit as st
import requests

# Define your Telegram bot token
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Define the base URL for Telegram API
TELEGRAM_API_BASE_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/'

# Define the Streamlit web app
def main():
    st.title('Telegram Bot API')
    st.markdown('This is a simple web API for your Telegram bot.')

    # Define a text input for sending messages
    message = st.text_input('Enter your message to send via Telegram bot:')

    if st.button('Send Message'):
        # Call the Telegram API to send the message
        response = send_message(message)
        if response['ok']:
            st.success('Message sent successfully!')
        else:
            st.error('Failed to send message. Please try again.')

# Function to send a message via the Telegram bot
def send_message(text):
    url = TELEGRAM_API_BASE_URL + 'sendMessage'
    data = {
        'chat_id': 'YOUR_CHAT_ID',  # Replace with the chat ID of the user or group
        'text': text
    }
    response = requests.post(url, data=data)
    return response.json()

if __name__ == '__main__':
    main()

