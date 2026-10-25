import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update
import datetime as dt

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv")

df['Month'] = pd.to_datetime(df['Date']).dt.month_name()
df['Year'] = pd.to_datetime(df['Date']).dt.year

# TASK 2.1 - Add title to the dashboard
app.layout = html.Div(children=[
    html.H1('Australia Wildfire Dashboard',style={'textAlign': 'center','color': '#503D36','fontSize': 26}),
    # TASK 2.2 - Add Radio Items for Region Selection
    html.Div([html.Label('Select Region:', style={'fontSize': 20}),
              dcc.RadioItems(id='region',
                             options=[{'label': 'New South Wales', 'value': 'NSW'},{'label': 'Northern Territory', 'value': 'NT'},
                                      {'label': 'Queensland', 'value': 'QL'},{'label': 'South Australia', 'value': 'SA'},
                                      {'label': 'Tasmania', 'value': 'TA'},{'label': 'Victoria', 'value': 'VI'},
                                      {'label': 'Western Australia', 'value': 'WA'}],value='NSW')]),
    # TASK 2.3 - Add Year Dropdown
    html.Div([html.Label('Select Year:',style={'fontSize': 20}),
        dcc.Dropdown(id='year',options=[{'label': str(year), 'value': year}for year in range(2005, 2021)],
                     value=2005,clearable=False)], style={'width': '50%', 'marginTop': '20px'}),
    # TASK 2.4 - Add Pie Chart and Bar Chart
    html.Div([html.Div([dcc.Graph(id='pie-plot')], style={'width': '50%'}),
              html.Div([dcc.Graph(id='bar-plot')], style={'width': '50%'})], style={'display': 'flex'})])

# TASK 2.5 - Create Callback
@app.callback([Output('pie-plot', 'figure'),Output('bar-plot', 'figure')],[Input('region', 'value'),Input('year', 'value')])
def update_graph(selected_region, selected_year):
    filtered_df = df[(df['Region'] == selected_region) &(df['Year'] == selected_year)]
    monthly_fire_area = (filtered_df.groupby('Month')['Estimated_fire_area'].mean().reset_index())
    pie_fig = px.pie(monthly_fire_area,values='Estimated_fire_area',names='Month',title='Monthly Average Estimated Fire Area')
    monthly_fire_count = (filtered_df.groupby('Month')['Count'].mean().reset_index())
    bar_fig = px.bar(monthly_fire_count, x='Month', y='Count',title='Monthly Average Count of Fire Pixels',
                     labels={'Month': 'Month','Count': 'Average Fire Pixel Count'})
    return pie_fig, bar_fig

if __name__ == '__main__':
    app.run(debug=True, port=8056)