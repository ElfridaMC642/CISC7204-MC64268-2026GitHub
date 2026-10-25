import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/d51iMGfp_t0QpO30Lym-dw/automobile-sales.csv"
df = pd.read_csv(URL)
year_list = sorted(df['Year'].unique())

app = dash.Dash(__name__)
app.layout = html.Div(children=[
    # TASK 2.1: Dashboard Title
    html.H1('Automobile Sales Statistics Dashboard',style={'textAlign': 'center','color': '#503D36','fontSize': 24}),
    # TASK 2.2: Report Type Dropdown
    html.Div([html.Label('Select Report Type:'),
              dcc.Dropdown(id='dropdown-statistics',
                           options=[{'label': 'Yearly Statistics','value': 'Yearly Statistics'},
                                    {'label': 'Recession Period Statistics','value': 'Recession Period Statistics'}],
                           placeholder='Select a report type',value=None,clearable=False,
                           style={'width': '80%','padding': '3px','fontSize': 20})]),
    # TASK 2.3: Year Dropdown
    html.Div([html.Label('Select Year:'),
              dcc.Dropdown(id='select-year',
                           options=[{'label': str(year), 'value': int(year)}for year in year_list],
                           value=int(year_list[0]),clearable=False,disabled=True,
                           style={'width': '80%','padding': '3px','fontSize': 20})]),
    html.Div(id='output-container',className='chart-grid',style={'display': 'flex','flexWrap': 'wrap','justifyContent': 'center'})])

# TASK 2.4: Control the Year Dropdown
@app.callback(Output('select-year', 'disabled'),Input('dropdown-statistics', 'value'))
def update_year_dropdown(selected_statistics):
    return selected_statistics != 'Yearly Statistics'

# TASK 2.5: Display dashboard charts
@app.callback(Output('output-container', 'children'),Input('dropdown-statistics', 'value'),Input('select-year', 'value'))
def update_output_container(selected_statistics, selected_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = df[df['Recession'] == 1]
        yearly_sales = (recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index())
        line_fig = px.line(yearly_sales,x='Year',y='Automobile_Sales',title='Average Automobile Sales During Recession')
        line_fig.update_layout(xaxis_title='Year',yaxis_title='Average Automobile Sales')
        vehicle_sales = (recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index())
        bar_fig = px.bar(vehicle_sales,x='Vehicle_Type',y='Automobile_Sales',
                         title='Average Vehicles Sold by Vehicle Type During Recession',
                         labels={'Vehicle_Type': 'Vehicle Type','Automobile_Sales': 'Average Automobile Sales'})
        advertising_data = (recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index())
        pie_fig = px.pie(advertising_data,values='Advertising_Expenditure',names='Vehicle_Type',
                         title='Advertising Expenditure Share by Vehicle Type During Recession')
        unemployment_data = (recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index())
        unemployment_fig = px.bar(unemployment_data,x='unemployment_rate',y='Automobile_Sales',color='Vehicle_Type',
                                  barmode='group',title='Effect of Unemployment Rate on Vehicle Sales',
                                  labels={'unemployment_rate': 'Unemployment Rate','Automobile_Sales': 'Average Automobile Sales',
                                          'Vehicle_Type': 'Vehicle Type'})
        return html.Div([html.Div([html.Div(dcc.Graph(figure=line_fig), style={'width': '50%'}),
                                   html.Div(dcc.Graph(figure=bar_fig), style={'width': '50%'})], 
                                  style={'display': 'flex', 'width': '100%'}),
                         html.Div([html.Div(dcc.Graph(figure=pie_fig), style={'width': '50%'}),
                                   html.Div(dcc.Graph(figure=unemployment_fig), style={'width': '50%'})], 
                                  style={'display': 'flex', 'width': '100%'})], style={'width': '100%'})

    elif selected_statistics == 'Yearly Statistics':
        yearly_data = df[df['Year'] == selected_year]
        average_yearly_sales = (df.groupby('Year')['Automobile_Sales'].mean().reset_index())
        yearly_sales_fig = px.line(average_yearly_sales,x='Year',y='Automobile_Sales',title='Yearly Average Automobile Sales',
                                   labels={'Year': 'Year','Automobile_Sales': 'Average Automobile Sales'})

        monthly_sales = (yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index().sort_values('Month'))
        monthly_sales_fig = px.line(monthly_sales,x='Month',y='Automobile_Sales',
                                    title=f'Total Monthly Automobile Sales in {selected_year}',markers=True,
                                    labels={'Month': 'Month','Automobile_Sales': 'Total Automobile Sales'})
        monthly_sales_fig.update_xaxes(categoryorder='array',categoryarray=list(range(1, 13)))
        monthly_sales_fig.update_xaxes(tickmode='linear',dtick=1)

        vehicle_sales = (yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index())
        vehicle_sales_fig = px.bar(vehicle_sales,x='Vehicle_Type',y='Automobile_Sales',
                                   title=f'Average Vehicles Sold by Vehicle Type in {selected_year}',
                                   labels={'Vehicle_Type': 'Vehicle Type','Automobile_Sales': 'Average Automobile Sales'})

        advertising_data = (yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index())
        advertising_fig = px.pie(advertising_data,values='Advertising_Expenditure',names='Vehicle_Type',
                                 title=f'Advertising Expenditure by Vehicle Type in {selected_year}')

        return html.Div([html.Div([html.Div(dcc.Graph(figure=yearly_sales_fig),style={'width': '50%'}),
                                   html.Div(dcc.Graph(figure=monthly_sales_fig),style={'width': '50%'})], 
                                  style={'display': 'flex', 'width': '100%'}),
                         html.Div([html.Div(dcc.Graph(figure=vehicle_sales_fig),style={'width': '50%'}),
                                   html.Div(dcc.Graph(figure=advertising_fig),style={'width': '50%'})], 
                                  style={'display': 'flex', 'width': '100%'})], style={'width': '100%'})
    return html.Div('Please select a report type to display the dashboard.',
                    style={'textAlign': 'center','fontSize': 20,'padding': '30px'})

if __name__ == '__main__':
    app.run(debug=True, port=8057)
