# TASK 1 - Read the Data
# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

airline_data = pd.read_csv('airline_data.csv',encoding='ISO-8859-1',
    dtype={'Div1Airport': str,'Div1TailNum': str,'Div2Airport': str,'Div2TailNum': str})

# TASK 2 - Create Dash Application
app = dash.Dash(__name__)
# Define the dashboard layout
app.layout = html.Div(children=[
    html.H1('Flight Delay Time Statistics',style={'textAlign': 'center','color': '#503D36','fontSize': 30}),
    html.Div(["Input Year: ",dcc.Input(id='input-year',value=2010,type='number',min=2010,max=2020)]),
    html.Div([html.Div([html.Div(dcc.Graph(id='carrier-plot'),style={'width': '50%'}),
        html.Div(dcc.Graph(id='weather-plot'),style={'width': '50%'})], style={'display': 'flex'}),
     html.Div([html.Div(dcc.Graph(id='nas-plot'),style={'width': '50%'}),
        html.Div(dcc.Graph(id='security-plot'),style={'width': '50%'})], style={'display': 'flex'}),
    dcc.Graph(id='late-plot')])])
    
# TASK 3 - Create Callback
@app.callback([Output('carrier-plot', 'figure'),Output('weather-plot', 'figure'),Output('nas-plot', 'figure'),
               Output('security-plot', 'figure'),Output('late-plot', 'figure')],Input('input-year', 'value'))

def get_graph(entered_year):
    df = airline_data[airline_data['Year'] == int(entered_year)]
    avg_carrier = (df.groupby(['Month', 'Reporting_Airline'])['CarrierDelay'].mean().reset_index())
    avg_weather = (df.groupby(['Month', 'Reporting_Airline'])['WeatherDelay'].mean().reset_index())
    avg_nas = (df.groupby(['Month', 'Reporting_Airline'])['NASDelay'].mean().reset_index())
    avg_security = (df.groupby(['Month', 'Reporting_Airline'])['SecurityDelay'].mean().reset_index())
    avg_late = (df.groupby(['Month', 'Reporting_Airline'])['LateAircraftDelay'].mean().reset_index())
    
    # Carrier Delay line chart
    carrier_fig = go.Figure()
    carrier_fig.add_trace(go.Scatter(x=avg_carrier['Month'],y=avg_carrier['CarrierDelay'],mode='lines+markers',name='Carrier Delay'))
    carrier_fig = px.line(avg_carrier,x='Month',y='CarrierDelay',color='Reporting_Airline',markers=True,
                          title='Average Carrier Delay by Month')
    carrier_fig.update_layout(xaxis_title='Month',yaxis_title='Average Delay (Minutes)')
    # Weather Delay line chart
    weather_fig = go.Figure()
    weather_fig.add_trace(go.Scatter(x=avg_weather['Month'],y=avg_weather['WeatherDelay'],mode='lines+markers',name='Weather Delay'))
    weather_fig = px.line(avg_weather,x='Month',y='WeatherDelay',color='Reporting_Airline',markers=True,
                          title='Average Weather Delay by Month')
    weather_fig.update_layout(xaxis_title='Month',yaxis_title='Average Delay (Minutes)')
    # NAS Delay line chart
    nas_fig = go.Figure()
    nas_fig.add_trace(go.Scatter(x=avg_nas['Month'],y=avg_nas['NASDelay'],mode='lines+markers',name='NAS Delay'))
    nas_fig = px.line(avg_nas,x='Month',y='NASDelay',color='Reporting_Airline',markers=True,title='Average NAS Delay by Month')
    nas_fig.update_layout(xaxis_title='Month',yaxis_title='Average Delay (Minutes)')
    # Security Delay line chart
    security_fig = go.Figure()
    security_fig.add_trace(go.Scatter(x=avg_security['Month'],y=avg_security['SecurityDelay'],mode='lines+markers',
                                      name='Security Delay'))
    security_fig = px.line(avg_security,x='Month',y='SecurityDelay',color='Reporting_Airline',markers=True,
                           title='Average Security Delay by Month')
    security_fig.update_layout(xaxis_title='Month',yaxis_title='Average Delay (Minutes)')
    # Late Aircraft Delay line chart
    late_fig = go.Figure()
    late_fig.add_trace(go.Scatter(x=avg_late['Month'],y=avg_late['LateAircraftDelay'],mode='lines+markers',name='Late Aircraft Delay'))
    late_fig = px.line(avg_late,x='Month',y='LateAircraftDelay',color='Reporting_Airline',markers=True,
                       title='Average Late Aircraft Delay by Month')
    late_fig.update_layout(xaxis_title='Month',yaxis_title='Average Delay (Minutes)')

    return carrier_fig, weather_fig, nas_fig, security_fig, late_fig

# TASK 4 - Run the Dash application
if __name__ == '__main__':
    app.run(debug=True, port=8054)
    