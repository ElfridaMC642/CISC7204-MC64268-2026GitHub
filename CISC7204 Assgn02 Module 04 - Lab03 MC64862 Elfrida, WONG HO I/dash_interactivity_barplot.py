# TASK 4 - Practice Exercise
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

airline_data = pd.read_csv('airline_data.csv',encoding='ISO-8859-1',dtype={
        'Div1Airport': str,'Div1TailNum': str,'Div2Airport': str,'Div2TailNum': str})

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('Total number of flights to the destination state split by reporting airline',
        style={'textAlign': 'center','color': '#503D36','fontSize': 40}),
    html.Div(children=["Input Year: ",dcc.Input(id='input-year',value=2010,type='number',style={'height': '50px','fontSize': 35})],
        style={'fontSize': 40}),
    html.Div([dcc.Graph(id='bar-plot')])])

@app.callback(
    Output('bar-plot', 'figure'),
    Input('input-year', 'value'))
def get_bar_chart(entered_year):
    df = airline_data[airline_data['Year'] == int(entered_year)]
    bar_data = (df.groupby(['DestState', 'Reporting_Airline'])['Flights'].sum().reset_index())
    fig = px.bar(bar_data,x='DestState',y='Flights',color='Reporting_Airline',
        title='Total number of flights to the destination state split by reporting airline')
    return fig

if __name__ == '__main__':
    app.run(debug=True, port=8053)