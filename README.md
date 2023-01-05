Your personal Telegram bot that uses DALL-E on Deta Space. Send a prompt via Telegram, and Telemage will use DALL-E to generate an image, store it in Drive and send it back to you.

### Setup

1. Install the Telemage app on Deta Space.
2. In Telegram, open search, search for [Botfather](https://t.me/botfather) and add it as a contact. Talk to BotFather and create a Telegram bot (using the  `/newbot` command). BotFather will ask for a bot name and username, then it will give you a bot key.
3. Paste the bot key from BotFather into the `TELEGRAM` configuration variable on Space (to get to Configuration, click the `...`, then 'Settings' then 'Configuration' from the App's Tile on your Canvas).
4. Get an API key from [Open AI](https://beta.openai.com/account/api-keys). Input the Open AI API key into the `OPEN_AI` configuration variable on Space.
5. Open the Telemage App from your Canvas to setup the Webhook integration with Telegram.

You are now ready to use your Bot.

### Use

Add your bot (via the Bot's username from step 1) as a contact in Telegram. Start messaging it to interact with it. 

Visit [https://github.com/xeust/telemage](https://github.com/xeust/telemage) for the source.
