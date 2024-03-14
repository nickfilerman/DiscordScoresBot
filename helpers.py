import requests
from bs4 import BeautifulSoup

'''
Gets matchups and scores for given sport and team gid, either current or recent, ongoing, and upcoming

:param sport: Which sport to filter by, 'all' if all sports
:param gid: Which team to look for by gid
:param now: True to only show ongoing games
:return: Dictionary, with the sport as the key, and the matches and scores as the value
'''
def getScores(sport: str, gid: str, now: bool=False) -> dict[str, str]:
  r = requests.get('https://statbroadcast.com/events/statmonitr.php?gid=' + gid)

  soup = BeautifulSoup(r.content, 'html.parser')

  s = soup.find('table', class_='table table-sm border border-secondary')
  s2 = s.find('tbody')

  classList = ['', 'bg-primary', 'bg-less-dark', 'text-muted', 'text-double-muted']
  if now:
    classList = ['bg-primary']

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

'''
Gets all available schools from statbroadcast to fill bot.schoolDict

:return: Dictionary, with the school's gid as the key, and the school's name as the value
'''
def getSchools() -> dict[str, str]:
  r = requests.get('https://www.statbroadcast.com/events/all.php')

  soup = BeautifulSoup(r.content, 'html.parser')
  s = soup.find_all('tr', class_='school')

  schoolDict = {}
  for row in s:
    s2 = row.find('a')
    schoolDict[s2.attrs['href'].split("=")[-1].lower()] = s2.text.replace(' ', '-').replace('.', '').replace('\'', '').replace('(', '').replace(')', '').lower()

  schoolDict.pop('test', None)
  return schoolDict

'''
Formats message to look nice in Discord

:param sportDict: Dictionary, with the sport as the key, and the matches and scores as the value
:return: A formatted string that will look nice in Discord as a message displaying the matches and scores by sport
'''
def prettier(sportDict: dict[str, str]) -> str:
  returnStr = ''
  for key, value in sportDict.items():
    returnStr = returnStr + '**' + key + '**\n'
    for item in value:
      returnStr = returnStr + item
    returnStr = returnStr + '\n'

  return returnStr
