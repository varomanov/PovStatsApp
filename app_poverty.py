import dash
from dash import html, dcc, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd

poverty_df = pd.read_csv('data/PovStatsData.csv')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('Poverty And Equity Database', className='display-1'),
            html.H2('The World Bank')
        ])
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='country', options=[{'label': country, 'value': country} for country in poverty_df['Country Name'].unique()]),
            html.Br(),
            html.Div(id='report')
        ])
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Tabs([
                dbc.Tab([
                    html.Ul([
                        html.Br(),
                        html.Li('Number of Economies: 170'),
                        html.Li('Temporal Coverage: 1974 - 2019'),
                        html.Li('Update Frequency: Quarterly'),
                        html.Li('Last Updated: March 18, 2020'),
                        html.Li(['Source: ', html.A('https://datacatalog.worldbank.org/dataset/poverty-and-equity-database', href='https://datacatalog.worldbank.org/dataset/poverty-and-equity-database')])
                    ])
                ], label='Key Facts'),
                dbc.Tab([
                    html.Ul([
                        html.Br(),
                        html.Li('Book title: Interactive Dashboards and Data Apps with Plotly and Dash'),
                        html.Li(['GitHub repo: ', html.A('https://github.com/PacktPublishing/Interactive-Dashboards-and-Data-Apps-with-Plotly-and-Dash', href='https://github.com/PacktPublishing/Interactive-Dashboards-and-Data-Apps-with-Plotly-and-Dash')])
                    ])
                ], label='Project Info')
            ])
        ])
    ])
])

@app.callback(Output('report', 'children'), Input('country', 'value'))
def update_country(country):
    if country is None:
        population = poverty_df[poverty_df['Country Name'].eq("World")]['2010'].sum()
        return html.H3(f'The population of World in 2010 was {population:,.0f}')
    population = poverty_df[poverty_df['Country Name'].eq(country)]['2010'].sum()
    return html.H3(f'The population of {country} in 2010 was {population:,.0f}')

if __name__ == '__main__':
    app.run(debug=True, port=8501)
    # app.run(debug=True, port=8501, host='192.168.0.172')