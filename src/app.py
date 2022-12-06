from pathlib import Path

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

# file selectioni
import tkinter
from tkinter import filedialog

# time series plot
from plotly import tools
import plotly.graph_objects as go
from plotly.graph_objs import Layout, YAxis, Scatter, Annotation, Annotations, Data, Figure, Marker, Font

# for card creation in time series plot
from dash import html

import numpy as np

# loading raw object
import mne
from mne_et_visualizer import MNEVisualizer

project_root = Path('./tmp_test_files')
derivatives_dir = project_root / 'derivatives'
files_list = [{'label':str(file), 'value':str(file)} for file in sorted(derivatives_dir.rglob("*.edf"))]


####################
#  Begin Dash App
####################

from pathlib import Path



'''raw = mne.io.read_raw_egi('sub-s004-ses_07_task-PLR_20220218_021538.mff').pick('eeg')
raw.load_data().filter(1,40)

raw_et = mne.io.eyetracking.read_raw_eyelink('s04s07_PLR_18Feb22.asc')'''
#info = mne.create_info(ica._ica_names,
#                       sfreq=raw.info['sfreq'],
#                       ch_types=['eeg'] * ica.n_components_)

#raw_ica = mne.io.RawArray(ica.get_sources(raw).get_data(), info)

app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([])

print('####', Path(__file__).parent.parent)
PATH = Path(__file__).parent.parent
DATA_PATH = PATH.joinpath("data").resolve()
FPATH = DATA_PATH.joinpath('test_eyelink.asc')
raw_et = mne.io.eyetracking.read_raw_eyelink(FPATH)
                #.copy()
                #.crop(tmin=44,tmax=54)
        #)
blink_annots = mne.Annotations(**{kwarg: [annot[kwarg] for annot
                                          in raw_et.annotations 
                                          if "blink" in annot["description"]]
                                  for kwarg in ('onset','duration','description')})
raw_et.set_annotations(blink_annots)

et_visualizer = MNEVisualizer(app, raw_et, scalings={'eyetrack':1000}, zoom=2, plot_n_chans=6)
et_visualizer.update_layout(5, 0)
#eeg_visualizer = MNEVisualizer(app, raw, time_slider=et_visualizer.dash_ids['time-slider']) # 




####################
# Callbacks
####################

@app.callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    # State('input-on-submit', 'value')
)
def _select_folder(n_clicks):
    global eeg_vizualizer
    if n_clicks:
        root = tkinter.Tk()
        root.withdraw()
        directory = filedialog.askdirectory()
        print('selected directory: ', directory)
        root.destroy()
        eeg_visualizer.change_dir(directory)
        return directory


########################
# Layout
########################


app.layout = html.Div([
                        html.Div([
                                    html.Button('Folder',
                                                id='submit-val',
                                                className="folderButton",
                                                title=f'current folder: {project_root.resolve()}'
                                                ),
                                    dcc.Dropdown(id="fileDropdown",
                                                className="card",
                                                options=files_list,
                                                placeholder="Select a file"
                                                ),
                                    html.Img(src=app.get_asset_url('mne_logo.png'), style={'margin':'10px'}),
                                    html.Div(id='container-button-basic',
                                            children='Enter a value and press submit')
                                    ],
                                    className='banner'
                                 ),
                        html.Div([
                                html.Div(id='plots-container', 
                                         children=[html.Div([et_visualizer.container_plot])],
                                        )
                                    ],
                                style={'display':'block'})
                        ], style={"display":"block"})


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
