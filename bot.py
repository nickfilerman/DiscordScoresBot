import discord
from helpers import getScores, getSchools, prettier
from discord.ext import commands

# Instantiates bot
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all(), help_command=None)

'''
Sets up bot and messages bot channel that it is online
'''
@bot.event
async def on_ready():
  bot.channel = bot.get_channel(bot.botChannelID)
  bot.schoolDict = getSchools()

  await bot.channel.send(f'{bot.user.name} is online!')

'''
Sends error message to bot chonnel, on error

:param message: Message sent that contained the error
:param error: The error itself
'''
@bot.event
async def on_command_error(message, error):
  if message.message.content[1] == '!':
    return
  
  if isinstance(error, commands.CommandNotFound):
    await message.send(str(error))
  else:
    await message.send('An Error Occurred. It is Likely that No Scores are Available at This Time')

  await bot.channel.send(str(error) + '\n\nCommand: ' + message.message.content)
  
'''
Gets the score for the default gid and given sport (or all sports) and returns as message

:param message: The message and relevant information provided with the message
:param sport: What sport to filter the scores for, default is "all" if you want all sports
'''
@bot.hybrid_command(name='score') 
async def score(message, sport='all'):
  returnStr = prettier(getScores(sport=sport, gid=bot.defaultGid))
  if returnStr == '':
    returnStr = 'No Scores Available'
  
  await message.send(returnStr)

'''
Gets the score for the default gid and given sport (or all sports) that are currently ongoing and returns as message

:param message: The message and relevant information provided with the message
:param sport: What sport to filter the scores for, default is "all" if you want all sports
'''
@bot.hybrid_command(name='nowScore')
async def nowScore(message, sport='all'):
  returnStr = prettier(getScores(sport=sport, gid=bot.defaultGid, now=True))
  if returnStr == '':
    returnStr = 'No Scores Available'

  await message.send(returnStr)

'''
Gets the score for another team (defaults to default gid) and given sport (or all sports) and returns as message

:param message: The message and relevant information provided with the message
:param gid: What gid to get the scores from, gets set to bot.defaultGid if nothing is passed
:param sport: What sport to filter the scores for, default is "all" if you want all sports
'''
@bot.hybrid_command(name='otherScore')
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

'''
Returns as message, descriptions for each command available with formatting

:param message: The message and relevant information provided with the message
'''
@bot.hybrid_command(name='help')
async def help(message):
  helpDict = {'score': 'Gets all recent and ongoing scores for ' + bot.defaultGid + ' sports, add sport name to get only scores for that sport (example: !score basketball)\n\n',
              'nowScore': 'Gets all ongoing scores for ' + bot.defaultGid + ' sports, add sport name to get only scores for that sport (example: !nowScore hockey)\n\n',
              'otherScore': 'Gets all ongoing scores for a given school\'s Sports, add sport name to get only scores for that sport (example: !otherScore ' + bot.defaultGid + ' football)\n    school name must be equal to the \'gid\' given by the school\'s relevant statbroadcast page, the list of schools can be found at statbroadcast.com/events/all.php'}
  
  returnStr = '```help:\n'
  for helpCommand, helpDesc in helpDict.items():
    returnStr += '  ' + helpCommand + ': ' + helpDesc

  await message.send(returnStr + '\n```')
