import logging
import os
import threading
import sys
from flask import Flask, request, session
from flask_sockets import Sockets
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app and Flask-Sockets
app = Flask(__name__)
sockets = Sockets(app)

# Enable Flask sessions
app.secret_key = os.getenv("FLASK_SECRET_KEY", "your_default_secret_key")

# Set the OpenAI API key and API type globally
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_type = "openai"
openai_client = openai

# Twilio account SID and auth token
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Flag to track when the call ends
call_active = True

# Make a call to a phone number and initiate the conversation
def make_call(to_phone_number):
    call = client.calls.create(
        to=to_phone_number,
        from_=TWILIO_PHONE_NUMBER,
        url=os.getenv("CALL_URL")  # Use environment variable for URL
    )
    print(f"Call initiated with SID: {call.sid}")

@app.route("/handle_call", methods=["GET", "POST"])
def handle_call():
    response = VoiceResponse()

    # Check if the user has already been greeted
    if not session.get("greeted", False):
        response.say("Hello, I am an AI-powered assistant. How can I help you today?")
        session["greeted"] = True  # Mark the user as greeted

    # Collect the caller's input (speech input)
    gather = response.gather(input='speech', timeout=5, action='/process_speech')

    # If no input is received, say something and try again
    response.say("Sorry, I didn't hear that. Can you repeat?")
    response.redirect('/handle_call')  # Retry if no input is detected

    return str(response)

@app.route("/process_speech", methods=["GET", "POST"])
def process_speech():
    global call_active
    response = VoiceResponse()

    # Get the speech result from Twilio
    speech_input = request.values.get('SpeechResult', '')
    print(f"Received speech input: {speech_input}")

    if speech_input:
        # Check if the user wants to end the call
        if "goodbye" in speech_input.lower() or "end call" in speech_input.lower():
            response.say("Goodbye! Ending the call now.")
            call_active = False  # Set the flag to end the call

            # Delay the server shutdown to allow the response to complete
            threading.Thread(target=shutdown_server).start()
            return str(response)

        # If speech input is received, generate a response using OpenAI
        ai_response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",  # Or use another model like gpt-4, if you have access
            messages=[{"role": "system", "content": "You are an AI assistant."},
                      {"role": "user", "content": speech_input}],
            max_tokens=150,  # Adjust the max tokens as needed
            temperature=0.8,  # Adjust the temperature for randomness
        )

        ai_reply = ai_response.choices[0].message.content.strip()
        print(f"AI Reply: {ai_reply}")

        # Respond to the caller using TTS (Text-to-Speech)
        response.say(ai_reply)
        response.redirect('/handle_call')  # Redirect to continue the conversation
    else:
        # If no speech input is detected, ask the user to try again
        response.say("Sorry, I didn't hear that. Can you repeat?")
        response.redirect('/handle_call')  # Retry if no input is detected

    return str(response)

def shutdown_server():
    """Shut down the Flask server gracefully."""
    print("Shutting down the server...")
    global server
    try:
        server.stop()  # Stop the gevent server
    except Exception as e:
        print(f"Error while stopping the server: {e}")
    finally:
        sys.exit(0)  # Exit the application

@app.before_request
def before_first_request():
    # Ensure that the required environment variables are set
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, openai.api_key]):
        raise ValueError("Required environment variables are missing.")

if __name__ == "__main__":
    # Set up logging and server
    app.logger.setLevel(logging.DEBUG)
    
    # Run Flask app
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    print("Server is running at http://localhost:5000")
    
    # Call the number to initiate the conversation
    make_call(os.getenv("TARGET_PHONE_NUMBER", Target Number))  # Use environment variable for the target number
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped manually.")
        sys.exit(0)
