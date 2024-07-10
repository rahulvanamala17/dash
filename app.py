import plotly.express as px
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
from skimage import data

# Load the solar dataset
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

# Load a sample image (Chelsea from skimage)
img = data.chelsea()

# Get unique states for dropdown options
states = df['State'].unique()

# Initialize Dash app
app = Dash(__name__)

# Define the layout of the Dash app
app.layout = html.Div([
    html.H1("Solar Dataset and Image Annotation Tool"),

    # Dropdown for selecting state
    html.Div([
        html.H2("Select State"),
        dcc.Dropdown(
            id='state-dropdown',
            options=[{'label': state, 'value': state} for state in states],
            value=states[0],  # Default value
        ),
    ]),

    # Dash DataTable for displaying filtered solar dataset
    html.Div([
        html.H2("Solar Dataset"),
        dash_table.DataTable(
            id='datatable',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
        ),
    ]),

    # Dash Graph component for displaying image and annotation tool
    html.Div([
        html.H2("Image Annotation Tool"),
        dcc.Graph(
            id='image-annotation',
            figure=px.imshow(img).update_layout(dragmode="drawrect"),
            config={
                "modeBarButtonsToAdd": [
                    "drawline",
                    "drawopenpath",
                    "drawclosedpath",
                    "drawcircle",
                    "drawrect",
                    "eraseshape",
                ]
            },
        ),
    ]),
])

# Define callback to update DataTable based on state selection
@app.callback(
    Output('datatable', 'data'),
    [Input('state-dropdown', 'value')]
)
def update_datatable(selected_state):
    filtered_df = df[df['State'] == selected_state]
    return filtered_df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
