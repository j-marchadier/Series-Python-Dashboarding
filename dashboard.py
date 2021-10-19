from re import I
import plotly_express as px
import dash
import pandas as pd
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


def backend(data_without_country_genre,data_country,data_genre):

    fig = [0, 1,2]
    # Back end
    fig[0] = px.scatter(data_country, x="series_or_movies", y="hidden_gem_score",
                        color="hidden_gem_score",
                        # size="pop",
                        hover_name="genre")  # (4)
    
    fig[1] = map(data_country)

    fig[2] = line(data_without_country_genre)

    return fig


def frontend(app, fig):
    # Front end
    app.layout = html.Div([

        html.H1(
            id='title1',
            # children=f'Life expectancy vs GDP per capita ({year})',
            children= 'Series In Time',
            style={'textAlign': 'center'}
        ),  # (5)


        dcc.Dropdown(
            id='series_or_movies_dropdown',
            options=[
                {'label': 'Series and Movies', 'value': 'Series and Movies'},
                {'label': 'Series', 'value': 'Series'},
                {'label': 'Movies', 'value': 'Movies'}
            ],
            value='Series and Movies'
        ),

        dcc.Graph(
            id="map",
            figure = fig[1]
        ),

        dcc.Graph(
            id="line",
            figure = fig[2]
        )





        #html.Div([
        #    dcc.Graph(
        #        id='graph2',
        #        figure=fig[0]
        #    )],
        #    style={'background-color': 'transparent', 'padding': '10px 5px', 'width': '49%'})

        # html.Button('On/Off', id='button',n_clicks=0),

        # dcc.Dropdown(
        #    id="year-dropdown",
        #    options = [{'label':str(year),'value': year} for year in gapminder["year"].unique()],
        #    value=2007,
        # ),

        # dcc.Slider(
        #    id="year-slider",
        #    min = 1952,
        #    max =2007,
        #    step =5,
        #    #marks ={year: '{}'.format(year) for year in gapminder["year"].unique()},
        #    value=2007,
        # ),

        # dcc.Interval(   id='interval',
        #    interval=1*300, # in milliseconds
        #    n_intervals=0,
        #    disabled = True,
        # ),

        # html.Div(children=f'''
        #    The graph above shows relationship between life expectancy and
        #    GDP per capita for year {year}. Each continent data has its own
        #    colour and symbol size is proportionnal to country population.
        #    Mouse over for details.
        # '''), # (7)

    ])

    return app


def callbacks(app,data_without_country_genre,data_country,data_genre):

    @app.callback(
        Output(component_id='title1', component_property='children'),
        Output(component_id='map',component_property='figure'),
        Output(component_id="line",component_property="figure"),
        [Input(component_id='series_or_movies_dropdown',component_property='value')]
    )
    def update_series_or_movies_values(input_value):
        new_title = "Dashboard of "+str(input_value)+" in time"

        if input_value == "Series and Movies" :
            input_value = 'Series","Movies'
        
        df_map = data_country.query('series_or_movies in ["'+str(input_value)+'"]')

        df_line = data_without_country_genre.query('series_or_movies in ["'+str(input_value)+'"]')



        return new_title,map(df_map),line(df_line)

    '''@app.callback(
        Output(component_id='graph1', component_property='figure'),
        Output(component_id='title1', component_property='children'),  # (1)
        [Input(component_id="year-slider", component_property="value")]
        # [Input(component_id='year-dropdown', component_property='value')] # (2)
    )
    def update_figure(input_value):  # (3)
        fig = px.scatter(data[input_value], x="gdpPercap", y="lifeExp",
                         color="continent",
                         size="pop",
                         hover_name="country")  # (4)

        # fig.update_layout(title ='Life expectancy vs GDP per capita ('+str(input_value)+')')
        title = 'Life expectancy vs GDP per capita (' + str(input_value) + ')'
        return fig, title

    @app.callback(Output('year-slider', 'value'),
                  Output('interval', 'disabled'),
                  [Input('interval', 'n_intervals'), Input('button', 'n_clicks')])
    def on_tick(n_intervals, n_clicks):
        OK = True
        if n_intervals is None: return 0
        if n_clicks % 2 == 0:
            OK = True
        else:
            OK = False
        return years[(n_intervals + 1) % len(years)], OK'''


def map(data):
    data = data[["country","hidden_gem_score","imdb_vote"]].dropna()
    data = data.groupby(["country"],as_index =False).mean()
    map = px.scatter_geo(data,
                        locations="country", 
                        color="hidden_gem_score",
                        hover_name="country", 
                        size="imdb_vote",
                        locationmode = "country names",
                        projection="natural earth")
    
    return map

def line(data):
    data = data[["release_year","box_office"]].dropna()
    data["release_year"] = data["release_year"].dropna().astype('int')
    data = data.groupby(["release_year"],as_index =False).sum()
    
    print(data.head())
    data = data.sort_values(by =["release_year"])
    

    
    line = px.line(data,
            x = "release_year",
            y = "box_office",
            title='Life expectancy in Canada')
    return line


def main(data):
    data_without_country_genre = data[0]
    data_country = data[1]
    data_genre = data[2]

    app = dash.Dash(__name__,suppress_callback_exceptions=True)
    fig = backend(data_without_country_genre ,data_country,data_genre)
    app = frontend(app, fig)

    callbacks(app,data_without_country_genre ,data_country,data_genre)

    # RUN APP
    app.run_server(port=2734, debug=True)  # (8)

