## When program runs the following warning can be ignored:A value is trying to be set on a copy of a slice from a DataFrame.
# Try using .loc[row_indexer,col_indexer] = value instead


# Import statements
import csv
import pandas as pd

# Generates the initial csv file that we use to gather statistics
urlIn1 = 'https://www.football-data.co.uk/mmz4281/1819/E0.csv'
##Generates the list of fixtures to be used for comparison
urlIn2 = 'http://dedicatedexcel.com/wp-content/uploads/2018/08/00109_UK-Football-Fixtures-2018-19-by-Dedicated-Excel.xlsx'

##Stores the downloaded csv file in a dataframe
initialStats = pd.read_csv(urlIn1, header=0)
##Reset index
initialStats.reset_index(inplace=True)

##Sets all matches to both teams to score initially.
initialStats['Both Teams Scored'] = 'Yes'

##Sets the index for the table
initialStats.set_index('index')

##Repeated process for fixtures file.
initialFixtures = pd.read_csv('UpcomingFixturesTemp.csv', header=0)
initialFixtures.reset_index(inplace=True)
initialFixtures.set_index('index')

##checks for values fo 0 in fulltime home goals column and full time away goals and if found sets both teams to score to no
initialStats.loc[initialStats.FTHG == 0, 'Both Teams Scored'] = 'NO'
initialStats.loc[initialStats.FTAG == 0, 'Both Teams Scored'] = 'NO'

##Renames the required rows as not all stats are required
initialStats.rename(columns={'index': 'GameID', 'Div': 'League'}, inplace=True)
initialFixtures.rename(columns={'index': 'GameID', 'DIVISION': 'League', 'DATE': 'Date',
                                'TIME': 'Time', 'FIXTURE': 'Fixture', 'HOME TEAM': 'Home Team',
                                'AWAY TEAM': 'Away Team'}, inplace=True)

requiredColumn = ['GameID', 'League', 'Date', 'Fixture',
                  'Home Team', 'Away Team', 'BothTeamsToScore?']

requiredColumns2 = ['GameID', 'League', 'Date', 'Fixture',
                    'Home Team', 'Away Team', 'PredictedHomeScore', 'PredictedAwayScore']

requiredCoulumn3 = ['GameID', 'League', 'Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'HTHG', 'HTAG', 'HTR',
                    'Referee',
                    'HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'Both Teams Scored'
                    ]

initialFixtures['BothTeamsToScore?'] = ' '
initialFixtures['PredictedHomeScore'] = ' '
initialFixtures['PredictedAwayScore'] = ' '
##As we will only be using the premeir league information below removes anything not in that league
setLeague = initialFixtures[initialFixtures.League == 'EPL']
finalFix = setLeague[requiredColumns2]
finalBtts = setLeague[requiredColumn]
finalBtts['BTTS'] = '?'
##Data moved to csv file structures.
finalFix.to_csv("UpcomingFixtures.csv", index=False)
finalBtts.to_csv("UpcomingBTTS.csv", index=False)

finalStats = initialStats[requiredCoulumn3]
finalStats.to_csv("Stats.csv", index=False)
