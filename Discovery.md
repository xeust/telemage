---
title: "telemage"
tagline: "generating images with ai from your phone"
theme_color: "#800080"
git: "https://github.com/xeust/telemage"
---

👅

send a message on telegram, get an image back. 

powered by DALL·E 2 & space.

images stored in a deta drive for you to use l8er.

### setup

1. install telemage.
2. in telegram, open search & search for [botfather](https://t.me/botfather). talk to it to create a telegram bot (use `/newbot`). botfather will give you that bot key.
3. paste that bot key into the `TELEGRAM` config variable (from your telemage tile on canvas, click the `...`, then 'settings' then 'configuration').
4. get an API key from [open ai](https://beta.openai.com/account/api-keys). input the API key into the `OPEN_AI` configuration variable (see above).
5. open your app and visit the "setup" view. click the "setup webhook" button to setup the webhook  with telegram.
6. message your bot "/chatid" to get your chat id.
7. open the app again and visit the "authorize" view. add the chat id with the button.

you are now readdddy to jump around with some images.

### use

add your bot as a contact in telegram. 

message your bot. get an image back.

visit [https://github.com/xeust/telespace](https://github.com/xeust/telespace) for the source.