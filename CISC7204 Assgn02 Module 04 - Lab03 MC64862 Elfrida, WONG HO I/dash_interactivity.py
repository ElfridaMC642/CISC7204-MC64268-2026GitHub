# TASK 1 - Read the Data
# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

airline_data = pd.read_csv('airline_data.csv',encoding='ISO-8859-1',
    dtype={'Div1Airport': str,'Div1TailNum': str,'Div2Airport': str,'Div2TailNum': str})

# TASK 2
# Create a Dash application
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('Airline Performance Dashboard',style={'textAlign': 'center','color': '#503D36','fontSize': 40}),
    html.Div(["Input Year: ",dcc.Input(id='input-year',value=2010,type='number',min=2010,max=2020)]),
    html.Div([dcc.Graph(id='line-plot')])
])

# TASK 3 - Add Callback
@app.callback(
    Output('line-plot', 'figure'),
    Input('input-year', 'value'))
    
def get_graph(entered_year):
    df = airline_data[airline_data['Year'] == int(entered_year)]
    line_data = (df.groupby('Month')['ArrDelay'].mean().reset_index())
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=line_data['Month'],y=line_data['ArrDelay'],mode='lines+markers'))
    fig.update_layout(title='Average Monthly Arrival Delay',xaxis_title='Month',yaxis_title='Average Arrival Delay')
    return fig

if __name__ == '__main__':
    app.run(debug=True, port=8052)