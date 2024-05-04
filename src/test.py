import streamlit as st
import requests
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define your database connection
DATABASE_URL = 'sqlite:///questionnaires.db'

# Create SQLAlchemy engine and session
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Define SQLAlchemy Base
Base = declarative_base()


# Define Questionnaire model
class Questionnaire(Base):
    __tablename__ = 'questionnaires'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    questions = Column(String)

# Create tables if not exist
Base.metadata.create_all(engine)

# Function to retrieve questionnaires from the database
def get_questionnaires():
    return session.query(Questionnaire).all()


# Define your Telegram bot token
TELEGRAM_BOT_TOKEN = 'TELEGRAM_BOT_TOKEN'

# Define the base URL for Telegram API
TELEGRAM_API_BASE_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/'

# Define the Streamlit web app
def main():
    st.title('Telegram Bot API')
    st.markdown('This is a simple web API for Telegram bot.')

    # Define a text input for sending messages
    message = st.text_input('Enter your message to send via Telegram bot:')

    if st.button('Send Message'):
        # Call the Telegram API to send the message
        response = send_message(message)
        if response['ok']:
            st.success('Message sent successfully!')
        else:
            st.error('Failed to send message. Please try again.')

    questionnaires = get_questionnaires()

    if not questionnaires:
        st.warning('No questionnaires found in the database.')
    else:
        st.write('Available Questionnaires:')
        for questionnaire in questionnaires:
            st.write(f"- {questionnaire.title}")

        selected_questionnaire = st.selectbox('Select a questionnaire to send:', [q.title for q in questionnaires])

        if st.button('Send Questionnaire'):
            # Find the selected questionnaire
            selected_q = next((q for q in questionnaires if q.title == selected_questionnaire), None)
            if selected_q:
                # Call the Telegram API to send the questionnaire
                response = send_message(selected_q.questions)
                if response['ok']:
                    st.success('Questionnaire sent successfully!')
                else:
                    st.error('Failed to send questionnaire. Please try again.')

# Function to send a message via the Telegram bot
def send_message(text):
    url = TELEGRAM_API_BASE_URL + 'sendMessage'
    data = {
        'chat_id': 'CHAT_ID',  # Replace with the chat ID of the user or group
        'text': text
    }
    response = requests.post(url, data=data)
    return response.json()

if __name__ == '__main__':
    main()
