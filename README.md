Your personal Telegram bot that uses DALL-E on Deta Space. Send a prompt via Telegram, and Telemage will use DALL-E to generate an image, store it in Drive and send it back to you.

### Setup

1. In Telegram, add Botfather as a contanct and create a Telegram bot (using the  `/newbot` command). It will ask for a bot username and Botfather will give you a bot key.
2. Paste the bot key into the `TELEGRAM` configuration variable on Space.
3. Input an Open AI API key into the `OPEN_AI` configuration variable on Space.
4. Visit the "/" route of the Space app to setup the Webhook with Telegram.

You are now ready to use your Bot.

### Use

Add your bot (via the Bot's username from step 1) as a contact in Telegram. Start messaging it to interact with it. 

Visit [https://github.com/xeust/telespace](https://github.com/xeust/telespace) for the source.
