# Morning Bot

Morning bot is a discord bot that runs every 24 hours to send me needed information. It uses: 

* Open Weather API for weather statistics
* Google Calender API for upcoming events and workouts
* Discord.py for building the bot

---
## Setup
### 1. Creating a discord bot
1. Go to the [discord developer portal](https://discord.com/developers/applications) and sign in with discord
2. Click the "new application" button in the top right and enter a name
    1.  make note of the application id, you will need this for later
3. Open up the side panel and click "bot". Click the "add bot" button. 
    1. make note of the token, you will need this for later
4. Settings
    1.  You can either leave on or turn off the "Public bot" setting, it doesn't matter. 
    2. Leave off the "Requires OAUTH2 CODE GRANT setting"
    3. Privileged Gateway Intents
        1. "Presense Intent" can be turned on or off, doesn't matter
        2. "Server Member Intent" must be turned on
        3. "Message Content Intent" mustbe turned on
5. Inviting the both
    1. Open the side panel and switch to the OAuth2 Link generator section
    2. Under scopes enable, "bot", and "applications.commands"
    3. Under General Permissions enable "Administrator"
    4. Copy and paste the generated URL into a new tab and add the bot to a server of your choosing.
        1. *note: you must have the needed permissions on whatever server you would like to add the bot too


### 2. API Config
1. Start by cloning `config.example.yml` as `config.yml`
```bash
 cp config.example.yml config.yml
```
2. Fill in the sections of config.yml 
 
   1. API/clientid: this is the discord id of your bot. You can get this either through the [discord developer portal](https://discord.com/developers/applications) or by enabling developer mode in discord settings, right clicking on your bot, and copying the id
   2. API/ownerid: this is the discord id of the owner (ie you). This can be obtained by enabling developer mode in discord, right clicking on yourself and selecting copy-id 
   3. API/guildid: this is the discord id of the guild (server) you will be using the bot in. This can be obtained by turning on developer mode in discord, right clicking on the server name, and selecting copy id.
   4. API/token: this is the token of your discord bot. This can be obtained by going to the [discord developer portal](https://discord.com/developers/applications), selecting your application, selecting "bot", and clicking copy token.
   5. API/key: this is your open weather api key. This can be obtained by going to [openweather.org](https://openweathermap.org),  creating an account, and making an API key.
   6. API/lat and API/long: this is the latitude and longitude of your house/office/etc. This can be obtained through some googling
   7. Google Calender API: follow the instructions on [this](https://developers.google.com/calendar/api/quickstart/python) page. Make sure you create a project and enable the google calender API. Once you have done that open the side panel in your google cloud console. Find APIs & Services and select "Credentials" from the menu that appears. Click "Create Credentials" and select a type of "OAuth client ID". The application type is "Desktop App". Give it a name and download the given json file to the directory of the project. Rename it to `credentials.json`.
## 3. Starting the project
Once you have setup the needed API's and entered the needed information into `config.yml` all you have to do it run:
```bash
python src/morning.py
```
The task will start immediately then wait 24hours before starting again. Make sure when you run the start command that time is when you want to recieve your messages. 
