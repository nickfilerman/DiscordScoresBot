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

:param ctx: The context surrounding the message sent for the command that contained an error
:param error: The error itself
'''
@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
  if ctx.message.content[1] == '!':
    return
  
  await bot.channel.send(str(error) + '\n\nCommand: ' + ctx.message.content)
  
  if isinstance(error, commands.CommandNotFound):
    await ctx.send(str(error))
  else:
    await ctx.send('An Error Occurred. It is Likely that No Scores are Available at This Time')

'''
Syncs hybrid_commands with Discord to use for slash commands (validates user first)

:param ctx: The context surrounding the message sent to request syncing
'''
@bot.command(name='sync')
async def sync(ctx: commands.Context):
  if (ctx.permissions.administrator):
    try:
      synced = await bot.tree.sync()
      await bot.channel.send(f'Synced {len(synced)} commands') 
    except:
      await bot.channel.send('Error syncing')
  else:
    await ctx.send('Command "sync" is not found')
  
'''
Gets the score for the default gid and given sport (or all sports) and returns as message

:param ctx: The context surrounding the message sent for the command
:param sport: What sport to filter the scores for, default is "all" if you want all sports
'''
@bot.hybrid_command(name='score') 
async def score(ctx: commands.Context, sport: str='all'):
  returnStr = prettier(getScores(sport=sport, gid=bot.defaultGid))
  if returnStr == '':
    returnStr = 'No Scores Available'
  
  await ctx.send(returnStr)

'''
Gets the score for the default gid and given sport (or all sports) that are currently ongoing and returns as message

:param ctx: The context surrounding the message sent for the command
:param sport: What sport to filter the scores for, default is "all" if you want all sports
'''
@bot.hybrid_command(name='now_score')
async def now_score(ctx: commands.Context, sport: str='all'):
  returnStr = prettier(getScores(sport=sport, gid=bot.defaultGid, now=True))
  if returnStr == '':
    returnStr = 'No Scores Available'

  await ctx.send(returnStr)

'''
Gets the score for another team (defaults to default gid) and given sport (or all sports) and returns as message

:param ctx: The context surrounding the message sent for the command
:param gid: What gid to get the scores from, gets set to bot.defaultGid if nothing is passed
:param sport: What sport to filter the scores for, default is "all" if you want all sports
'''
@bot.hybrid_command(name='other_score')
async def other_score(ctx: commands.Context, gid: str='', sport: str='all'):
  if gid == '':
    gid = bot.defaultGid

  if gid.lower() in bot.schoolDict:
    returnStr = prettier(getScores(sport=sport, gid=gid))
    if returnStr == '':
      returnStr = 'No Scores Available'

    await ctx.send(returnStr)
  else:
    await ctx.send('Not a Valid School GID, Check statbroadcast.com/events/all.php')

'''
Returns as message, descriptions for each command available with formatting

:param ctx: The context surrounding the message sent for the command
'''
@bot.hybrid_command(name='help')
async def help(ctx: commands.Context):
  helpDict = {'score': 'Gets all recent and ongoing scores for ' + bot.defaultGid + ' sports, add sport name to get only scores for that sport (example: !score basketball)\n\n',
              'now_score': 'Gets all ongoing scores for ' + bot.defaultGid + ' sports, add sport name to get only scores for that sport (example: !nowScore hockey)\n\n',
              'other_score': 'Gets all ongoing scores for a given school\'s Sports, add sport name to get only scores for that sport (example: !otherScore ' + bot.defaultGid + ' football)\n    school name must be equal to the \'gid\' given by the school\'s relevant statbroadcast page, the list of schools can be found at statbroadcast.com/events/all.php'}
  
  returnStr = '```help:\n'
  for helpCommand, helpDesc in helpDict.items():
    returnStr += '  ' + helpCommand + ': ' + helpDesc

  await ctx.send(returnStr + '\n```')
