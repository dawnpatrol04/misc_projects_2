def get_bot_user_id(app):
    """
    Get the bot user ID using the Slack API.
    Args:
        app (App): The Slack app instance.
    Returns:
        str: The bot user ID.
    """
    try:
        response = app.client.auth_test()
        return response["user_id"]
    except Exception as e:
        print(f"Error getting bot user ID: {e}")