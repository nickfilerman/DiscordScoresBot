import requests

from bs4 import BeautifulSoup

import discord
from discord.ext import commands

def getScores(sport, gid='msu', now=False):
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
      returnStr = s4[0].text + ' - ' +  s4[1].text.replace('\n', ' ').replace('FINAL', 'Final').replace(' -', '-').replace('--', '-').replace('\t', ' ')
      returnStr = returnStr + '\n'

      if s4[2].text.split('\n')[2] in sportDict:
        sportDict[s4[2].text.split('\n')[2]].append(returnStr)
      else:
        sportDict[s4[2].text.split('\n')[2]] = [returnStr]

  return sportDict

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

def prettier(sportDict):
  returnStr = ''
  for key, value in sportDict.items():
    returnStr = returnStr + key + '\n'
    for item in value:
      returnStr = returnStr + item
    returnStr = returnStr + '\n'

  return returnStr


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all(), help_command=None)

bot.schoolDict = {}
bot.botChannelID = None

@bot.event
async def on_ready():
  bot.channel = bot.get_channel(bot.botChannelID)
  bot.schoolDict = getSchools()

  await bot.channel.send(f'{bot.user.name} is online!')

@bot.event
async def on_command_error(message, error):
  if message.message.content[1] == '!':
    return
  
  if isinstance(error, commands.CommandNotFound):
    await message.send(str(error))
  else:
    await message.send('An Error Occurred. It is Likely that No Scores are Available at This Time')

  await bot.channel.send(str(error) + '\n\nCommand: ' + message.message.content)
  
@bot.command(name='score') 
async def score(message, sport='all'):
  returnStr = prettier(getScores(sport=sport))
  if returnStr == '':
    returnStr = 'No Scores Available'
  
  await message.send(returnStr)

@bot.command(name='nowScore')
async def nowScore(message, sport='all'):
  returnStr = prettier(getScores(sport=sport, now=True))
  if returnStr == '':
    returnStr = 'No Scores Available'

  await message.send(returnStr)

@bot.command(name='otherScore')
async def otherScore(message, gid='msu', sport='all'):
  if gid.lower() in bot.schoolDict:
    returnStr = prettier(getScores(sport=sport, gid=gid))
    if returnStr == '':
      returnStr = 'No Scores Available'

    await message.send(returnStr)
  else:
    await message.send('Not a Valid School GID, Check statbroadcast.com/events/all.php')

@bot.command(name='steve')
async def steve(message):
  await message.send('Yes')

@bot.command(name='help')
async def help(message):
  helpDict = {'score': 'Gets all recent and ongoing scores for MSU sports, add sport name to get only scores for that sport (example: !score basketball)\n\n',
              'nowScore': 'Gets all ongoing scores for MSU sports, add sport name to get only scores for that sport (example: !nowScore hockey)\n\n',
              'otherScore': 'Gets all ongoing scores for a given school\'s Sports, add sport name to get only scores for that sport (example: !otherScore msu football)\n    school name must be equal to the \'gid\' given by the school\'s relevant statbroadcast page, the list of schools can be found at statbroadcast.com/events/all.php\n\n',
              'steve': 'Says whether or not Steve has made a fieldgoal'}
  
  returnStr = '```help:\n'
  for helpCommand, helpDesc in helpDict.items():
    returnStr += '  ' + helpCommand + ': ' + helpDesc

  await message.send(returnStr + '\n```')
