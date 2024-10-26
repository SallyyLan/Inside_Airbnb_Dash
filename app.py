from dash import Dash, html, Input, Output, dcc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np

app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.DARKLY,  
        "https://use.fontawesome.com/releases/v5.15.4/css/all.css"
    ]
)

sydney_df = pd.read_csv("sydney_listings.csv")
melbourne_df = pd.read_csv("melbourne_listings.csv")
brisbane_df = pd.read_csv("brisbane_listings.csv")

server = app.server


# Map of States
state_dfs = {
    "Sydney": sydney_df,
    "Melbourne": melbourne_df,
    "Brisbane": brisbane_df
}



# Summary Card 
def summary_card(title, value):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H5(value, className="card-title", style={"color": "#FFFFFF"}),
                html.P(title, className="card-text", style={"color": "#B0B0B0"})
            ]
        ),
        className="shadow-sm text-center bg-dark",  # Dark background for a sleek look
        style={
            "marginTop": "20px", 
            "marginLeft": "10px",
            "height": "100px",
            "padding": "10px",
            "width": "500px"
        }
    )



# Graph titles with tooltips 
def graph_title_with_tooltip(title, tooltip_text, tooltip_id, summary_number=None):
    return [
        dbc.Row(
            [
                dbc.Col(html.H4(title, style={"color": "#FFFFFF"}), width="auto"),
                dbc.Col(
                    html.I(className="fas fa-question-circle ml-2", id=tooltip_id, style={"color": "#FFFFFF"}),
                    width="auto",
                    style={"cursor": "pointer"}
                )
            ],
            align="center",
            className="mb-2"
        ),
        dbc.Tooltip(
            html.Div(
                [html.P(paragraph) for paragraph in tooltip_text],
                style={"textAlign": "left"} 
            ),
            target=tooltip_id,
            placement='right',
            style={"maxWidth": "500px"}  
        )
    ]


AIRBNB_LOGO_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Airbnb_Logo_B%C3%A9lo.svg/1200px-Airbnb_Logo_B%C3%A9lo.svg.png"



# Layout
app.layout = dbc.Container([
    # Title and Summary Numbers 
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col(
                    html.Img(
                        src=AIRBNB_LOGO_URL,
                        height="70px",  
                        style={"marginRight": "10px"}
                    ),
                    width="auto",
                    className="d-flex align-items-center"
                ),
            ], align="center")
        ], width=6, className="d-flex align-items-center"),  


        # Summaries Column
        dbc.Col([
            dbc.Row([
                dbc.Col(
                    summary_card("Average Income", html.Span(id='average_income', style={"fontSize": "1.2em"})),
                    xs=12, sm=6, md=4, className="d-flex justify-content-center mb-2"
                ),
                dbc.Col(
                    summary_card("Average Stay", html.Span(id='average_nights', style={"fontSize": "1.2em"})),
                    xs=12, sm=6, md=4, className="d-flex justify-content-center mb-2"
                ),
                dbc.Col(
                    summary_card("Total Listings", html.Span(id='total_listings', style={"fontSize": "1.2em"})),
                    xs=12, sm=6, md=4, className="d-flex justify-content-center mb-2"
                ),
            ], className="w-100 justify-content-end")  
        ], width=6)
    ], align="right", className="mb-4"),


    # Dropdowns
    dbc.Row([
        dbc.Col([
            html.Label("Select State:", style={"color": "#FFFFFF", "fontSize": "1.4em"}),
            dcc.Dropdown(
                id="state_dropdown",
                options=[
                    {"label": "Sydney", "value": "Sydney"},
                    {"label": "Melbourne", "value": "Melbourne"},
                    {"label": "Brisbane", "value": "Brisbane"}
                ],
                value="Sydney",
                placeholder="Choose a State",  
                style={
                    "backgroundColor": "#FFFFFF", 
                    "color": "#2C2C2C",  
                    "border": "1px solid #555555"
                },
                className="custom-dropdown"
            )
        ], width=12, md=4, className="mb-4"),
        dbc.Col([
            html.Label("Select Neighborhood:", style={"color": "#FFFFFF", "fontSize": "1.4em"}),
            dcc.Dropdown(
                id="neighborhood_dropdown",
                options=[],
                placeholder="Choose a Neighborhood",  
                value='All',
                style={
                    "backgroundColor": "#FFFFFF", 
                    "color": "#2C2C2C",  
                    "border": "1px solid #555555"
                },
                className="custom-dropdown"
            )
        ], width=12, md=4, className="mb-4"),
        dbc.Col([
            html.Label("Select Room Type:", style={"color": "#FFFFFF", "fontSize": "1.4em"}),
            dcc.Dropdown(
                id="roomtype_dropdown",
                options=[
                    {'label': 'All', 'value': 'All'},
                    {'label': 'Entire home/apt', 'value': 'Entire home/apt'},
                    {'label': 'Private room', 'value': 'Private room'},
                    {'label': 'Shared room', 'value': 'Shared room'},
                    {'label': 'Hotel room', 'value': 'Hotel room'}
                ],
                value='All',
                placeholder="Choose a Room Type",  
                style={
                    "backgroundColor": "#FFFFFF", 
                    "color": "#2C2C2C",  
                    "border": "1px solid #555555"
                },
                className="custom-dropdown"
            )
        ], width=12, md=4, className="mb-4")
    ], className="mb-4"),


    # Map Graph
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="map_graph", figure={}, config={"displayModeBar": True})
        ], width=12)
    ], style={"marginTop": "-30px", "marginBottom": "30px"}),

    # First Row of Graphs 
    dbc.Row([
        dbc.Col(
            graph_title_with_tooltip(
                title="Room Type Distribution",
                tooltip_text=[
                    "Airbnb hosts can list entire homes/apartments, private, shared rooms, and more recently hotel rooms.", 
                    "Depending on the room type and activity, a residential Airbnb listing could be more like a hotel, disruptive for neighbours, taking away housing, and illegal."
                ],
                tooltip_id="roomtype-tooltip",
            ) + [dcc.Graph(id="roomtype_graph")],
            width=12, md=6, className="mb-4"
        ),

        dbc.Col(
            graph_title_with_tooltip(
                title="Estimated Nights Booked",
                tooltip_text=[
                    "The minimum stay, price and number of reviews have been used to estimate the number of nights booked and the income for each listing, for the last 12 months.",
                    "Is the home, apartment or room rented frequently and displacing units of housing and residents? Does the income from Airbnb incentivise short-term rentals vs long-term housing?"
                ],
                tooltip_id="occupancy-tooltip",
            ) + [dcc.Graph(id="occupancy_graph")],
            width=12, md=6, className="mb-4"
        )
    ], className="mb-4"),


    # Second Row 
    dbc.Row([
        dbc.Col(
            graph_title_with_tooltip(
                title="Short-term Rentals (Minimum Nights)",
                tooltip_text=[
                    "The housing policies of cities and towns can be restrictive of short-term rentals, to protect housing for residents.",
                    "By looking at the 'minimum nights' setting for listings, we can see if the market has shifted to longer-term stays. Was it to avoid regulations, or in response to changes in travel demands?",
                    "In some cases, Airbnb has moved large numbers of their listings to longer stays to avoid short-term rental regulations and accountability."
                ],
                tooltip_id="shortrental-tooltip",
            ) + [dcc.Graph(id="shortrental_graph")],
            width=12, md=6, className="mb-4"
        ),
        dbc.Col(
            graph_title_with_tooltip(
                title="Distribution of Hosts by Number of Properties",
                tooltip_text=[
                    "Some Airbnb hosts have multiple listings.",
                    "A host may list separate rooms in the same apartment, or multiple apartments or homes available in their entirety.",
                    "Hosts with multiple listings are more likely to be running a business, are unlikely to be living in the property, and in violation of most short-term rental laws designed to protect residential housing."
                ],
                tooltip_id="listperhost-tooltip",
            ) + [dcc.Graph(id="listperhost_graph")],
            width=12, md=6, className="mb-4"
        )
    ])
], fluid=True)


# Callback for updating Neighborhood dropdown 
@app.callback(
    [Output("neighborhood_dropdown", "options"),
     Output("neighborhood_dropdown", "value")],
    [Input("state_dropdown", "value")]
)
def update_neighborhood_dropdown(selected_state):
    if selected_state is None:
        return [], None
    else:
        df = state_dfs[selected_state]
        neighborhoods = df["neighbourhood"].dropna().unique()
        options = [{'label': 'All', 'value': 'All'}] + [{"label": n, "value": n} for n in sorted(neighborhoods)]
        value = 'All'
        return options, value



# Callback for updating graphs 
@app.callback(
    [
        Output("map_graph", "figure"),
        Output("shortrental_graph", "figure"),
        Output("listperhost_graph", "figure"),  
        Output("roomtype_graph", "figure"),
        Output('average_income', 'children'),
        Output('average_nights', 'children'),
        Output('total_listings', 'children'), 
        Output("occupancy_graph", "figure")
    ],
    [
        Input("state_dropdown", "value"),
        Input("neighborhood_dropdown", "value"),
        Input("roomtype_dropdown", "value")
    ]
)
def update_graph(state_dropdown, neighborhood_dropdown, roomtype_dropdown):
    # Filter data 
    filtered_state = state_dfs[state_dropdown]
    filtered_state = filtered_state.dropna(subset=["latitude", "longitude"])

    # Total listings 
    total_state_listings = filtered_state.shape[0]


    # Filter neighborhood
    if neighborhood_dropdown and neighborhood_dropdown != "All":
        filtered_data = filtered_state[filtered_state["neighbourhood"] == neighborhood_dropdown]
    else:
        filtered_data = filtered_state


    # Filter room type
    if roomtype_dropdown and roomtype_dropdown != "All":
        filtered_data = filtered_data[filtered_data["room_type"] == roomtype_dropdown]


    # Additional filtering and calculations
    filtered_data = filtered_data.dropna(subset=['price', 'minimum_nights', 'number_of_reviews'])

    filtered_data['price'] = pd.to_numeric(filtered_data['price'], errors='coerce')
    filtered_data['minimum_nights'] = pd.to_numeric(filtered_data['minimum_nights'], errors='coerce')
    filtered_data['number_of_reviews'] = pd.to_numeric(filtered_data['number_of_reviews'], errors='coerce')
    filtered_data = filtered_data.dropna(subset=['price', 'minimum_nights', 'number_of_reviews'])


    # Estimated nights booked and income
    filtered_data['estimated_nights_booked'] = filtered_data['number_of_reviews'] * filtered_data['minimum_nights']
    filtered_data['estimated_income'] = filtered_data['estimated_nights_booked'] * filtered_data['price']


    # Calculate summary numbers 
    average_income = filtered_data['estimated_income'].mean()
    average_nights_booked = filtered_data['estimated_nights_booked'].mean()
    total_listings = filtered_data.shape[0]  


    # Summary Divs
    average_income_content = f"${average_income:,.2f}" if not np.isnan(average_income) else "N/A"
    average_nights_content = f"{average_nights_booked:,.2f} nights" if not np.isnan(average_nights_booked) else "N/A"
    total_listings_content = f"{total_listings:,}" if not np.isnan(total_listings) else "N/A"


    zoom_level = 12 if neighborhood_dropdown and neighborhood_dropdown != "All" else 9

    # Map center
    if not filtered_data.empty:
        map_center = {
            "lat": filtered_data["latitude"].mean(),
            "lon": filtered_data["longitude"].mean()
        }
    else:
        map_center = {
            "lat": filtered_state["latitude"].mean(),
            "lon": filtered_state["longitude"].mean()
        }

    # Map Figure 
    map_figure = px.scatter_mapbox(
        filtered_data,
        lat='latitude',
        lon='longitude',
        hover_name='name',
        hover_data={
            'price': True,
            'estimated_income': True,
            'latitude': False,    
            'longitude': False    
        },
        zoom=zoom_level,
        center=map_center,
        height=600
    )

    map_figure.update_layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        plot_bgcolor="#2C2C2C",  
        paper_bgcolor="#2C2C2C"  
    )

    map_figure.update_traces(marker=dict(size=8, color='#FF6347'))  




    # Room Type Distribution
    room_type_counts = filtered_data['room_type'].value_counts().sort_values(ascending=True).reset_index()
    room_type_counts.columns = ['room_type', 'count']
    roomtype_fig = px.bar(
        room_type_counts,
        x='count',
        y='room_type',
        orientation='h',
        labels={'count': 'Number of Listings', 'room_type': 'Room Type'},
        height=490 
    )
    roomtype_fig.update_layout(
        margin={"l": 100},
        plot_bgcolor="#2C2C2C",
        paper_bgcolor="#2C2C2C",
        font_color="#FFFFFF",
        xaxis=dict(
            categoryorder='array',
            categoryarray=room_type_counts['room_type'],
            color="#FFFFFF"
        ),
        yaxis=dict(
            color="#FFFFFF"
        )
    )
    roomtype_fig.update_traces(marker=dict(color="#FF6347"))  




    # Short-term Rentals Graph 
    short_term_counts = filtered_data['minimum_nights'].value_counts().reset_index().head(10)
    short_term_counts.columns = ['minimum_nights', 'count']
    shortrental_fig = px.bar(
        short_term_counts,
        x='minimum_nights',
        y='count',
        labels={'minimum_nights': 'Minimum Nights', 'count': 'Number of Listings'},
        height=490 
    )
    shortrental_fig.update_layout(
        margin={"l": 50, "r": 50},
        plot_bgcolor="#2C2C2C",
        paper_bgcolor="#2C2C2C",
        font_color="#FFFFFF",
        xaxis=dict(
            showgrid=False, 
            color="#FFFFFF"
        ),
        yaxis=dict(
            color="#FFFFFF"
        )
    )
    shortrental_fig.update_traces(marker=dict(color='#FF6347'))



    # Listings per Host Distribution 
    listings_per_host = filtered_data.groupby('host_id').size().reset_index(name='listing_count')

    bins = list(range(1, 11))  
    bins.append(np.inf)         

    labels_bins = [str(i) for i in range(1, 10)] + ['10+']  

    listings_per_host['listing_bin'] = pd.cut(
        listings_per_host['listing_count'],
        bins=bins,
        labels=labels_bins,
        right=False,
        include_lowest=True
    )

    host_distribution = listings_per_host['listing_bin'].value_counts().reindex(labels_bins).fillna(0).astype(int).reset_index()
    host_distribution.columns = ['property_count', 'host_count']

    listperhost_fig = px.bar(
        host_distribution,
        x='property_count',
        y='host_count',
        labels={'property_count': 'Number of Properties', 'host_count': 'Number of Hosts'},
        text='host_count',
        height=490
    )

    listperhost_fig.update_layout(
        xaxis=dict(
            categoryorder='array',
            categoryarray=labels_bins,
            showgrid=False,  
            color="#FFFFFF"
        ),
        yaxis=dict(
            title='Number of Hosts',
            color="#FFFFFF"
        ),
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        margin={"l": 50, "r": 50},
        plot_bgcolor="#2C2C2C",
        paper_bgcolor="#2C2C2C",
        font_color="#FFFFFF"
    )

    listperhost_fig.update_traces(texttemplate='%{text}', textposition='outside', marker=dict(color="#FF6347"))



    # Occupancy Bar Chart
    occupancy_counts = filtered_data['estimated_nights_booked'].copy()

    bins_occupancy = [0, 50, 100, 150, 200, 250, np.inf]
    labels_bins_occupancy = ['0-49', '50-99', '100-149', '150-199', '200-249', '250+']

    occupancy_binned = pd.cut(
        occupancy_counts,
        bins=bins_occupancy,
        labels=labels_bins_occupancy,
        right=False  
    )

    occupancy_data = occupancy_binned.value_counts().reindex(labels_bins_occupancy).reset_index()
    occupancy_data.columns = ['occupancy_range', 'count']

    occupancy_fig = px.bar(
        occupancy_data,
        x='occupancy_range',
        y='count',
        labels={'occupancy_range': 'Occupancy Range', 'count': 'Number of Listings'},
        text='count',
        height=490 
    )

    occupancy_fig.update_layout(
        xaxis=dict(
            categoryorder='array',
            categoryarray=labels_bins_occupancy,
            showgrid=False,  
            color="#FFFFFF"
        ),
        yaxis=dict(
            title='Number of Listings',
            color="#FFFFFF"
        ),
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        margin={"l": 50, "r": 50},
        plot_bgcolor="#2C2C2C",
        paper_bgcolor="#2C2C2C",
        font_color="#FFFFFF"
    )

    occupancy_fig.update_traces(texttemplate='%{text}', textposition='outside', marker=dict(color="#FF6347"))





    return (
        map_figure,
        shortrental_fig,
        listperhost_fig,
        roomtype_fig,
        average_income_content,
        average_nights_content,
        total_listings_content, 
        occupancy_fig
    )

if __name__ == '__main__':
    app.run_server(debug=True)
