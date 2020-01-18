##Import Statements
import csv
import pandas as pd
import numpy as np

##prevents panda warning pop up
pd.options.mode.chained_assignment = None

# Generates new data frame from created csv stats.csv file from our generateData file.
newStats = pd.read_csv('Stats.csv', header=0)

##Sets the dataframe to only set values on required columns
newStats.rename(columns={'DivTest': 'League'})
newStats['BothTeamsScored'] = 'Yes'
# if either team did not score set both teams scored to no
newStats.loc[newStats.FTHG == 0, 'BothTeamsScored'] = 'No'
newStats.loc[newStats.FTAG == 0, 'BothTeamsScored'] = 'No'
yes = 'Yes'

# Count the amount of games played per team home and away. combine them for team totals
totalGames = newStats.HomeTeam.value_counts() + newStats.AwayTeam.value_counts()

totalGames = totalGames.to_frame().reset_index()

totalGames.columns = ['TEAM', 'GAMES_PLAYED']
##check for DS changes


##Declare new data frames to store fulltime home goals and fulltime away team goals. Below also specifies to only use yes when counting btts
bttsColumn = newStats[['HomeTeam', 'AwayTeam', 'BothTeamsScored']][(newStats.BothTeamsScored == yes)]
ftHgColumn = newStats[['HomeTeam', 'FTHG']]
ftAgColumn = newStats[['AwayTeam', 'FTAG']]

## Similiar to the generateData class here we count up home btts and away btts columns and combine them together for a new totalled Data Frame
bttsTotalDf = bttsColumn.HomeTeam.value_counts() + bttsColumn.AwayTeam.value_counts()
bttsTotalDf = bttsTotalDf.to_frame().reset_index()
bttsTotalDf.columns = [['TEAM', 'BothTeamsScored']]



# creates a dataframe to check the percentage of btts to be used for calculation purposes
bttsPercDf = pd.DataFrame()

bttsPercDf['TEAM'] = totalGames['TEAM']
bttsPercDf['GAMES_PLAYED'] = totalGames['GAMES_PLAYED']
bttsPercDf['BothTeamsScored'] = bttsTotalDf[['BothTeamsScored']]
bttsPercDf['Percentage'] = (bttsPercDf.BothTeamsScored / bttsPercDf.GAMES_PLAYED)

# for decimal places
precision = 3
# Uses precision to set the value for decimal places in bttsPercDf['Percentage']
bttsPercDf['Percentage'] = bttsPercDf['Percentage'].round(decimals=precision)
# New sorted dataframe
sortBttsPerc = bttsPercDf.sort_values(by='Percentage', ascending=False)

##Sets the file to csv format so can be reused in the dash file
bttsPercDf.to_csv("BTTSStats.csv", index=False)
# Allows us to show the teams with the largest btts percentage
# print(bttsPercDf.sort_values(by=['Percentage'],ascending=False))


# Calculates the FT home goals and the FT away home goals and then stores these in a total goalsfor calculation
totalFtGoals = ftHgColumn.FTHG.sum() + ftAgColumn.FTAG.sum()

##Creating Data Frame to work with Goal information
calcGoalsDf = pd.DataFrame()
calcGoalsDf['TEAM'] = totalGames['TEAM']
calcGoalsDf['GAMES_PLAYED'] = totalGames['GAMES_PLAYED']
# Calculating average number of goals
calcGoalsDf['Total Number of Goals'] = totalFtGoals
calcGoalsDf['Average Goals Per Game'] = totalFtGoals / calcGoalsDf.GAMES_PLAYED

##Creating dataframe to store Goals per team based on home and away stats.
results = pd.DataFrame()
results['HOME_TEAM'] = newStats['HomeTeam']
results['AWAY_TEAM'] = newStats['AwayTeam']
results['TotalHomeGoals'] = newStats['FTHG']
results['TotalAwayGoals'] = newStats['FTAG']

# Creates a data frame with the total home goals scored per team
homeTotGoalDf = results.groupby('HOME_TEAM', as_index=False).agg({'TotalHomeGoals': 'sum'})

# Creates a data frame with the total away goals scored per team
awayTotGoalDf = results.groupby('AWAY_TEAM', as_index=False).agg({'TotalAwayGoals': 'sum'})

# table for storing the goal stats for each team for the season Calculations done to set average goals pe
goalStatTotalsDf = pd.DataFrame()
goalStatTotalsDf['TEAM'] = homeTotGoalDf['HOME_TEAM']
goalStatTotalsDf['TotalHomeGoals'] = homeTotGoalDf['TotalHomeGoals']
goalStatTotalsDf['TotalAwayGoals'] = awayTotGoalDf['TotalAwayGoals']
goalStatTotalsDf['TotalGoals'] = homeTotGoalDf['TotalHomeGoals'] + awayTotGoalDf['TotalAwayGoals']
goalStatTotalsDf['AverageHomeGoals'] = goalStatTotalsDf['TotalHomeGoals'] / ((totalGames['GAMES_PLAYED'] / 2))
goalStatTotalsDf['AverageAwayGoals'] = goalStatTotalsDf['TotalAwayGoals'] / ((totalGames['GAMES_PLAYED'] / 2))
goalStatTotalsDf['AverageTotalGoals'] = goalStatTotalsDf['TotalGoals'] / totalGames['GAMES_PLAYED']




# Use UpcomingBTTS generated in generateData file to create a new Data Frame.
bttsDF = pd.read_csv('UpcomingBTTS.csv', header=0)
bttsDF['HomeBTTS'] = '?'
bttsDF['AwayBTTS'] = '?'



# create final score table from csv already created in other file
resultsPred = pd.read_csv('UpcomingFixtures.csv', header=0)
# temporarily make home score 1
resultsPred['PredictedHomeScore'] = 1
# rename columns
resultsPred.rename(columns={'Home Team': 'HomeTeam', 'Away Team': 'AwayTeam'}, inplace=True)
# finds the amount of columns based on the dataframe - dynamic - not needed in the end
num_cols = resultsPred.shape[1]

##Within each created table All the team names are required to match
# so that they can be used together. Below are the teams that where required to have the changes made
team1 = 'Fulham'
team2 = 'Brighton and Hove Albion'
team3 = 'Crystal Palace'
team4 = 'Cardiff City'
team5 = 'Wolverhampton Wanderers'
team6 = 'Huddersfield Town'
team7 = 'Manchester City'
team8 = 'West Ham United'
team9 = 'Leicester City'
team10 = 'Manchester United'
team11 = 'Tottenham Hotspur'
team12 = 'Newcastle United'

##Same as above. Specifying specific team names so that they can be refrenced.


goalStatTotalsDf['TEAM'][8] = 'Fulham'
goalStatTotalsDf['TEAM'][2] = 'BrightonHoveAlbion'
goalStatTotalsDf['TEAM'][6] = 'CrystalPalace'
goalStatTotalsDf['TEAM'][4] = 'CardiffCity'
goalStatTotalsDf['TEAM'][19] = 'WolverhamptonWanderers'
goalStatTotalsDf['TEAM'][9] = 'HuddersfieldTown'
goalStatTotalsDf['TEAM'][12] = 'ManchesterCity'
goalStatTotalsDf['TEAM'][18] = 'WestHamUnited'
goalStatTotalsDf['TEAM'][10] = 'LeicesterCity'
goalStatTotalsDf['TEAM'][13] = 'ManchesterUnited'
goalStatTotalsDf['TEAM'][16] = 'TottenhamHotspur'
goalStatTotalsDf['TEAM'][14] = 'Newcastle'

##Same as above. Specifying specific team names so that they can be refrenced.
bttsPercDf['TEAM'][8] = 'Fulham'
bttsPercDf['TEAM'][2] = 'BrightonHoveAlbion'
bttsPercDf['TEAM'][6] = 'CrystalPalace'
bttsPercDf['TEAM'][4] = 'CardiffCity'
bttsPercDf['TEAM'][19] = 'WolverhamptonWanderers'
bttsPercDf['TEAM'][9] = 'HuddersfieldTown'
bttsPercDf['TEAM'][12] = 'ManchesterCity'
bttsPercDf['TEAM'][18] = 'WestHamUnited'
bttsPercDf['TEAM'][10] = 'LeicesterCity'
bttsPercDf['TEAM'][13] = 'ManchesterUnited'
bttsPercDf['TEAM'][16] = 'TottenhamHotspur'
bttsPercDf['TEAM'][14] = 'Newcastle'


##get average home goals of home team in each game and put
##them in the output table (FinalScorePred)

## The loop below first checks goalStatTotalsDf for the team value. It then moves into the next loop and uses this as the home score predicted.
for i in range(0, len(resultsPred)):
    for j in range(4, 5):
        y = resultsPred.iloc[i][j]

        if y == team1:
            y = 'Fulham'

        if y == team2:
            y = 'BrightonHoveAlbion'

        if y == team3:
            y = 'CrystalPalace'

        if y == team4:
            y = 'CardiffCity'

        if y == team5:
            y = 'WolverhamptonWanderers'

        if y == team6:
            y = 'HuddersfieldTown'

        if y == team7:
            y = 'ManchesterCity'

        if y == team8:
            y = 'WestHamUnited'

        if y == team9:
            y = 'LeicesterCity'

        if y == team10:
            y = 'ManchesterUnited'

        if y == team11:
            y = 'TottenhamHotspur'

        if y == team12:
            y = 'Newcastle'
        #Here we set x to value of average home team goals to the team at y. We repeat the proccess in the loops below for the corresponding values required.
        x = goalStatTotalsDf.loc[goalStatTotalsDf['TEAM'] == y, 'AverageHomeGoals'].values[0]
        # Here we set the value of x to the desired column in the DF
        resultsPred.iloc[i, 6] = x

#Repeated process from above for the awaygoals column in the resultPred dataframe.

for i in range(0, len(resultsPred)):
    for j in range(5, 6):
        y = resultsPred.iloc[i][j]

        if y == team1:
            y = 'Fulham'

        if y == team2:
            y = 'BrightonHoveAlbion'

        if y == team3:
            y = 'CrystalPalace'

        if y == team4:
            y = 'CardiffCity'

        if y == team5:
            y = 'WolverhamptonWanderers'

        if y == team6:
            y = 'HuddersfieldTown'

        if y == team7:
            y = 'ManchesterCity'

        if y == team8:
            y = 'WestHamUnited'

        if y == team9:
            y = 'LeicesterCity'

        if y == team10:
            y = 'ManchesterUnited'

        if y == team11:
            y = 'TottenhamHotspur'

        if y == team12:
            y = 'Newcastle'
##Getting required Value
        x = goalStatTotalsDf.loc[goalStatTotalsDf['TEAM'] == y, 'AverageAwayGoals'].values[0]
##Setting required value to next column in dataframe.
        resultsPred.iloc[i, 7] = x

# Same process as above only here we begin to fill the bttsDF as required. This is setting the average home goals in that column.
for i in range(0, len(resultsPred)):
    for j in range(4, 5):
        y = resultsPred.iloc[i][j]
        # if y is not None:
        # print(y)
        if y == team1:
            y = 'Fulham'

        if y == team2:
            y = 'BrightonHoveAlbion'

        if y == team3:
            y = 'CrystalPalace'

        if y == team4:
            y = 'CardiffCity'

        if y == team5:
            y = 'WolverhamptonWanderers'

        if y == team6:
            y = 'HuddersfieldTown'

        if y == team7:
            y = 'ManchesterCity'

        if y == team8:
            y = 'WestHamUnited'

        if y == team9:
            y = 'LeicesterCity'

        if y == team10:
            y = 'ManchesterUnited'

        if y == team11:
            y = 'TottenhamHotspur'

        if y == team12:
            y = 'Newcastle'
## Sets the value of x for the team located at y
        x = bttsPercDf.loc[bttsPercDf['TEAM'] == y, 'Percentage'].values[0]
## Sets x value in the required column
        bttsDF.iloc[i, 8] = x

# Same process as above only here we begin to fill the bttsDF as required. This is setting the average home goals in that column.

for i in range(0, len(resultsPred)):
    for j in range(5, 6):
        y = resultsPred.iloc[i][j]
        # print(y)

        if y == team1:
            y = 'Fulham'

        if y == team2:
            y = 'BrightonHoveAlbion'

        if y == team3:
            y = 'CrystalPalace'

        if y == team4:
            y = 'CardiffCity'

        if y == team5:
            y = 'WolverhamptonWanderers'

        if y == team6:
            y = 'HuddersfieldTown'

        if y == team7:
            y = 'ManchesterCity'

        if y == team8:
            y = 'WestHamUnited'

        if y == team9:
            y = 'LeicesterCity'

        if y == team10:
            y = 'ManchesterUnited'

        if y == team11:
            y = 'TottenhamHotspur'

        if y == team12:
            y = 'Newcastle'

        x = bttsPercDf.loc[bttsPercDf['TEAM'] == y, 'Percentage'].values[0]
        bttsDF.iloc[i, 9] = x


#Below we now use the average btts to score figure for home and away team
## We add the two averages together and if the result returns greater than 50 for the pair the result is Yes for btts
# we set the value to yes.
bttsDF['BTTS'] = (bttsDF['HomeBTTS'] + bttsDF['AwayBTTS']) / 2
# check back here Kenneth
higherThanFifty = bttsDF['BTTS'] >= 0.5
lowerThanFifty = bttsDF['BTTS'] < 0.5


# depending on whether the result returns greater than 50 the yes or no is placed in the new BothTeamsToScore Column
bttsDF['BothTeamsToScore?'][higherThanFifty] = 'Yes'
bttsDF['BothTeamsToScore?'][lowerThanFifty] = 'No'

# Create Final BTTS Table
displayBtts = bttsDF
# Remove unwanted columns for display purposes
displayBtts = displayBtts.drop('HomeBTTS', 1)
displayBtts = displayBtts.drop('AwayBTTS', 1)
resultsPred = resultsPred.drop('GameID', 1)
displayBtts = displayBtts.drop('GameID', 1)



# change score columns to ints so they can be rounded
resultsPred[['PredictedHomeScore']] = resultsPred[['PredictedHomeScore']].astype(int)
resultsPred[['PredictedAwayScore']] = resultsPred[['PredictedAwayScore']].astype(int)
##round score columns
resultsPred['PredictedHomeScore'] = resultsPred['PredictedHomeScore'].round(decimals=0)
resultsPred['PredictedAwayScore'] = resultsPred['PredictedAwayScore'].round(decimals=0)
# round percentage column
bttsPercDf['Percentage'] = bttsPercDf['Percentage'].round(2)


# for rounding
# Remove unwanted columns for display purposes
displayBtts = displayBtts.drop('Home Team', 1)
displayBtts = displayBtts.drop('Away Team', 1)
resultsPred = resultsPred.drop('HomeTeam', 1)
resultsPred = resultsPred.drop('AwayTeam', 1)
# rename column
displayBtts = displayBtts.rename(columns={'BothTeamsToScore?': 'Will BTS?'})


# converts the decimals to percentage format
displayBtts[['BTTS']] = displayBtts[['BTTS']] * 100
bttsPercDf[['Percentage']] = bttsPercDf[['Percentage']] * 100


homeWin = resultsPred['PredictedHomeScore'] > resultsPred['PredictedAwayScore']
awayWin = resultsPred['PredictedHomeScore'] < resultsPred['PredictedAwayScore']
draw = resultsPred['PredictedHomeScore'] == resultsPred['PredictedAwayScore']


##Testing for predicted result. sets all values to test
resultsPred['NewResults'] = 'Test'
#
# if resultsPred['PredictedHomeScore'].values[0] > 2:
#     print('test')

homeWin = homeWin.astype(int)


for i in range(0, len(resultsPred)):
    for j in range(3, 4):


        resultsPred.iloc[i, resultsPred.columns.get_loc('NewResults')] \
            = np.where(resultsPred.iloc[i, resultsPred.columns.get_loc('PredictedHomeScore')]
                       > resultsPred.iloc[i, resultsPred.columns.get_loc('PredictedAwayScore')], 'Home Win', (
                           np.where(resultsPred.iloc[i, resultsPred.columns.get_loc('PredictedAwayScore')] >
                                    resultsPred.iloc[i, resultsPred.columns.get_loc('PredictedHomeScore')],
                                    'Away Win', 'Draw')))

newshowytable = resultsPred
resultsPred = resultsPred.drop('PredictedHomeScore', 1)
resultsPred = resultsPred.drop('PredictedAwayScore', 1)

#

# Sets column names for display purposes
displayBtts = displayBtts.rename(columns={'BTTS': 'BTTS%'})
resultsPred = resultsPred.rename(
    columns={'PredictedHomeScore': 'Predicted Home Score', 'PredictedAwayScore': 'Predicted Away Score'})
displayBtts = displayBtts.rename(columns={'BothTeamsToScore?': 'Will Both Teams Score'})
bttsPercDf = bttsPercDf.rename(columns={'Percentage': 'Games Played Where BTS%'})
bttsPercDf = bttsPercDf.rename(columns={'BothTeamsScored': 'Games Played Where BTS'})
goalStatTotalsDf = goalStatTotalsDf.rename(columns={'TEAM': 'Team', 'TotalHomeGoals': 'Total Home Goals',
                                          'TotalAwayGoals': 'Total Away Goals',
                                          'TotalGoals': 'Total Goals',
                                          'AverageHomeGoals': 'Average Home Goals',
                                          'AverageAwayGoals': 'Average Away Goals',
                                          'AverageTotalGoals': 'Average Total Goals',
                                                    })
displayBtts['BTTS%'] = displayBtts['BTTS%'].astype(float)
displayBtts['BTTS%'] = displayBtts['BTTS%'].round(2)

#Creates the required CSV files from the dataframes to be used in the final dash file.py.
resultsPred.to_csv("finalScorePred.csv", index=False)
displayBtts.to_csv("finaloutputBTTS.csv", index=False)
goalStatTotalsDf.to_csv("score_table.csv", index=False)
bttsPercDf.to_csv("btsStats.csv", index=False)


