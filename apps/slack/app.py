import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import find_dotenv, load_dotenv

from slack_util import get_bot_user_id
# from functions import slack_assistant
import jira_agent

load_dotenv(find_dotenv())


SLACK_BOT_TOKEN=os.environ["SLACK_BOT_TOKEN"]  # xoxb
SLACK_APP_TOKEN=os.environ["SLACK_APP_TOKEN"]  # xapp


app = App(token=SLACK_BOT_TOKEN)


@app.event("message")
def handle_message_events(body, say, logger):
    try:
        # Log the body of the event to understand its structure and contents
        logger.info(body)

        # You can process the message here and send a response if needed
        if 'subtype' not in body['event']:  # Check if the message is a standard message sent by a user
            text = body['event']['text']  # Extract the text from the message event
            say(text=jira_agent.agents(text) )  # Echoes back the received message
    except Exception as e:
        logger.error(f"Error handling message event: {e}")

# Initialize Socket Mode handler
if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
