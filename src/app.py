from pathlib import Path

import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# for card creation in time series plot
from dash import html, dcc

import numpy as np

# loading raw object
import mne
from pylossless.dash.mne_visualizer import MNEVisualizer
from pylossless.dash.css_defaults import CSS, STYLE

####################
#  Begin Dash App
####################

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
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
et_viz.channel_slider_div.style.update(dict(display='none'))
et_viz.channel_slider_div.className = ''


df = raw_et.dataframes['blinks']
style_header = {'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white'},
style_data = {'backgroundColor': 'rgb(50, 50, 50)',
              'color': 'white'}
style_table = {'height': '300px', 
               'overflowX': 'auto',
               'overflowY': 'auto'}


TABLE_INFO = "When loading an eyetracking recording in MNE-Python,"\
             " data tables are accessible so that you can view samples and"\
             " event information in spreadsheet form. Use the drop-down to"\
             " the left to select different data tables for this recording."

table_info_col = dbc.Col(width=4, className='ms-5', align='center', children=[
                    dbc.Alert(color='success',
                              children=[html.H4('Data Tables of Events and Samples'),
                                        html.P(TABLE_INFO,
                                className="card-text fst-italic")
                                ])
                        ])
df_names = ['Blinks', 'Saccades', 'Fixations', 'Messages', 'Samples']
dfs = [{'label': this_df, 'value': this_df.lower()}
        for this_df
        in df_names]
dropdown = dcc.Dropdown(id='df-dropdown',
                        options=dfs,
                        value='blinks',
                        placeholder="Select a DataFrame",
                        className=CSS['dropdown'],)
table = dash_table.DataTable(df.to_dict('records'),
                             style_data=style_data,
                             style_table=style_table,
                             id='dataframe')

timeseries_div = html.Div([et_viz.container_plot],
                           id='channel-and-icsources-div',
                           className=CSS['timeseries-col'] + ' mb-3')

TEXT = "To the left is a timeseries graph of eyetracking data,"\
       " from a text-reading task. There are channels for"\
       " the x-position, y-position, and pupil-size of the right eye."\
       " you can see the x-position increase as the participant reads each"\
       " line of text, then decrease when they begin a new line."\
       " For simplicity, only blink events are added to this graph as"\
       " 'Annotations', which appar as red vertical boxes."\
       " Fixations and Saccades can also be included by the user if desired."
    

ts_info_col = dbc.Col(width=4, align='center', className='mb-5 pe-5', children=[
                    dbc.Alert(color='primary',
                              children=[html.H4('Eyetracking Timeseries Graph'),
                                        html.P(TEXT,
                                className="card-text fst-italic")
                                ])
                    ])
visualizers_row = dbc.Row([dbc.Col([timeseries_div], width=8),
                           ts_info_col],
                           style=STYLE['plots-row'],
                           className=CSS['plots-row'])

app.layout = dbc.Container([
                dbc.NavbarSimple(
                            html.A([html.Img(src=app.get_asset_url('mne_logo.png'),
                                    className=CSS['logo'],
                                    height='50px')], href='https://mne.tools/stable/index.html'),
                    color="primary",
                    dark=True,
                    fluid=True,
                    class_name='mb-3'),
                visualizers_row,
                dbc.Row([
                    dbc.Col([dropdown], width={'size': 6},
                            className='ms-5')
                    ]),
                dbc.Row([
                    dbc.Col([table], width={'size':7},
                            className='ms-5 mb-3'),
                    table_info_col
                    ])
], fluid=True)
@app.callback(Output('dataframe', 'data'),
              Input('df-dropdown', 'value'),
              prevent_initial_call=True)
def select_dataframe(df_dropdown_value):
    return raw_et.dataframes[df_dropdown_value].head(101).to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=False)
