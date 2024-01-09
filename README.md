# Set Up

Clone GitHub Repo

Follow the steps [here](https://www.howtogeek.com/364225/how-to-make-your-own-discord-bot/) to create a Discord Bot account and get a token

## Python Dependencies 

Made using Python 3.11, may or may not work with other versions
```
pip install beautifulsoup4
pip install requests
```

## main.py

Place within the GitHub directory 
```
from bot import bot, setChannelID
setChannelID(desiredChannelID)

bot.run("TOKEN_GOES_HERE")
```

## Allow main.py to be executable

Linux example
```
sudo chmod +x main.py
```

## Keep it Running

Find your own way to keep the discord bot running. There are services to do this for you for cheap, I personally use a Raspberry Pi with the following bash command for simplicity
```
botStart() {
  pkill -f main.py;
  nohup python3 location/to/directory/main.py &
}
```
