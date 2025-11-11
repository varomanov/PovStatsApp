from dash import Dash, callback, html, dcc, Output, Input, no_update
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


# Данные из файлов
poverty_df = pd.read_csv('data/PovStatsData.csv')
poverty_data = pd.read_csv('data/PovStatsData.csv')
regions = ['East Asia & Pacific', 'Europe & Central Asia', 'Fragile and conflict affected situations', 'High income', 
    'IDA countries classified as fragile situations', 'IDA total', 'Latin America & Caribbean', 
    'Low & middle income', 'Low income', 'Lower middle income', 'Middle East & North Africa', 'Middle income', 
    'South Asia', 'Sub-Saharan Africa', 'Upper middle income', 'World'
]
population_df = poverty_data[~poverty_data['Country Name'].isin(regions) & poverty_data['Indicator Name'].eq('Population, total')]
poverty = pd.read_csv('data/poverty.csv', low_memory=False)
gini = 'GINI index (World Bank estimate)'
gini_df = poverty[poverty[gini].notna()]


# приложение
app = Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('Poverty And Equity Database'),
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
    dbc.Row(
        dbc.Col([
            dcc.Dropdown(
                id='year_dropdown',
                options=[{'label': year, 'value': str(year)} for year in range(1974, 2019)],
                value='2010',
            ),
            html.Div(
                dcc.Graph(id='population_chart')
            )
        ])
    ),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='gini_year_dropdown',
                options=[{'label': x, 'value': x} for x in gini_df['year'].sort_values().unique()]
            ),
            html.Div(dcc.Graph(id='gini_year_barchart'))
        ]),
        dbc.Col([
            dcc.Dropdown(
                id='gini_country_dropdown',
                options=[{'label': x, 'value': x} for x in gini_df['Country Name'].sort_values().unique()],
            ),
            html.Div(dcc.Graph(id='gini_country_barchart'))
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

@callback(Output('report', 'children'), Input('country', 'value'))
def update_country(country):
    if country is None:
        population = poverty_df[poverty_df['Country Name'].eq("World")]['2010'].sum()
        return html.H3(f'The population of World in 2010 was {population:,.0f}')
    population = poverty_df[poverty_df['Country Name'].eq(country)]['2010'].sum()
    return html.H3(f'The population of {country} in 2010 was {population:,.0f}')


@callback(
    Output('population_chart', 'figure'),
    Input('year_dropdown', 'value')
)
def plot_countries_by_population(year):
    year_df = population_df[['Country Name', year]].sort_values(by=year, ascending=False).head(20)

    fig = go.Figure()
    fig.add_bar(
        x=year_df['Country Name'],
        y=year_df[year],
    )
    fig.update_layout(
        title=f'Top twelwe countrues by population = {year}',
        template='none',
    )
    return fig

@callback(
    Output('gini_year_barchart', 'figure'),
    Output('gini_country_barchart', 'figure'),
    Input('gini_year_dropdown', 'value'),
    Input('gini_country_dropdown', 'value'),
)
def update_plot(year, country):
    if not year and not country:
        raise PreventUpdate
    
    if year:
        df_year = gini_df[gini_df['year'].eq(year)].dropna(subset=gini).sort_values(by=gini)
        fig_year = px.bar(df_year, x=gini, y='Country Name', title=gini + ' ' + str(year))
    else:
        fig_year = no_update
    
    if country:
        df_country = gini_df[gini_df['Country Name'].eq(country)].dropna(subset=gini).sort_values(by='year')
        fig_country = px.bar(df_country, y=gini, x='year', title=' - '.join([gini, country]))
    else:
        fig_country = no_update
    
    return fig_year, fig_country

if __name__ == '__main__':
    app.run(debug=True, port=8501)
    # app.run(debug=True, port=8501, host='192.168.0.172')