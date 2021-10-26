import plotly_express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# https://www.w3schools.com/css/css_font_fallbacks.asp
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


def backend(data_without_country_genre, data_country, data_genre):
    fig = [0, 1, 2, 3, 4]
    # Back end
    fig[0] = px.scatter(data_country, x="series_or_movies", y="hidden_gem_score",
                        color="hidden_gem_score",
                        # size="pop",
                        hover_name="genre")  # (4)

    fig[1] = map_score(data_country)

    fig[2] = line(data_without_country_genre)

    fig[3] = bar(data_genre)

    fig[4] = hist(data_without_country_genre)

    return fig


def frontend(app, fig):
    # Front end
    app.layout = html.Div([
        # 1 row
        html.Div(children=[

            html.H1(
                id='title1',
                children='Series In Time',
                style={'textAlign': 'center', 'text-decoration': 'underline', 'letter-spacing': '5px',
                       'font-family': 'Tahoma, sans-serif',
                       'font-size': '3vw'}
            ),

        ], style={'height': '30px', 'position': 'sticky'}, className='row'),

        # Second Row
        html.Div(children=[
            # 1 column of 2 row
            html.Div(children=[

                dcc.Dropdown(
                    id='series_or_movies_dropdown',
                    options=[
                        {'label': 'Series and Movies', 'value': 'Series and Movies'},
                        {'label': 'Series', 'value': 'Series'},
                        {'label': 'Movies', 'value': 'Movies'}
                    ],
                    value='Series and Movies'
                ),

            ], style={'display': 'inline-block', 'width': '15%'}),

            # 2 col of 2 row
            html.Div(children=[
                dcc.Graph(
                    id="line",
                    figure=fig[2],
                    # config={'displayModeBar': False, 'editable':True}
                ),
            ], style={'display': 'inline-block', 'width': '42%', 'height': '60%'}),

            # 3 col of 2 row
            html.Div(children=[

                dcc.Graph(
                    id="map",
                    figure=fig[1]
                )
            ], style={'display': 'inline-block', 'width': '42%', 'height': '60%'}),

        ], style={'height': '350px', 'padding': '20px 5px'}, className='row'),

        # 3 row
        html.Div(children=[

            # 3rows 1 col
            html.Div(children=[
                dcc.Graph(
                    id="bar",
                    figure=fig[3]
                )
            ], style={'display': 'inline-block', 'width': '42%', 'height': '60%'}),

            # 3rows 1 col
            html.Div(children=[
                dcc.Graph(
                    id="hist",
                    figure=fig[4]
                )
            ], style={'display': 'inline-block', 'width': '42%', 'height': '60%'}),
        ], style={'height': '250px', 'padding': '20px 5px'}, className='row'),

        # html.Div([
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

    ], style={'background-color': 'white'})

    return app


def callbacks(app, data_without_country_genre, data_country, data_genre):
    @app.callback(
        Output(component_id='title1', component_property='children'),
        Output(component_id='map', component_property='figure'),
        Output(component_id="line", component_property="figure"),
        Output(component_id="bar", component_property="figure"),
        [Input(component_id='series_or_movies_dropdown', component_property='value'),
         Input(component_id='line', component_property='relayoutData')]
    )
    def update_series_or_movies_values(input_value, selectedData):
        new_title = "Dashboard of " + str(input_value) + " in time"

        if input_value == "Series and Movies":
            input_value = 'Series","Movies'

        df, df_country, df_genre = crossfilter(data_without_country_genre, data_country, data_genre, selectedData)

        df_map = df_country.query('series_or_movies in ["' + str(input_value) + '"]')

        df_line = df.query('series_or_movies in ["' + str(input_value) + '"]')

        df_bar = df_genre.query('series_or_movies in ["' + str(input_value) + '"]')

        return new_title, map_score(df_map), line(df_line), bar(df_bar)

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


def map_score(data):
    data = data[["country", "hidden_gem_score", "imdb_vote"]].dropna()
    data = data.groupby(["country"], as_index=False).mean()
    map = px.scatter_geo(data,
                         locations="country",
                         color="hidden_gem_score",
                         hover_name="country",
                         size="imdb_vote",
                         locationmode="country names",
                         projection="natural earth", )

    map.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})

    return map


def line(data):
    data = data[["release_year", "box_office"]].dropna()
    data["release_year"] = data["release_year"].dropna().astype('int')
    data = data.groupby(["release_year"], as_index=False).sum()

    data = data.sort_values(by=["release_year"])

    line = px.line(data,
                   x="release_year",
                   y="box_office",
                   title='Life expectancy in Canada')

    line.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})

    return line


def bar(data):
    data = data[["awards_received", "run_time", "title", "genre"]].dropna()
    data = data.reset_index(drop=True)
    data["count"] = 0
    data["count"] = data[["run_time","genre","count"]].groupby(by=["run_time","genre"]).count().reset_index(drop=True)

    bar = px.sunburst(data, names= "genre", parents= "run_time", values='count')

   # starbucks_dist = starbucks_locations.groupby(by=["Country", "State/Province", "City"]).count()[["Store Number"]].rename(columns={"Store Number":"Count"})

   # bar = px.bar(data,
     #            x="run_time",
    #             y="awards_received",
     #            color="genre",
     #            title="Number of awards recieve by runing time",
     #            hover_name="title")

    #bar.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': ['< 30 minutes', '30-60 mins', '1-2 hour', '> 2 hrs']})

    bar.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})

    return bar


def hist(data):
    data = data[["title", "imdb_vote", "series_or_movies"]].dropna()

    hist = px.histogram(data, "imdb_vote", nbins=30, range_x=[0, 1000000], color="series_or_movies")

    return hist


def crossfilter(data_without_country_genre, data_country, data_genre, selectedData):
    if selectedData is not None and selectedData != {'autosize': True}:
        if selectedData == {'xaxis.autorange': True,
                            'yaxis.autorange': True}: return data_without_country_genre, data_country, data_genre
        min_year = str(int(selectedData['xaxis.range[0]']))
        max_year = str(int(selectedData['xaxis.range[1]']))

        df_country = data_country.query("release_year > " + min_year + " and release_year < " + max_year)
        df_genre = data_genre.query("release_year >" + min_year + " and release_year <" + max_year)
        df = data_without_country_genre.query("release_year >" + min_year + " and release_year <" + max_year)
        print(min_year, max_year)

        return df, df_country, df_genre
    return data_without_country_genre, data_country, data_genre


def main(data):
    data_without_country_genre = data[0]
    data_country = data[1]
    data_genre = data[2]

    app = dash.Dash(__name__, suppress_callback_exceptions=True)
    fig = backend(data_without_country_genre, data_country, data_genre)

    app = frontend(app, fig)

    callbacks(app, data_without_country_genre, data_country, data_genre)

    # RUN APP
    app.run_server(port=2734, debug=True)  # (8)
