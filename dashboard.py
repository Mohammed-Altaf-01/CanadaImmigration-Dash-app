# importing all the modules
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
pd.set_option('display.max_columns', None)


# wrangling our dataframe to check for proper values to be plotted
df = pd.read_excel('canada.xlsx',
                   sheet_name='Canada by Citizenship',
                   skiprows=range(20),
                   skipfooter=2)

# making years list usefull for plotting
years = [str(y) for y in range(1980, 2014)]
df.drop(columns=['AREA', 'REG', 'DEV', 'DevName'],
        axis=1, inplace=True)  # droping waste columns
df.rename(columns={'OdName': 'Country',
          'AreaName': 'Continent', 'RegName': 'Region'}, inplace=True)  # renaming column names appropriately
df['Total'] = df.sum(axis=1, numeric_only=True)
df.drop(columns=['Type', 'Coverage'], axis=1, inplace=True)
df.set_index('Country', inplace=True)  # changing the index of our dataframe
df.columns = list(map(str, df.columns))
unique_continents = df['Continent'].unique()


# making our dashboard
app = Dash(__name__)


app.layout = html.Div([
    html.H2('Graphs of various Immigrations to canada Is Shown Below ', style={
            'width': '96%', 'padding-left': '3%', 'padding-right': '1%', 'margin': 25, 'textAlign': 'Center'}),
    dcc.Dropdown(options=df['Continent'].unique(),
                 value=df['Continent'].unique()[0], id='data-dropdown'),
    html.H3('List of Countries for that Continent: '),
    # drawing graph of top5 countries in that continent.
    dcc.Graph(id='basic-figures1'),

    html.H3(children=["Graph of Migration of Least five Countires:",
                      dcc.Graph(id='basic-figures2')]
            )  # least 5 countires graph
])


# writing our callback for first Graph
@ app.callback(
    Output(component_id='basic-figures1', component_property='figure'),
    Input(component_id='data-dropdown', component_property='value')
)
def update_graph1(value):
    if value == 'Northern America':
        north_america = df.loc[['Canada', 'United States of America'], years]
        fig_america = px.histogram(
            north_america, x=years, y=north_america.index)
        return fig_america

        # getting data of that particular column
    data = df.loc[df['Continent'] == str(value)]
    # sorting increasing order
    data = data.sort_values(by='Total', ascending=False)
    # grabing top 5 values from the dataframe
    top5 = df.loc[list(data.head(5).index), years]
    top5 = top5.transpose()  # interchanging the values
    fig = px.line(top5)
    return fig


# creating least 5 graphs callback system
@app.callback(
    Output(component_id='basic-figures2', component_property='figure'),
    Input(component_id='data-dropdown', component_property='value')
)
def update_graph(value):
    if value == 'Northern America':
        north_america = df.loc[['Canada', 'United States of America'], years]
        fig_america = px.bar(north_america, x=years, y=north_america.index)
        return fig_america

    # getting data of that particular column
    data = df.loc[df['Continent'] == str(value)]
    # sorting increasing order
    data = data.sort_values(by='Total', ascending=False)
    # grabing top 5 values from the dataframe
    least5 = df.loc[list(data.tail(5).index), years]
    least5 = least5.transpose()  # interchanging the values
    fig = px.line(least5)
    return fig


# running our server
if __name__ == '__main__':
    app.run_server()
