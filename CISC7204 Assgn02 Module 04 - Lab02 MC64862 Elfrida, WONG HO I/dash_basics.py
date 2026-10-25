#Task1
# Import required packages
import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html

# Read the airline data into pandas dataframe
airline_data = pd.read_csv(
    'airline_data.csv',
    encoding='ISO-8859-1',
    dtype={'Div1Airport': str,'Div1TailNum': str,'Div2Airport': str,'Div2TailNum': str})

# Randomly sample 500 data points
data = airline_data.sample(n=500, random_state=42)

fig_data = (data.groupby('DistanceGroup')['Flights'].sum().reset_index())

# Create a pie chart
fig = px.pie(fig_data,values='Flights',names='DistanceGroup',title='Proportion of Distance Group by Flights')

#Task2&Task3&Task4&Task5
# Create a dash application
app = dash.Dash(__name__)

# Define the dashboard layout
app.layout = html.Div(children=[
   html.H1('Airline On-time Performance Dashboard',style={'textAlign': 'center','color': '#503D36','fontSize': 50}),
    html.P('Proportion of distance group (250 mile distance interval group) by flights.',
        style={'textAlign': 'center'}),
    dcc.Graph(figure=fig)])

# Run the application                   
if __name__ == '__main__':
    app.run(debug=True, port=8051)


