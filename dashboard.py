import plotly_express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd

def backend(data):
    fig = [0, 1, 2, 3]

    fig[0] = map_score(data[1])

    fig[1] = line(data[0])

    fig[2] = pie(data[2])

    fig[3] = hist(data[0],'Movies and Series')

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
                ]),
                html.Div(children=[
                    dcc.Dropdown(
                        id='Best_score',
                        options=[
                            {'label': 'All score', 'value': 0},
                            {'label': 'Best 30 Score', 'value': 30},
                            {'label': 'Best 100 Score', 'value': 100},
                            {'label': 'Worse 100 Score', 'value': -100}
                        ],
                        value=0
                    ),
                ], style={'padding': '10px 0px'}),

                html.H1(
                    id='title_watch_time',
                    children='Watch time',
                    style={'textAlign': 'center','font-family': 'Tahoma, sans-serif','font-size': '20px'}
                ),

                html.Div(children=[
                    dcc.Checklist(
                        id='watch_time_all',
                        options=[
                            {'label': 'All', 'value': 'All'},
                        ],
                        value=['All']
                    ),
                    dcc.Checklist(
                        id='watch_time',
                        options=[
                            {'label': '< 30 minutes', 'value': '< 30 minutes'},
                            {'label': '30-60 mins', 'value': '30-60 mins'},
                            {'label': '1-2 hour', 'value': '1-2 hour'},
                            {'label': '> 2 hrs', 'value': '> 2 hrs'},
                        ],
                        value=['< 30 minutes','30-60 mins','1-2 hour','> 2 hrs']
                    )
                ], style={'padding': '10px 0px'})

            ], style={'display': 'inline-block', 'width': '15%'}),

            # 2 col of 2 row
            html.Div(children=[
                dcc.Graph(
                    id="line",
                    figure=fig[1],
                    # config={'displayModeBar': False, 'editable':True}
                ),
            ], style={'display': 'inline-block', 'width': '42%', 'height': '60%'}),

            # 3 col of 2 row
            html.Div(children=[

                dcc.Graph(
                    id="map",
                    figure=fig[0]
                )
            ], style={'display': 'inline-block', 'width': '42%', 'height': '60%'}),

        ], style={'height': '350px', 'padding': '20px 5px'}, className='row'),

        # 3 row
        html.Div(children=[

            # 3rows 1 col
            html.Div(children=[
                dcc.Graph(
                    id="pie",
                    figure=fig[2]
                )
            ], style={'display': 'inline-block', 'width': '39%', 'height': '60%'}),

            # 3rows 1 col
            html.Div(children=[
                dcc.Graph(
                    id="hist",
                    figure=fig[3]
                )
            ], style={'display': 'inline-block', 'width': '60%', 'height': '60%'}),
        ], style={'height': '250px', 'padding': '20px 5px'}, className='row'),

    ], style={'background-color': 'white'})

    return app


def callbacks(app, data):
    @app.callback(
        Output(component_id='title1', component_property='children'),
        Output(component_id='map', component_property='figure'),
        Output(component_id="line", component_property="figure"),
        Output(component_id="hist", component_property="figure"),
        Output(component_id="pie", component_property="figure"),
        Output(component_id='watch_time_all',component_property='value'),
        Output(component_id='watch_time',component_property='value'),
        [Input(component_id='series_or_movies_dropdown', component_property='value'),
         Input(component_id='Best_score', component_property='value'),
         Input(component_id='line', component_property='relayoutData'),
         Input(component_id='watch_time_all',component_property='value'),
         Input(component_id='watch_time',component_property='value')]
    )
    def update_series_or_movies_values(movieorserie, best_score, selectedData,watch_time_all,watch_time):
        new_title = "Dashboard of " + str(movieorserie) + " through time"
        df = data
        # df[0] == with ou country and genre
        # df[1] == country
        # df[2] == genre

        df = movies_or_series_f(movieorserie, df)

        df = best_score_f(best_score, df)

        df,watch_time_all,watch_time = watch_time_f(watch_time_all,watch_time,df)

        df = crossfilter(selectedData, df)

        return new_title, map_score(df[1]), line(df[0]), hist(df[0],str(movieorserie)), pie(df[2]),watch_time_all,watch_time


def map_score(data):
    data = data[["country", "hidden_gem_score", "imdb_vote"]].dropna()
    data = data.groupby(["country"], as_index=False).mean()
    map = px.scatter_geo(data,
                         locations="country",
                         color="hidden_gem_score",
                         hover_name="country",
                         size="imdb_vote",
                         locationmode="country names",
                         projection="natural earth",
                         title='Map of Hidden gem score in the word')

    map.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})

    return map


def line(data):
    data = data[["release_year", "box_office"]].dropna()
    #print(data[data["release_year"]== 1940])
    data["release_year"] = data["release_year"].dropna().astype('int')
    data = data.groupby(["release_year"], as_index=False).sum()

    data = data.sort_values(by=["release_year"])



    line = px.area(data,
                   x="release_year",
                   y="box_office",
                   title='Box office through time')

    line.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})


    return line


def pie(data):
    data = data["genre"].dropna()
    data = pd.DataFrame(data.reset_index(drop=True))
    data["count"] = 0
    data = pd.DataFrame(data.groupby(["genre"]).count())
    data["genre"] = data.index
    data = pd.DataFrame(data.reset_index(drop=True))

    pie = px.pie(data, names="genre", values='count',title='Domination of genres', hole = 0.5)

    pie.update_traces(textposition='inside')

    pie.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})

    return pie


def hist(data,movieorserie):
    data = data[["title", "imdb_vote", "series_or_movies"]].dropna()

    hist = px.histogram(data, "imdb_vote", nbins=30, range_x=[0, 1000000],title=f'Count of IMBD votes according to {movieorserie} ', color="series_or_movies")

    return hist


def crossfilter(selectedData, df):
    if selectedData is not None and selectedData != {'autosize': True}:
        if selectedData == {'xaxis.autorange': True,
                            'yaxis.autorange': True}: return df
        min_year = str(int(selectedData['xaxis.range[0]']))
        max_year = str(int(selectedData['xaxis.range[1]']))

        df[1].query("release_year > " + min_year + " and release_year < " + max_year, inplace=True)
        df[2].query("release_year >" + min_year + " and release_year <" + max_year, inplace=True)
        df[0].query("release_year >" + min_year + " and release_year <" + max_year, inplace=True)
        print(min_year, max_year)

        return df
    return df


def movies_or_series_f(movieorserie, df):
    df_bis = [0, 1, 2]
    for i in range(3):
        if movieorserie == "Series and Movies":
            df_bis[i] = df[i].query('series_or_movies == "Series" or series_or_movies == "Movies"').reset_index()
        else:
            df_bis[i] = df[i].query(f'series_or_movies ==  "{str(movieorserie)}" ').reset_index()

    df = df_bis
    return df


def best_score_f(best_score, df):
    y = 0
    if best_score == 0 : return df

    if best_score > 0:
        df[0] = df[0].sort_values(['imdb_score'], ascending=False).head(best_score).reset_index()
        df[1] = df[1].sort_values(['imdb_score'], ascending=False).head(best_score).reset_index()
        df[2] = df[2].sort_values(['imdb_score'], ascending=False).head(best_score).reset_index()
    else:
        df[0] = df[0].sort_values(['imdb_score'], ascending=True).head(-best_score).reset_index()
        df[1] = df[1].sort_values(['imdb_score'], ascending=True).head(-best_score).reset_index()
        df[2] = df[2].sort_values(['imdb_score'], ascending=True).head(-best_score).reset_index()

    return df

def watch_time_f(watch_time_all,watch_time,df):
    options=[
        {'label': '< 30 minutes', 'value': '< 30 minutes'},
        {'label': '30-60 mins', 'value': '30-60 mins'},
        {'label': '1-2 hour', 'value': '1-2 hour'},
        {'label': '> 2 hrs', 'value': '> 2 hrs'},
    ]
    all_wt = [option["value"] for option in options]
    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "watch_time" :
        watch_time_all =["All"] if set(watch_time) == set(all_wt) else []
    else :
        watch_time = all_wt if watch_time_all else []

    df[0] = df[0].query(f"run_time in {watch_time}")
    df[1] = df[1].query(f"run_time in {watch_time}")
    df[2] = df[2].query(f"run_time in {watch_time}")

    return df,watch_time_all,watch_time

def main(data):
    app = dash.Dash(__name__, suppress_callback_exceptions=True)
    fig = backend(data)

    app = frontend(app, fig)

    callbacks(app, data)

    # RUN APP
    app.run_server(port=2734, debug=True)  # (8)
