import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
pd.set_option('display.max_columns', None)
# Graphs
histogram = px.histogram(test, x='Probability', color=TARGET, marginal="box", nbins=30, opacity=0.6,
                         color_discrete_sequence=['#FFBD59', '#3BA27A'])
histogram.update_layout(title_text=f'Distribution of probabilities by class (n={len(test)})',
                        font_family='Tahoma', plot_bgcolor='rgba(255,242,204,100)')
histogram.update_yaxes(title_text="Count")

barplot = px.bar(test.groupby('Binned probability', as_index=False)['Target'].mean(),
                 x='Binned probability', y='Target', color_discrete_sequence=['#3BA27A'])
barplot.update_layout(title_text=f'Survival rate by binned probabilities (n={len(test)})',
                      font_family='Tahoma', xaxis={'categoryarray': labels},
                      plot_bgcolor='rgba(255,242,204,100)')
barplot.update_yaxes(title_text="Percentage survived")

columns = ['Age', 'Gender', 'Class', 'Embark town', TARGET, 'Probability']
table = go.Figure(data=[go.Table(
    header=dict(values=columns, fill_color='#FFBD59', line_color='white', align='center',
                font=dict(color='white', size=13)),
    cells=dict(values=[test[c] for c in columns], format=["d", "", "", "", "", ".2%"],
               fill_color=[['white', '#FFF2CC']*(len(test)-1)], align='center'))
])
table.update_layout(
    title_text=f'Sample records (n={len(test)})', font_family='Tahoma')

# ********************* Dash app *********************
app = dash.Dash(__name__)
app.layout = html.Div([
    html.Div([
        html.H1("Titanic predictions"),
        html.P("Summary of predicted probabilities for Titanic test dataset."),
        html.Img(src="assets/left_pane.png"),
        html.Label("Passenger class", className='dropdown-labels'),
        dcc.Dropdown(id='class-dropdown', className='dropdown', multi=True,
                     options=create_dropdown_options(test['Class']),
                     value=create_dropdown_value(test['Class'])),
        html.Label("Gender", className='dropdown-labels'),
        dcc.Dropdown(id='gender-dropdown', className='dropdown', multi=True,
                     options=create_dropdown_options(test['Gender']),
                     value=create_dropdown_value(test['Gender'])),
        html.Button(id='update-button', children="Update")
    ], id='left-container'),
    html.Div([
        html.Div([
            dcc.Graph(id="histogram", figure=histogram),
            dcc.Graph(id="barplot", figure=barplot)
        ], id='visualisation'),
        html.Div([
            dcc.Graph(id='table', figure=table),
            html.Div([
                html.Label("Survival status", className='other-labels'),
                daq.BooleanSwitch(id='target_toggle',
                                  className='toggle', on=True, color="#FFBD59"),
                html.Label("Sort probability in ascending order",
                           className='other-labels'),
                daq.BooleanSwitch(
                    id='sort_toggle', className='toggle', on=True, color="#FFBD59"),
                html.Label("Number of records", className='other-labels'),
                dcc.Slider(id='n-slider', min=5, max=20, step=1, value=10,
                           marks=create_slider_marks([5, 10, 15, 20])),
            ], id='table-side'),
        ], id='data-extract')
    ], id='right-container')
], id='container')

if __name__ == '__main__':
    app.run_server(debug=True)
