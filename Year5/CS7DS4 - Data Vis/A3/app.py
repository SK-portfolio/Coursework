import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import plotly.io as pio
#------------------------[load dataset (prepared from ghcnm.py)]------------------------
df = pd.read_csv("ghcnm_europe_1924_2024.csv")

#dictionary: station -> name
station_names = df.groupby("station")["name"].first()

#convert temp vals to numeric
mcols = [f"v{i}" for i in range(1, 13)]
df[mcols] = df[mcols].apply(pd.to_numeric, errors="coerce")
df["annual_mean"] = df[mcols].mean(axis=1)

#------------------------[build MapLibre map]------------------------
#remove duplicate stations for mapping
df_unique = df.drop_duplicates("station")

#create scatter mapbox figure
fig_map = px.scatter_map(
    df_unique,
    lat="lat",
    lon="lon",
    hover_name="name",
    hover_data={"station": True, "lat": False, "lon": False},   #show station ID only when hovering
    custom_data=["station"],                                    #for clickData retrieval
    zoom=3.4,
    height=350,
    template="plotly_dark"
)
# marker customization (station+station clusters)
fig_map.update_traces(
    marker=dict(size=7, opacity=1, color="red"),
    cluster=dict(enabled=True, maxzoom=8, step=50, color='#1f77b4')
)
# map layout customization
fig_map.update_layout(
    map=dict(
        style="open-street-map",
        center={"lat": 54, "lon": 15},
        zoom=1.7
    ),
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor="#2b2b2b",
    plot_bgcolor="#2b2b2b",
    font=dict(color="white")
)

#------------------------[Dash app layout(the web dashboard)]------------------------
#initialisation
app = dash.Dash(__name__)

#dashboard layout 
app.layout = html.Div([
    #dashboard title
    html.H1("European Climate Dashboard (1924–2024)", style={"text-align": "center", "color": "white"}),
    #scatterplot map figure
    html.H3("1. Select a station by clicking on the map below.", style={"color": "white"}),
    dcc.Graph(id="map", figure=fig_map, style={'height': '350px', 'backgroundColor': '#2b2b2b'}),
    
    #time series figures
    html.Div([
        html.Div([
                #annual mean time series figure
            html.H3("2. Annual Mean Temperature (°C)", style={"color": "white"}),
            dcc.Graph(id="timeseries", style={'height': '350px', 'backgroundColor': '#2b2b2b'})
        ], style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
                #monthly time series figure
            html.H3("3. Monthly Breakdown (°C)", style={"color": "white"}),
            dcc.Graph(id="monthlyseries", style={'height': '350px', 'backgroundColor': '#2b2b2b'})
        ], style={'width': '49%', 'display': 'inline-block', 'float': 'right'})
    ])
], style={'margin': '0px', 'backgroundColor': '#2b2b2b'})

#------------------------[Callbacks]------------------------
#callback to update time series figures based on map click
@app.callback(
    Output("timeseries", "figure"),
    Input("map", "clickData")
)
#function to update annual mean time series
def update_timeseries(clickData):
    if clickData is None:                                   #wait until a station is clicked
        return px.line(title="Click a station on the map", template="plotly_dark")

    station_id = clickData["points"][0]["customdata"][0]    #get station ID from clickData
    df_station = df[df["station"] == station_id]            #filter dataframe for selected station
        #create line plot for annual mean temperature
    fig = px.line(
        df_station,
        x="year",
        y="annual_mean",
        title=f"{station_names[station_id]} ({station_id})",
        markers=True,
        template="plotly_dark"
    )
        #change y-axis title and background colors
    fig.update_layout(yaxis_title="°C", paper_bgcolor="#3c3c3c", plot_bgcolor="#6a6a6a")
    return fig

#callback to update monthly time series based on map click
@app.callback(
    Output("monthlyseries", "figure"),
    Input("map", "clickData")
)
#function to update monthly breakdown time series
def update_monthlyseries(clickData):
    if clickData is None:                                   #wait until a station is clicked
        return px.line(title="Click a station on the map", template="plotly_dark")

    station_id = clickData["points"][0]["customdata"][0]    #get station ID from clickData
    df_station = df[df["station"] == station_id]            #filter dataframe for selected station
        #reshape dataframe to long format for monthly plotting
    df_long = df_station.melt(
        id_vars=["year"],
        value_vars=mcols,
        var_name="month",
        value_name="temp"
    )
        #map monthly temp vals to month names
    month_names = {f"v{i}": name for i, name in enumerate(
        ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"], start=1)}
    df_long["month"] = df_long["month"].map(month_names)
        #create line plot for monthly temperature breakdown
    fig = px.line(
        df_long,
        x="year",
        y="temp",
        color="month",                     #different colour line for each month
        title=f"{station_names[station_id]} ({station_id})",
        markers=False,
        template="plotly_dark"
    )
        #change y-axis title and background colors
    fig.update_layout(yaxis_title="°C", paper_bgcolor="#3c3c3c", plot_bgcolor="#6a6a6a")
    return fig

#------------------------[run app]------------------------
if __name__ == "__main__":
    app.run(debug=True)
