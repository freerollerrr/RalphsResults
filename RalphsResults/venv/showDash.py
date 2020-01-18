# call imports
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import calendar

import csv

external_stylesheets = ['https://codepen.io/hardtocrack/pen/qBEoQwM.css']

# -------- read in data from csvs and store them in dataframes ----------------
displayScores = pd.read_csv('score_table.csv')
displayScorePred = pd.read_csv('finalScorePred.csv')
displaybttsPred = pd.read_csv('finaloutputBTTS.csv')
# for score preds with dates broken down in day month and year column
displayScorePred2 = pd.read_csv('finalScorePred.csv')

# Sets all blank cells to NaN
displayScores.replace(r'\s+', np.nan, regex=True)

# Year and month selected for use in drop down option
dropDownDf = displayScorePred
# change date column to correct format
dropDownDf['Date'] = pd.to_datetime(dropDownDf['Date'], format='%Y/%m/%d')
dropDownDf['DAY'] = dropDownDf['Date'].dt.day
dropDownDf['MONTH'] = dropDownDf['Date'].dt.month
dropDownDf['YEAR'] = dropDownDf['Date'].dt.year

# Changing month to string format
dropDownDf['MONTH'] = dropDownDf['MONTH'].apply(lambda x: calendar.month_abbr[x])

# Values for drop down menu
year_indicators = dropDownDf['YEAR'].unique()
month_indicators = dropDownDf['MONTH'].unique()

# declare app
app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets, routes_pathname_prefix='/dash/')

# allow scripts to run locally
# app.scripts.config.serve_locally = False

# configure application to allow callback functions within multiple tabs
app.config['suppress_callback_exceptions'] = True

# define the layout for the application

app.layout = html.Div([

##Display Drop down Menu
    html.Div([
        html.Div(
            dcc.Dropdown(
                id='year_selector',
                options=[
                    {'label': i, 'value': i} for i in year_indicators
                ],
                value=2018
            ), className='year_selector'
        ),

## Month drop down display
        html.Div(
            dcc.Dropdown(
                id='month_selector',
                options=[
                    {'label': i, 'value': i} for i in month_indicators
                ],
                value='Aug'
            ), className='month_selector'
        )
    ]),

##Display Tables
    html.Div([
        html.Div([
            html.H2("Both Teams To Score Prediction"),
            html.Div(id='btts_table', style={'width': '100%'}),
        ], className='BTTS_Table'),

        html.Div([
            html.H2("Full Time Result Prediction"),
            html.Div(id='pred_scores_table'),

        ], className='FTRP_Table'),
    ], className='MultiTable'),

##Display Bar Charts/Pie Charts
    html.Div([
        html.H2("Home-Away-Total Goals by Team"),
        html.Div(dcc.Graph(id='score_bar')),

    ], className='goalBarDiv'),

    html.Div([
        html.Div([
            html.H4("Total Goals"),
            html.Div(dcc.Graph(id='score_pie', style={'height': '100vh', "width": "100%"})),
        ],
            className='pie_charts'
        ),

        html.Div([
            html.H4("Home Goals"),
            html.Div(dcc.Graph(id='home_score_pie', style={'height': '100vh', "width": "100%"})),
        ],

            className='pie_charts'
        ),

        html.Div([
            html.H4("Away Goals"),
            html.Div(dcc.Graph(id='away_score_pie', style={'height': '100vh', "width": "100%"})),
        ],
            className='pie_charts'
        ),
    ])
])


# Function to display tables based on user selection in the dropdown(MatchResults)
@app.callback(Output('goalStatsTable', 'children'),
              [Input('year_selector', 'value'),
               Input('month_selector', 'value')
               ])
def buildGoalTable(year, month):
    # Calls the build goal tablea
    goalOutputTable = constructDisplayScores(year, month)

    # count the total number of rows in the Dataframe
    num_rows = goalOutputTable.shape[0]

    # return a html table with the calculated figures
    return html.Table(
        [html.Tr([html.Th(col) for col in goalOutputTable.columns])] +
        [html.Tr([
            html.Td(goalOutputTable.iloc[i][col]) for col in goalOutputTable.columns
        ]) for i in range(min(len(goalOutputTable), num_rows))]
    )


#Function to display tables based on user selection in the dropdown(BTTS)
@app.callback(Output('btts_table', 'children'),
              [Input('year_selector', 'value'),
               Input('month_selector', 'value')
               ])
def buildBttsTable(year, month):
    # calls constructor
    bttsDisplayTable = constructDisplayBtts(year, month)

    dropDownBtts = bttsDisplayTable[
        (dropDownDf.MONTH == month) & (dropDownDf.YEAR == year)]

    # count the total number of rows in the Dataframe
    num_rows = dropDownBtts.shape[0]

    # Creates Table with calculed figures
    return html.Table(
        [html.Tr([html.Th(col) for col in dropDownBtts.columns])] +
        [html.Tr([
            html.Td(dropDownBtts.iloc[i][col]) for col in dropDownBtts.columns
        ]) for i in range(min(len(dropDownBtts), num_rows))]
    )


#Function to display tables based on user selection in the dropdown. Chose not to display these results
@app.callback(Output('pred_scores_table', 'children'),
              [Input('year_selector', 'value'),
               Input('month_selector', 'value')
               ])
def populate_pred_scores_table(year, month):
    # call the function that will construct the pred_scores_table
    pred_scores_table = constructDisplayPred(year, month)

    selected_pred_scores_table = pred_scores_table[
        (dropDownDf.MONTH == month) & (dropDownDf.YEAR == year)]

    # find the number of rows in the dataframe to use in creating the table
    num_rows = selected_pred_scores_table.shape[0]

    #Creates Table with calculed figures
    return html.Table(
        [html.Tr([html.Th(col) for col in selected_pred_scores_table.columns])] +
        [html.Tr([
            html.Td(selected_pred_scores_table.iloc[i][col]) for col in selected_pred_scores_table.columns
        ]) for i in range(min(len(selected_pred_scores_table), num_rows))]
    )


#Function to display Pie Charts
@app.callback(Output('score_pie', 'figure'),
              [Input('year_selector', 'value'),
               Input('month_selector', 'value')
               ])
def update_score_pie(year, month):
    # call the function that will construct the goalStatsTable
    goalStatsTable = constructDisplayScores(year, month)

    # set the labels and values for the pie chart
    pie_labels = (displayScores['Team'])
    pie_values = (displayScores['Total Goals'])

    # construct the pie chart
    pie_chart = go.Pie(values=pie_values, labels=pie_labels)

    return {
        'data': [pie_chart],
        'layout': {'showlegend': True}
    }


# Function to display home team goals pie chart
@app.callback(Output('home_score_pie', 'figure'),
              [Input('year_selector', 'value'),
               Input('month_selector', 'value')
               ])
def update_home_score_pie(year, month):
    # call the function that will construct the home goals
    goalStatsTable = constructDisplayScores(year, month)

    # set the labels and values for the pie chart
    pie_labels = (displayScores['Team'])
    pie_values = (displayScores['Total Home Goals'])

    # create pie chart
    pie_chart = go.Pie(values=pie_values, labels=pie_labels)

    return {
        'data': [pie_chart],
        'layout': {'showlegend': True}
    }

# Function to display Awaym goals pie chart
@app.callback(Output('away_score_pie', 'figure'),
              [Input('year_selector', 'value'),
               Input('month_selector', 'value')
               ])
def update_away_score_pie(year, month):
    # call the function that will construct goalStatsTable
    goalStatsTable = constructDisplayScores(year, month)

    # set the labels and values for the pie chart
    pie_labels = (displayScores['Team'])
    pie_values = (displayScores['Total Away Goals'])

    # construct the pie chart
    pie_chart = go.Pie(values=pie_values, labels=pie_labels)

    return {
        'data': [pie_chart],
        'layout': {'showlegend': True}
    }


#Finalresults saved to csv file
displayScorePred.to_csv("dataSetWithDates.csv", index=False)


# function that constructs the table used for the goalStatsTable
def constructDisplayScores(year, month):
    return displayScores


# function that constructs the table used for the btts_table
def constructDisplayBtts(year, month):
    return displaybttsPred


# function that constructs the table used for the pred_scores_table
def constructDisplayPred(year, month):
    return displayScorePred2


# Function to display bar charts for goals
@app.callback(Output('score_bar', 'figure'),
              [Input('year_selector', 'value'),
               Input('month_selector', 'value')
               ])
def scoreBarUpdate(year, month):
    return {
        'data': [
            go.Bar(
                x=displayScores['Team'],  # assign x as the dataframe column 'x'
                y=displayScores['Total Goals'],
                name='Total Goals'),

            go.Bar(
                x=displayScores['Team'],  # assign x as the dataframe column 'x'
                y=displayScores['Total Home Goals'],
                name='Total Home Goals'
            ),
            go.Bar(
                x=displayScores['Team'],  # assign x as the dataframe column 'x'
                y=displayScores['Total Away Goals'],
                name='Total Away Goals'
            )
        ],
    }


#CSS for the the display generated via codepen

if __name__ == '__main__':
    app.run_server(debug=True)
