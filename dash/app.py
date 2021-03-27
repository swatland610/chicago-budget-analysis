import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

# import data wranglers
from data.wranglers.viz_data import Data_Viz_Data

# initiate dash app
app = dash.Dash(__name__)

# set data objects
annual_budgets_totals = Data_Viz_Data().get_annual_budget_totals()

# pull in budget data
annual_totals_fig = px.area(annual_budgets_totals, x='budget_year', y='amount')

app.layout = html.Div(children = [
    html.H1(children='''
    Chicago Budgets: 10 Year Look
'''), 
    
    html.H2(children='''
    Annual Budget Totals
    '''
    ), 
    
    dcc.Graph(
        figure = annual_totals_fig
    )])

if __name__ == '__main__':    
    app.run_server(debug=True)

