# Set Up

Clone GitHub Repo

Follow the steps [here](https://www.howtogeek.com/364225/how-to-make-your-own-discord-bot/) to create a Discord Bot account and get a token

## Dev Containers

If you would like to use a dev container, feel free to use the pre-supplied `.devcontainer/devcontainer.json`

This will automatically install Python 3.11 along with the necessary packages, as well as create the template `main.py` file

## Python Dependencies

Made using Python 3.11, may or may not work with other versions

```
pip3 install beautifulsoup4 requests discord
```

## main.py

Create `main.py` file within the project's root directory

```
from bot import bot

bot.botChannelID = 0
bot.defaultGid = ''

bot.run('')
```

Change the default values to match your information:

-   desiredChannelID is the channel id, as a number, where specific bot errors and wake-up message will be displayed

-   defaultGid is the default id, as a string, that the bot will use to fetch scores when none is provided

-   Place your discord bot token, as a string, for the parameter in `bot.run(...)`

## bot.py

Includes any bot commands that can be called by a Discord user

Feel free to change the `command_prefix`, `intents`, and `help_command` as desired within the arguments of the `Bot` constructor

## helpers.py

Includes any helper functions used by the bot. New functions used in `bot.py` must be imported

## Keep it Running

Find your own way to keep the discord bot running. There are services to do this for you for cheap, you can use the provided Dockerfile if you would like, or here is a useful bash command to stop and restart the bot detached in a CLI

```
botStart() {
  pkill -f main.py;
  nohup python3 location/to/directory/main.py &
}
```
