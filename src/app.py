from pathlib import Path

import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# for card creation in time series plot
from dash import html

import numpy as np

# loading raw object
import mne
from pylossless.dash.mne_visualizer import MNEVisualizer
from pylossless.dash.css_defaults import CSS, STYLE

####################
#  Begin Dash App
####################

app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([])

PATH = Path(__file__).parent.parent
DATA_PATH = PATH.joinpath("data").resolve()
fname = 'HREF_eyelink_sample_textpage_ws.asc'
FPATH = DATA_PATH.joinpath(fname)
raw_et = mne.io.read_raw_eyelink(FPATH,
                                 create_annotations=['blinks', 'messages'])

et_viz = MNEVisualizer(app, raw_et, show_ch_slider=False,
                       scalings={'eyegaze': 1, 'pupil': 1000},
                       show_n_channels=3)  # scalings={'eyegaze': 1000}  zoom=2

df = raw_et.dataframes['blinks']
style_header = {'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white'},
style_data = {'backgroundColor': 'rgb(50, 50, 50)',
              'color': 'white'}
table = dash_table.DataTable(df.to_dict('records'),
                             style_data=style_data)

timeseries_div = html.Div([et_viz.container_plot],
                           id='channel-and-icsources-div',
                           className=CSS['timeseries-col'])
visualizers_row = dbc.Row([dbc.Col([timeseries_div], width=8)],
                           style=STYLE['plots-row'],
                           className=CSS['plots-row'])

app.layout = dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.Img(src=app.get_asset_url('mne_logo.png'),
                                 className=CSS['logo'],
                                 height='40px')
                            ], width=12)
                    ]),
                visualizers_row,
], fluid=True)


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
