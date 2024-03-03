import requests

from bs4 import BeautifulSoup

import discord
from discord.ext import commands

''' Bot setup '''

# Instantiates bot object
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all(), help_command=None)

# Establishes default values to be overridden in main.py
bot.botChannelID = None
bot.defaultGid = ''

''' Helper functions for bot '''

# Gets scores for given sport and team
# If sport is all, gets all sports
# If now is true, only gets ongoing games
def getScores(sport, gid, now=False):
  r = requests.get('https://statbroadcast.com/events/statmonitr.php?gid=' + gid)

  soup = BeautifulSoup(r.content, 'html.parser')

  s = soup.find('table', class_='table table-sm border border-secondary')
  s2 = s.find('tbody')

  classList = ['bg-primary', 'bg-less-dark', 'text-muted', 'text-double-muted']
  if not now:
    classList.append('')

  s3 = s2.find_all('tr', {'class': classList})

  sportDict = {}
  for row in s3:
    s4 = row.find_all('td')

    if (sport.lower() in s4[2].text.lower() or sport == 'all'):
      returnStr = s4[0].text + ' - ' +  s4[1].text.replace('\t', '').replace('\n', ' ').replace('FINAL', 'Final').replace('--', '-').replace('  ', ' ')
      returnStr = " ".join(returnStr.split())
      returnStr = returnStr + '\n'

      if s4[2].text.split('\n')[2] in sportDict:
        sportDict[s4[2].text.split('\n')[2]].append(returnStr)
      else:
        sportDict[s4[2].text.split('\n')[2]] = [returnStr]

  return sportDict

# Gets all available schools from statbroadcast to fill bot.schoolDict
def getSchools():
  r = requests.get('https://www.statbroadcast.com/events/all.php')

  soup = BeautifulSoup(r.content, 'html.parser')
  s = soup.find_all('tr', class_='school')

  schoolDict = {}
  for row in s:
    s2 = row.find('a')
    schoolDict[s2.attrs['href'].split("=")[-1].lower()] = s2.text.replace(' ', '-').replace('.', '').replace('\'', '').replace('(', '').replace(')', '').lower()

  schoolDict.pop('test', None)
  return schoolDict

# Formats message to look nice in Discord
def prettier(sportDict):
  returnStr = ''
  for key, value in sportDict.items():
    returnStr = returnStr + '**' + key + '**\n'
    for item in value:
      returnStr = returnStr + item
    returnStr = returnStr + '\n'

  return returnStr

''' Bot Events '''


# Sets up bot and messages bot channel that it is online
@bot.event
async def on_ready():
  bot.channel = bot.get_channel(bot.botChannelID)
  bot.schoolDict = getSchools()

  await bot.channel.send(f'{bot.user.name} is online!')

# Sends error message to bot chonnel, on error
@bot.event
async def on_command_error(message, error):
  if message.message.content[1] == '!':
    return
  
  if isinstance(error, commands.CommandNotFound):
    await message.send(str(error))
  else:
    await message.send('An Error Occurred. It is Likely that No Scores are Available at This Time')

  await bot.channel.send(str(error) + '\n\nCommand: ' + message.message.content)
  
# Gets the score for the default gid and given sport (or all sports) and returns as message
@bot.command(name='score') 
async def score(message, sport='all'):
  returnStr = prettier(getScores(sport=sport, gid=bot.defaultGid))
  if returnStr == '':
    returnStr = 'No Scores Available'
  
  await message.send(returnStr)

# Gets the score for the default gid and given sport (or all sports) that are currently ongoing and returns as message
@bot.command(name='nowScore')
async def nowScore(message, sport='all'):
  returnStr = prettier(getScores(sport=sport, gid=bot.defaultGid, now=True))
  if returnStr == '':
    returnStr = 'No Scores Available'

  await message.send(returnStr)

# Gets the score for another team (defaults to default gid) and given sport (or all sports) and returns as message
@bot.command(name='otherScore')
async def otherScore(message, gid='', sport='all'):
  if gid == '':
    gid = bot.defaultGid

  if gid.lower() in bot.schoolDict:
    returnStr = prettier(getScores(sport=sport, gid=gid))
    if returnStr == '':
      returnStr = 'No Scores Available'

    await message.send(returnStr)
  else:
    await message.send('Not a Valid School GID, Check statbroadcast.com/events/all.php')

# Returns as message, descriptions for each command available with formatting
@bot.command(name='help')
async def help(message):
  helpDict = {'score': 'Gets all recent and ongoing scores for ' + bot.defaultGid + ' sports, add sport name to get only scores for that sport (example: !score basketball)\n\n',
              'nowScore': 'Gets all ongoing scores for ' + bot.defaultGid + ' sports, add sport name to get only scores for that sport (example: !nowScore hockey)\n\n',
              'otherScore': 'Gets all ongoing scores for a given school\'s Sports, add sport name to get only scores for that sport (example: !otherScore msu football)\n    school name must be equal to the \'gid\' given by the school\'s relevant statbroadcast page, the list of schools can be found at statbroadcast.com/events/all.php'}
  
  returnStr = '```help:\n'
  for helpCommand, helpDesc in helpDict.items():
    returnStr += '  ' + helpCommand + ': ' + helpDesc

  await message.send(returnStr + '\n```')
