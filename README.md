# AI-Powered Voice Assistant

This is a Flask-based AI-powered voice assistant that uses Twilio for phone calls and OpenAI's GPT model to generate conversational responses. The app greets users, listens to their speech, and replies with AI-generated responses using text-to-speech. For local development, **ngrok** is used to tunnel requests to the app.

## Features
- Makes phone calls using Twilio
- Uses OpenAI's GPT model to generate responses
- Responds via text-to-speech
- Built with Flask and Flask-Sockets
- Environment variables for secure API keys and phone numbers
- Uses ngrok for local development tunneling

## Prerequisites
Before running the app locally, ensure you have the following:
- A Twilio account and phone number
- An OpenAI account and API key
- Python 3.x and pip
- **ngrok** for local development tunneling

## Installation

### 1. Clone the repository:
```bash
git clone https://github.com/Manish-KT/outgoingcall--twilio-and-openai-.git
cd outgoingcall--twilio-and-openai-
```

### 2. Install the dependencies:
Create a virtual environment (optional but recommended) and install the necessary libraries.

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 3. Set up environment variables:
Create a `.env` file in the root of the project with the following content:

```env
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
OPENAI_API_KEY=your_openai_api_key
FLASK_SECRET_KEY=your_flask_secret_key
CALL_URL=http://your-ngrok-url/handle_call  # Use ngrok URL for local testing
TARGET_PHONE_NUMBER=+1234567890  # Replace with the target phone number
```

### 4. Start ngrok (for local development tunneling):
To expose your local Flask app to the public internet, use **ngrok**:

1. Download and install ngrok from [https://ngrok.com/](https://ngrok.com/).
2. Run ngrok to tunnel requests to your local Flask app:

```bash
ngrok http 5000
```

This will provide a public URL (e.g., `http://your-ngrok-url.ngrok.io`), which you can use for the `CALL_URL` in the `.env` file.

### 5. Run the app:
After setting up your environment and ngrok, you can run the Flask app with:

```bash
python app.py
```

By default, it will run on `http://localhost:5000`. Make sure to replace the `CALL_URL` in the `.env` file with the ngrok URL provided after starting ngrok.

## Troubleshooting

- Make sure your environment variables are set correctly.
- Ensure your Twilio account is active, and you've set the correct phone number and SID.
- If the app isn't responding, check the logs for errors:

```bash
tail -f logs/debug.log
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- [Twilio](https://www.twilio.com/) for the API to handle phone calls.
- [OpenAI](https://openai.com/) for the GPT-3.5 model.
- [Flask](https://flask.palletsprojects.com/) for the web framework.
- [Python-dotenv](https://pypi.org/project/python-dotenv/) for handling environment variables.
- [ngrok](https://ngrok.com/) for local development tunneling.
