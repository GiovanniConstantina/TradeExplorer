"""
Global Energy Trade Explorer
Dashboard for comparative evaluation of data visualization techniques

Study Design: Users complete Google Form tasks while freely exploring this dashboard.

Author: Constantina Giovanni
Institution: Newcastle University
Module: CSC3094 - Computing Project
Year: 2026
"""

import dash
from dash import html, dcc, Input, Output, State, ctx
import plotly.graph_objects as go
import pandas as pd
import numpy as np


# DASH APP SETUP
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
        {%css%}
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { background: #08090c; font-family: 'Inter', sans-serif; }
            #_dash-app-content { max-width: 1440px; margin: 0 auto; }

            /* Dropdown styles */
            .Select-control { background: #12151c !important; border: none !important; }
            .Select-value-label { color: #e8eaf0 !important; }
            .Select-menu-outer { background: #12151c !important; border: 1px solid rgba(255,255,255,0.06) !important; }
            .VirtualizedSelectOption { color: #e8eaf0 !important; }
            .VirtualizedSelectFocusedOption { background: #1e2330 !important; }
            .Select-arrow { border-color: #5a5f70 transparent transparent !important; }

            /* Slider styles */
            .rc-slider-mark-text { color: #8b90a0 !important; font-size: 11px !important; }
            .rc-slider-mark-text-active { color: #e8eaf0 !important; }
            .rc-slider-rail { background: #1e2330 !important; }
            .rc-slider-track { background: #3b82f6 !important; }
            .rc-slider-handle { border-color: #3b82f6 !important; background: #3b82f6 !important; }

            /* Visualization tab styles */
            .viz-tab {
                padding: 12px 24px;
                background: #12151c;
                border: 1.5px solid #2a2f40;
                color: #9499a8;
                font-size: 13px;
                font-family: 'Inter', sans-serif;
                font-weight: 500;
                cursor: pointer;
                border-radius: 6px;
                transition: all 0.2s;
                display: inline-flex;
                align-items: center;
                gap: 8px;
            }
            .viz-tab:hover {
                border-color: #3b82f6;
                color: #e8eaf0;
                transform: translateY(-1px);
            }
            .viz-tab.active {
                background: #3b82f6;
                border-color: #3b82f6;
                color: white;
                box-shadow: 0 4px 12px rgba(59,130,246,0.3);
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        {%config%}
        {%scripts%}
        {%renderer%}
    </body>
</html>
'''
app.title = 'Global Energy Trade Explorer'


# DATA LOADING
df = pd.read_csv('data/trade_data_cleaned.csv')


# THEME COLORS
background_color = '#08090c'
card_color = '#0d0f14'
input_color = '#12151c'
text1_color = '#e8eaf0'
text2_color = '#9499a8'
text3_color = '#4a4f5e'
accent_color = '#3b82f6'
success_color = '#10b981'
warning_color = '#f59e0b'
danger_color = '#ef4444'

regions_colors = {
    'Americas': '#ef4444',
    'Europe / CIS': '#3b82f6',
    'Middle East': '#f59e0b',
    'Asia / Pacific': '#10b981',
    'Africa': '#a855f7',
}


def hex_to_rgba(hex_color, alpha=0.5):
    """Convert hex color to rgba with specified alpha."""
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f'rgba({r},{g},{b},{alpha})'



# Story Telling
insights = {
    'All': {
        'title': 'No single visualisation tells the full story',
        'body': 'The Sankey reveals that Canada to USA dwarfs all other flows. The choropleth shows geographic clustering of exporters. The chord diagram exposes hub-and-spoke dependency structures. Each technique serves a distinct analytical purpose.'
    },
    'Americas': {
        'title': 'A continental pipeline system',
        'body': 'The Canada-USA corridor is the single largest bilateral energy relationship. The USA also exports significantly to Mexico and Canada. Colombia and Trinidad & Tobago supply the US market.'
    },
    'Europe / CIS': {
        'title': 'Russia — the hub Europe depended on',
        'body': 'Russia was the most connected energy exporter, supplying Germany, Netherlands, Poland, Finland, and many others. Norway serves as the key alternative supplier.'
    },
    'Middle East': {
        'title': "The world's fuel station",
        'body': 'Saudi Arabia, Iraq, and Qatar form the export core. Saudi Arabia alone appears in numerous top flows. Qatar specialises in LNG exports to Asia.'
    },
    'Asia / Pacific': {
        'title': "The world's largest energy importers",
        'body': 'China receives energy from the most diverse set of sources. Japan and South Korea depend heavily on Middle Eastern and Australian energy. Indonesia and Australia are the major regional exporters.'
    },
    'Africa': {
        'title': 'Resource-rich exporters supplying distant markets',
        'body': 'Nigeria and Angola are the dominant African energy exporters, supplying China, India, and European markets. Algeria supplies Southern Europe.'
    },
}


# COUNTRY NAMES MAPPING
country_names = {
    'CAN': 'Canada', 'USA': 'United States', 'MEX': 'Mexico', 'COL': 'Colombia',
    'BRA': 'Brazil', 'ARG': 'Argentina', 'TTO': 'Trinidad & Tobago', 'CHL': 'Chile',
    'VEN': 'Venezuela', 'ECU': 'Ecuador', 'PER': 'Peru', 'BOL': 'Bolivia',
    'RUS': 'Russia', 'NOR': 'Norway', 'GBR': 'United Kingdom', 'NLD': 'Netherlands',
    'DEU': 'Germany', 'POL': 'Poland', 'FIN': 'Finland', 'BLR': 'Belarus',
    'CZE': 'Czechia', 'HUN': 'Hungary', 'SVK': 'Slovakia', 'AUT': 'Austria',
    'FRA': 'France', 'ITA': 'Italy', 'BEL': 'Belgium', 'ESP': 'Spain',
    'SWE': 'Sweden', 'DNK': 'Denmark', 'UKR': 'Ukraine', 'GRC': 'Greece',
    'PRT': 'Portugal', 'ROU': 'Romania', 'BGR': 'Bulgaria', 'HRV': 'Croatia',
    'IRL': 'Ireland', 'CHE': 'Switzerland', 'SRB': 'Serbia', 'SVN': 'Slovenia',
    'LTU': 'Lithuania', 'LVA': 'Latvia', 'EST': 'Estonia',
    'SAU': 'Saudi Arabia', 'IRQ': 'Iraq', 'IRN': 'Iran', 'QAT': 'Qatar',
    'KWT': 'Kuwait', 'OMN': 'Oman', 'ARE': 'UAE', 'BHR': 'Bahrain',
    'CHN': 'China', 'JPN': 'Japan', 'KOR': 'South Korea', 'IND': 'India',
    'AUS': 'Australia', 'TUR': 'Turkey', 'IDN': 'Indonesia', 'THA': 'Thailand',
    'SGP': 'Singapore', 'MYS': 'Malaysia', 'VNM': 'Vietnam', 'PAK': 'Pakistan',
    'PHL': 'Philippines', 'BGD': 'Bangladesh', 'TWN': 'Taiwan', 'BRN': 'Brunei',
    'NZL': 'New Zealand', 'KAZ': 'Kazakhstan', 'MNG': 'Mongolia',
    'NGA': 'Nigeria', 'ZAF': 'South Africa', 'EGY': 'Egypt', 'DZA': 'Algeria',
    'AGO': 'Angola', 'LBY': 'Libya', 'MAR': 'Morocco', 'GHA': 'Ghana',
    'TZA': 'Tanzania', 'KEN': 'Kenya', 'CMR': 'Cameroon', 'GAB': 'Gabon',
    'COG': 'Congo', 'GNQ': 'Eq. Guinea', 'TCD': 'Chad', 'SDN': 'Sudan',
    'AZE': 'Azerbaijan', 'MOZ': 'Mozambique',
}


def get_name(iso):
    """Get country full name from ISO code."""
    return country_names.get(iso, iso)



# PLOTLY CONFIGURATION
sankey_config = {
    'displayModeBar': True,
    'modeBarButtonsToRemove': ['lasso2d', 'select2d', 'zoom2d', 'pan2d', 'zoomIn2d', 'zoomOut2d'],
    'displaylogo': False,
}

choropleth_config = {
    'displayModeBar': True,
    'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
    'displaylogo': False,
    'scrollZoom': True,
}


# APP LAYOUT AND DESIGN
app.layout = html.Div([
    # Hidden store for active visualization tracking
    dcc.Store(id='active-viz', data='sankey'),

    # Header
    html.Div([
        html.H1('UN Comtrade HS27 - 2020-2022', style={
            'textAlign': 'left', 'color': 'white', 'fontWeight': '100',
            'fontSize': '13px', 'marginLeft': '30px', 'marginTop': '20px',
            'fontFamily': 'Open Sans', 'letterSpacing': '0.1em', 'marginBottom': '4px'
        }),
        html.H1('Global Energy Trade Explorer', style={
            'textAlign': 'left', 'marginLeft': '30px', 'color': 'white',
            'fontWeight': '400', 'fontSize': '20px',
            'fontFamily': 'Open Sans', 'letterSpacing': '0.1em'
        }),
    ], style={
        'padding': '16px 40px',
        'borderBottom': '1px solid rgba(255,255,255,0.04)'
    }),

    # Region Filter
    html.Div([
        html.Span('REGION', style={
            'fontFamily': 'monospace', 'fontSize': '14px',
            'color': text3_color, 'letterSpacing': '0.08em'
        }),
        dcc.RadioItems(
            id='region-filter',
            options=[
                {'label': 'All', 'value': 'All'},
                {'label': 'Americas', 'value': 'Americas'},
                {'label': 'Europe / CIS', 'value': 'Europe / CIS'},
                {'label': 'Middle East', 'value': 'Middle East'},
                {'label': 'Asia / Pacific', 'value': 'Asia / Pacific'},
                {'label': 'Africa', 'value': 'Africa'},
            ],
            value='All',
            inline=True,
            labelStyle={
                'color': text2_color, 'fontSize': '12px',
                'fontFamily': 'Inter, sans-serif', 'padding': '6px 14px',
                'cursor': 'pointer'
            },
            inputStyle={'marginRight': '6px', 'accentColor': accent_color},
        ),
    ], style={
        'background': card_color, 'padding': '10px 40px',
        'display': 'flex', 'alignItems': 'center', 'gap': '16px',
        'borderBottom': '1px solid rgba(255,255,255,0.04)'
    }),

    # Control Bar
    html.Div([
        # Year
        html.Div([
            html.Span('YEAR', style={
                'fontFamily': 'monospace', 'fontSize': '14px',
                'color': text3_color, 'letterSpacing': '0.08em'
            }),
            dcc.Dropdown(
                id='year-dropdown',
                options=[
                    {'label': '2020', 'value': 2020},
                    {'label': '2021', 'value': 2021},
                    {'label': '2022', 'value': 2022}
                ],
                value=2021,
                clearable=False,
                style={
                    'width': '100px', 'backgroundColor': input_color,
                    'color': 'black', 'border': 'none', 'fontSize': '14px'
                }
            ),
        ], style={'display': 'flex', 'alignItems': 'center', 'gap': '8px'}),

        # Flow Type
        html.Div([
            html.Span('FLOW', style={
                'fontFamily': 'monospace', 'fontSize': '14px',
                'color': text3_color, 'letterSpacing': '0.08em'
            }),
            dcc.Dropdown(
                id='flow-dropdown',
                options=[
                    {'label': 'Export', 'value': 'Export'},
                    {'label': 'Import', 'value': 'Import'}
                ],
                value='Export',
                clearable=False,
                style={
                    'width': '110px', 'backgroundColor': input_color,
                    'color': 'black', 'border': 'none', 'fontSize': '14px'
                }
            ),
        ], style={'display': 'flex', 'alignItems': 'center', 'gap': '8px'}),

        # Top-N Slider
        html.Div([
            html.Span('TOP-N', style={
                'fontFamily': 'monospace', 'fontSize': '14px',
                'color': text3_color, 'letterSpacing': '0.08em', 'marginRight': '5px'
            }),
            dcc.Slider(
                id='top-n-slider',
                min=10, max=50, step=5, value=20,
                marks={
                    10: {'label': '10', 'style': {'color': '#8b90a0'}},
                    20: {'label': '20', 'style': {'color': '#8b90a0'}},
                    30: {'label': '30', 'style': {'color': '#8b90a0'}},
                    40: {'label': '40', 'style': {'color': '#8b90a0'}},
                    50: {'label': '50', 'style': {'color': '#8b90a0'}},
                }
            ),
            html.Span('Sankey only', style={
                'fontFamily': 'monospace', 'fontSize': '10px',
                'color': text3_color, 'letterSpacing': '0.06em',
                'marginLeft': '6px', 'whiteSpace': 'nowrap'
            }),
        ], style={'display': 'flex', 'alignItems': 'center', 'gap': '8px', 'width': '260px'}),

        # Search
        html.Div([
            html.Span('SEARCH', style={
                'fontFamily': 'monospace', 'fontSize': '14px',
                'color': text3_color, 'letterSpacing': '0.08em', 'marginRight': '5px'
            }),
            dcc.Input(
                id='search-input',
                type='text',
                placeholder='Enter country name or code...',
                debounce=True,
                style={
                    'width': '250px', 'fontSize': '12px', 'padding': '6px 10px',
                    'borderRadius': '6px', 'border': '1px solid rgba(255,255,255,0.06)',
                    'background': input_color, 'color': text1_color, 'outline': 'none'
                }
            ),
        ], style={'display': 'flex', 'alignItems': 'center', 'gap': '8px'}),
    ], style={
        'background': card_color, 'padding': '10px 40px',
        'display': 'flex', 'alignItems': 'center', 'gap': '32px',
        'flexWrap': 'wrap', 'borderBottom': '1px solid rgba(255,255,255,0.04)'
    }),

    # Metric Row
    html.Div([
        html.Div([
            html.Div('TOTAL TRADE', style={
                'fontFamily': 'monospace', 'fontSize': '15px',
                'color': text3_color, 'letterSpacing': '0.08em', 'marginBottom': '4px'
            }),
            html.Div(id='m-val', style={
                'fontSize': '24px', 'fontWeight': '600', 'color': text1_color
            }),
            html.Div(id='m-val-sub', style={'fontSize': '10px', 'color': text3_color}),
        ], style={
            'background': card_color, 'borderRadius': '10px', 'padding': '14px 16px',
            'border': '1px solid rgba(255,255,255,0.03)'
        }),

        html.Div([
            html.Div('COUNTRIES', style={
                'fontFamily': 'monospace', 'fontSize': '15px',
                'color': text3_color, 'letterSpacing': '0.08em', 'marginBottom': '4px'
            }),
            html.Div(id='m-cnt', style={
                'fontSize': '24px', 'fontWeight': '600', 'color': text1_color
            }),
        ], style={
            'background': card_color, 'borderRadius': '10px', 'padding': '14px 16px',
            'border': '1px solid rgba(255,255,255,0.03)'
        }),

        html.Div([
            html.Div('FLOWS', style={
                'fontFamily': 'monospace', 'fontSize': '15px',
                'color': text3_color, 'letterSpacing': '0.08em', 'marginBottom': '4px'
            }),
            html.Div(id='m-flw', style={
                'fontSize': '24px', 'fontWeight': '600', 'color': text1_color
            }),
        ], style={
            'background': card_color, 'borderRadius': '10px', 'padding': '14px 16px',
            'border': '1px solid rgba(255,255,255,0.03)'
        }),

        html.Div([
            html.Div('TOP EXPORTER', style={
                'fontFamily': 'monospace', 'fontSize': '15px',
                'color': text3_color, 'letterSpacing': '0.08em', 'marginBottom': '4px'
            }),
            html.Div(id='m-exp', style={
                'fontSize': '24px', 'fontWeight': '600', 'color': text1_color
            }),
            html.Div(id='m-exp-sub', style={'fontSize': '10px', 'color': text3_color}),
        ], style={
            'background': card_color, 'borderRadius': '10px', 'padding': '14px 16px',
            'border': '1px solid rgba(255,255,255,0.03)'
        }),

        html.Div([
            html.Div('YoY CHANGE', style={
                'fontFamily': 'monospace', 'fontSize': '15px',
                'color': text3_color, 'letterSpacing': '0.08em', 'marginBottom': '4px'
            }),
            html.Div(id='m-yoy', style={
                'fontSize': '24px', 'fontWeight': '600', 'color': text1_color
            }),
            html.Div(id='m-yoy-sub', style={'fontSize': '10px', 'color': text3_color}),
        ], style={
            'background': card_color, 'borderRadius': '10px', 'padding': '14px 16px',
            'border': '1px solid rgba(255,255,255,0.03)'
        }),
    ], style={
        'display': 'grid', 'gridTemplateColumns': 'repeat(5, 1fr)',
        'gap': '10px', 'padding': '20px 40px 10px'
    }),

    # Visualization Selector Tabs
    html.Div([
        html.Div('SELECT VISUALIZATION', style={
            'fontFamily': 'monospace', 'fontSize': '10px',
            'color': text3_color, 'letterSpacing': '0.14em',
            'marginBottom': '12px', 'fontWeight': '600'
        }),
        html.Div([
            html.Button([
                html.Span( style={'fontSize': '16px'}),
                'Sankey Diagram'
            ], id='tab-sankey', n_clicks=0, className='viz-tab active'),

            html.Button([
                html.Span( style={'fontSize': '16px'}),
                'Choropleth Map'
            ], id='tab-choropleth', n_clicks=0, className='viz-tab'),

            html.Button([
                html.Span( style={'fontSize': '16px'}),
                'Chord Diagram'
            ], id='tab-chord', n_clicks=0, className='viz-tab'),
        ], style={'display': 'flex', 'gap': '12px', 'flexWrap': 'wrap'}),

        html.Div([
            html.Span( style={'fontSize': '14px'}),
            html.Span(
                'Switch between visualizations to compare different views of the data. Each technique reveals different patterns.',
                style={'fontSize': '11px', 'color': text2_color, 'fontStyle': 'italic'}
            )
        ], style={
            'marginTop': '12px', 'padding': '10px 14px',
            'background': 'rgba(59,130,246,0.05)', 'borderRadius': '4px',
            'border': '1px solid rgba(59,130,246,0.1)'
        }),
    ], style={'padding': '20px 40px 16px', 'marginTop': '4px'}),

    # Visualizations Section
    html.Div([
        # Sankey Diagram
        html.Div(id='sankey-container', children=[
            html.Div([
                html.Span('01', style={
                    'fontFamily': 'monospace', 'fontSize': '10px', 'fontWeight': '600',
                    'color': accent_color, 'background': 'rgba(59,130,246,0.08)',
                    'padding': '2px 8px', 'borderRadius': '4px'
                }),
                html.Span('Sankey diagram — Trade flow magnitude', style={
                    'fontSize': '13px', 'fontWeight': '600', 'color': text1_color
                }),
                html.Span('  (values scaled using √ transform for readability)', style={
                    'fontSize': '10px', 'color': text3_color, 'marginLeft': '8px'
                }),
            ], style={'display': 'flex', 'alignItems': 'center', 'gap': '10px', 'marginBottom': '12px'}),
            dcc.Graph(id='sankey-chart', config=sankey_config, style={'height': '700px'})
        ], style={
            'background': card_color, 'borderRadius': '12px', 'padding': '20px 24px',
            'marginBottom': '16px', 'border': '1px solid rgba(255,255,255,0.03)',
            'display': 'block'
        }),

        # Choropleth Map
        html.Div(id='choro-container', children=[
            html.Div([
                html.Span('02', style={
                    'fontFamily': 'monospace', 'fontSize': '10px', 'fontWeight': '600',
                    'color': accent_color, 'background': 'rgba(59,130,246,0.08)',
                    'padding': '2px 8px', 'borderRadius': '4px'
                }),
                html.Span('Choropleth — Geographic distribution', style={
                    'fontSize': '13px', 'fontWeight': '600', 'color': text1_color
                }),
                html.Span('  (scroll to zoom · drag to pan)', style={
                    'fontSize': '10px', 'color': text3_color, 'marginLeft': '8px'
                }),
            ], style={'display': 'flex', 'alignItems': 'center', 'gap': '10px', 'marginBottom': '12px'}),
            dcc.Graph(id='choro-chart', config=choropleth_config, style={'height': '500px'}),
        ], style={
            'background': card_color, 'borderRadius': '12px', 'padding': '20px 24px',
            'marginBottom': '16px', 'border': '1px solid rgba(255,255,255,0.03)',
            'display': 'none'
        }),

        # Chord Diagram
        html.Div(id='chord-container', children=[
            html.Div([
                html.Span('03', style={
                    'fontFamily': 'monospace', 'fontSize': '10px', 'fontWeight': '600',
                    'color': accent_color, 'background': 'rgba(59,130,246,0.08)',
                    'padding': '2px 8px', 'borderRadius': '4px'
                }),
                html.Span('Chord diagram — Bilateral dependencies', style={
                    'fontSize': '13px', 'fontWeight': '600', 'color': text1_color
                }),
                html.Span('  (click a country to focus · hover ribbons for details)', style={
                    'fontSize': '10px', 'color': text3_color, 'marginLeft': '8px'
                }),
            ], style={'display': 'flex', 'alignItems': 'center', 'gap': '10px', 'marginBottom': '12px'}),
            html.Iframe(
                id='chord-iframe',
                src='/assets/chord_embed.html?region=All',
                style={
                    'width': '100%', 'height': '480px',
                    'border': 'none', 'borderRadius': '8px'
                },
            ),
        ], style={
            'background': card_color, 'borderRadius': '12px', 'padding': '20px 24px',
            'marginBottom': '16px', 'border': '1px solid rgba(255,255,255,0.03)',
            'display': 'none'
        }),

        # Insight Panel
        html.Div([
            html.Div('KEY INSIGHT', style={
                'fontFamily': 'monospace', 'fontSize': '9px',
                'color': accent_color, 'letterSpacing': '0.12em', 'marginBottom': '8px'
            }),
            html.Div(id='insight-title', style={
                'fontSize': '18px', 'fontWeight': '600',
                'color': text1_color, 'marginBottom': '8px'
            }),
            html.Div(id='insight-body', style={
                'fontSize': '13px', 'lineHeight': '1.75', 'color': text2_color
            }),
        ], style={
            'background': card_color, 'borderRadius': '12px', 'padding': '24px 28px',
            'marginBottom': '16px', 'border': '1px solid rgba(255,255,255,0.03)',
            'borderTop': f'2px solid {accent_color}'
        }),

        # Evaluation Table
        html.Div([
            html.Div([
                html.Span('04', style={
                    'fontFamily': 'monospace', 'fontSize': '10px', 'fontWeight': '600',
                    'color': accent_color, 'background': 'rgba(59,130,246,0.08)',
                    'padding': '2px 8px', 'borderRadius': '4px'
                }),
                html.Span('Heuristic evaluation — Godfrey 2016, Wang 2019', style={
                    'fontSize': '13px', 'fontWeight': '600', 'color': text1_color
                }),
            ], style={'display': 'flex', 'alignItems': 'center', 'gap': '10px', 'marginBottom': '16px'}),

            html.Table([
                html.Thead(html.Tr([
                    html.Th('Criteria', style={
                        'textAlign': 'left', 'color': text3_color, 'padding': '8px 12px',
                        'fontSize': '10px', 'fontFamily': 'monospace',
                        'borderBottom': '1px solid rgba(255,255,255,0.08)'
                    }),
                    html.Th('Sankey', style={
                        'textAlign': 'center', 'color': text3_color, 'padding': '8px 12px',
                        'fontSize': '10px', 'fontFamily': 'monospace',
                        'borderBottom': '1px solid rgba(255,255,255,0.08)'
                    }),
                    html.Th('Choropleth', style={
                        'textAlign': 'center', 'color': text3_color, 'padding': '8px 12px',
                        'fontSize': '10px', 'fontFamily': 'monospace',
                        'borderBottom': '1px solid rgba(255,255,255,0.08)'
                    }),
                    html.Th('Chord', style={
                        'textAlign': 'center', 'color': text3_color, 'padding': '8px 12px',
                        'fontSize': '10px', 'fontFamily': 'monospace',
                        'borderBottom': '1px solid rgba(255,255,255,0.08)'
                    }),
                ])),
                html.Tbody([
                    html.Tr([
                        html.Td('Volume encoding', style={'color': text2_color, 'padding': '10px 12px'}),
                        html.Td('High', style={'textAlign': 'center', 'color': success_color, 'padding': '10px'}),
                        html.Td('Med', style={'textAlign': 'center', 'color': warning_color, 'padding': '10px'}),
                        html.Td('Med', style={'textAlign': 'center', 'color': warning_color, 'padding': '10px'}),
                    ]),
                    html.Tr([
                        html.Td('Directional clarity', style={'color': text2_color, 'padding': '10px 12px'}),
                        html.Td('High', style={'textAlign': 'center', 'color': success_color, 'padding': '10px'}),
                        html.Td('Low', style={'textAlign': 'center', 'color': danger_color, 'padding': '10px'}),
                        html.Td('Med', style={'textAlign': 'center', 'color': warning_color, 'padding': '10px'}),
                    ]),
                    html.Tr([
                        html.Td('Geographic grounding', style={'color': text2_color, 'padding': '10px 12px'}),
                        html.Td('Low', style={'textAlign': 'center', 'color': danger_color, 'padding': '10px'}),
                        html.Td('High', style={'textAlign': 'center', 'color': success_color, 'padding': '10px'}),
                        html.Td('Low', style={'textAlign': 'center', 'color': danger_color, 'padding': '10px'}),
                    ]),
                    html.Tr([
                        html.Td('Structural clustering', style={'color': text2_color, 'padding': '10px 12px'}),
                        html.Td('Low', style={'textAlign': 'center', 'color': danger_color, 'padding': '10px'}),
                        html.Td('Med', style={'textAlign': 'center', 'color': warning_color, 'padding': '10px'}),
                        html.Td('High', style={'textAlign': 'center', 'color': success_color, 'padding': '10px'}),
                    ]),
                    html.Tr([
                        html.Td('Cognitive load', style={'color': text2_color, 'padding': '10px 12px'}),
                        html.Td('Med', style={'textAlign': 'center', 'color': warning_color, 'padding': '10px'}),
                        html.Td('Low', style={'textAlign': 'center', 'color': success_color, 'padding': '10px'}),
                        html.Td('Med', style={'textAlign': 'center', 'color': warning_color, 'padding': '10px'}),
                    ]),
                ]),
            ], style={'width': '100%', 'borderCollapse': 'collapse', 'fontSize': '12px'}),
        ], style={
            'background': card_color, 'borderRadius': '12px', 'padding': '20px 24px',
            'border': '1px solid rgba(255,255,255,0.03)'
        }),
    ], style={'padding': '10px 40px 40px'}),

    # Footer
    html.Footer([
        html.Div([
            'UN Comtrade HS27 (Mineral Fuels) · 2020–2022 · Export & Import flows',
            html.Br(),
            'Constantina Giovanni · Newcastle University · CSC3094 · 2026',
        ], style={
            'fontFamily': 'monospace', 'fontSize': '10px',
            'color': text3_color, 'letterSpacing': '0.04em', 'lineHeight': '2'
        }),
    ], style={
        'textAlign': 'center', 'padding': '32px',
        'borderTop': '1px solid rgba(255,255,255,0.04)'
    }),

], style={
    'background': background_color, 'minHeight': '100vh',
    'fontFamily': 'Inter, sans-serif', 'color': text1_color
})



# HELPER FUNCTIONS
def filter_data(region, year, flow='Export'):
    """Filter dataset by region, year, and flow direction."""
    dff = df[df['Year'] == year].copy()
    dff = dff[dff['Flow'] == flow]
    if region != 'All':
        dff = dff[(dff['Exporter_Region'] == region) | (dff['Importer_Region'] == region)]
    return dff


def find_country(search):
    """Find country ISO code from search term (case-insensitive, partial name match)."""
    if not search or not search.strip():
        return None
    q = search.strip().upper()
    # Exact ISO match first
    if q in country_names:
        return q
    # Partial name match
    for code, name in country_names.items():
        if q in name.upper():
            return code
    return None



# CALLBACKS

@app.callback(
    [Output('sankey-container', 'style'),
     Output('choro-container', 'style'),
     Output('chord-container', 'style'),
     Output('tab-sankey', 'className'),
     Output('tab-choropleth', 'className'),
     Output('tab-chord', 'className'),
     Output('active-viz', 'data')],
    [Input('tab-sankey', 'n_clicks'),
     Input('tab-choropleth', 'n_clicks'),
     Input('tab-chord', 'n_clicks')],
    prevent_initial_call=False
)
def toggle_visualization_tabs(sankey_clicks, choro_clicks, chord_clicks):
    """
    Control which visualization is visible based on tab selection.
    Only one visualization is shown at a time for clearer comparison.
    """
    button_id = ctx.triggered_id if ctx.triggered_id else 'tab-sankey'

    base_style = {
        'background': card_color,
        'borderRadius': '12px',
        'padding': '20px 24px',
        'marginBottom': '16px',
        'border': '1px solid rgba(255,255,255,0.03)'
    }

    if button_id == 'tab-sankey':
        return (
            {**base_style, 'display': 'block'},
            {**base_style, 'display': 'none'},
            {**base_style, 'display': 'none'},
            'viz-tab active', 'viz-tab', 'viz-tab',
            'sankey'
        )
    elif button_id == 'tab-choropleth':
        return (
            {**base_style, 'display': 'none'},
            {**base_style, 'display': 'block'},
            {**base_style, 'display': 'none'},
            'viz-tab', 'viz-tab active', 'viz-tab',
            'choropleth'
        )
    else:  # chord
        return (
            {**base_style, 'display': 'none'},
            {**base_style, 'display': 'none'},
            {**base_style, 'display': 'block'},
            'viz-tab', 'viz-tab', 'viz-tab active',
            'chord'
        )


@app.callback(
    [Output('m-val', 'children'), Output('m-val-sub', 'children'),
     Output('m-cnt', 'children'), Output('m-flw', 'children'),
     Output('m-exp', 'children'), Output('m-exp-sub', 'children'),
     Output('m-yoy', 'children'), Output('m-yoy-sub', 'children')],
    [Input('region-filter', 'value'),
     Input('year-dropdown', 'value'),
     Input('flow-dropdown', 'value')]
)
def update_metrics(region, year, flow):
    """Update summary metrics based on current filter settings."""
    dff = filter_data(region, year, flow)
    total = dff['Trade_Value_USD'].sum()
    countries = set(dff['Exporter'].unique()) | set(dff['Importer'].unique())
    n_flows = len(dff)

    exp_totals = dff.groupby('Exporter')['Trade_Value_USD'].sum()
    if len(exp_totals) > 0:
        top_exp = exp_totals.idxmax()
        exp_count = len(dff[dff['Exporter'] == top_exp])
    else:
        top_exp = '—'
        exp_count = 0

    # Format total value
    if total >= 1e12:
        val_str = f'${total / 1e12:.2f}T'
    else:
        val_str = f'${total / 1e9:.0f}B'

    # Calculate year-over-year change
    prev_year = year - 1
    if prev_year >= 2020:
        dff_prev = filter_data(region, prev_year, flow)
        total_prev = dff_prev['Trade_Value_USD'].sum()
        if total_prev > 0:
            pct_change = ((total - total_prev) / total_prev) * 100
            sign = '+' if pct_change >= 0 else ''
            yoy_str = f'{sign}{pct_change:.1f}%'
            yoy_sub = f'vs {prev_year}'
        else:
            yoy_str = 'N/A'
            yoy_sub = 'no prior data'
    else:
        yoy_str = '—'
        yoy_sub = 'no prior year'

    return (
        val_str,
        f'{n_flows} flows · {flow} · {year}',
        str(len(countries)),
        str(n_flows),
        get_name(top_exp),
        f'{exp_count} flows',
        yoy_str,
        yoy_sub
    )


@app.callback(
    Output('sankey-chart', 'figure'),
    [Input('region-filter', 'value'),
     Input('year-dropdown', 'value'),
     Input('top-n-slider', 'value'),
     Input('search-input', 'value'),
     Input('flow-dropdown', 'value')]
)
def update_sankey(region, year, topn, search, flow):
    """Generate Sankey diagram showing trade flows.

    When a searched country has very little data in the current flow direction
    (e.g. Saudi Arabia under-reports Exports to UN Comtrade), the callback
    automatically supplements with mirror-direction data so the country
    always appears visibly when searched.
    """
    dff = filter_data(region, year, flow)
    dff = dff.nlargest(topn, 'Trade_Value_USD')
    hl = find_country(search)

    # If searched country is invisible in current flow, pull its rows from mirror direction.
    # Fixes countries like SAU that under-report Exports to UN Comtrade.
    if hl:
        hl_visible = ((dff['Exporter'] == hl) | (dff['Importer'] == hl)).any()
        if not hl_visible:
            mirror_flow = 'Import' if flow == 'Export' else 'Export'
            dff_mirror = filter_data(region, year, mirror_flow)
            dff_mirror = dff_mirror[
                (dff_mirror['Exporter'] == hl) | (dff_mirror['Importer'] == hl)
            ].nlargest(min(topn, 10), 'Trade_Value_USD')
            dff = pd.concat([dff, dff_mirror]).drop_duplicates()

    if search and search.strip() and hl is None:
        fig = go.Figure()
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            annotations=[dict(
                text=f'No country found for "{search}".<br>Try "Russia" or "RUS".',
                x=0.5, y=0.5, xref='paper', yref='paper', showarrow=False,
                font=dict(color=danger_color, size=14)
            )]
        )
        return fig

    if dff.empty:
        fig = go.Figure()
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        return fig

    # Build node lists
    exporters = dff['Exporter'].unique().tolist()
    importers = dff['Importer'].unique().tolist()
    labels = [get_name(e) for e in exporters] + [get_name(i) + ' ' for i in importers]
    exp_idx = {e: i for i, e in enumerate(exporters)}
    imp_idx = {i: len(exporters) + j for j, i in enumerate(importers)}

    # Build links
    sources, targets, values, colors = [], [], [], []
    for _, row in dff.iterrows():
        src = exp_idx.get(row['Exporter'])
        tgt = imp_idx.get(row['Importer'])
        if src is not None and tgt is not None:
            sources.append(src)
            targets.append(tgt)
            values.append(np.sqrt(row['Trade_Value_USD']))
            c = regions_colors.get(row['Exporter_Region'], '#666')
            if hl and row['Exporter'] != hl and row['Importer'] != hl:
                colors.append('rgba(255,255,255,0.03)')
            else:
                colors.append(hex_to_rgba(c, 0.45))

    # Color nodes
    node_colors = []
    for e in exporters:
        if e in dff['Exporter'].values:
            reg = dff[dff['Exporter'] == e]['Exporter_Region'].iloc[0]
        else:
            reg = 'Africa'
        c = regions_colors.get(reg, '#666')
        if hl and e != hl:
            node_colors.append('rgba(255,255,255,0.1)')
        else:
            node_colors.append(c)

    for i in importers:
        if i in dff['Importer'].values:
            reg = dff[dff['Importer'] == i]['Importer_Region'].iloc[0]
        else:
            reg = 'Africa'
        c = regions_colors.get(reg, '#666')
        if hl and i != hl:
            node_colors.append('rgba(255,255,255,0.1)')
        else:
            node_colors.append(c)

    fig = go.Figure(go.Sankey(
        arrangement='snap',
        node=dict(pad=8, thickness=10, line=dict(width=0), label=labels, color=node_colors),
        link=dict(source=sources, target=targets, value=values, color=colors,
                  hovertemplate='%{source.label} → %{target.label}<br>%{value:,.0f}<extra></extra>')
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=text1_color, size=11),
        margin=dict(l=10, r=10, t=10, b=10)
    )

    return fig


@app.callback(
    Output('choro-chart', 'figure'),
    [Input('region-filter', 'value'),
     Input('year-dropdown', 'value'),
     Input('search-input', 'value'),
     Input('flow-dropdown', 'value')]
)
def update_choropleth(region, year, search, flow):
    """Generate choropleth map showing geographic distribution.

    UN Comtrade schema note: in both Export and Import rows,
    'Exporter' is always the REPORTING country.
    - Flow=Export → Exporter is the actual exporter → group by Exporter
    - Flow=Import → Exporter is the actual importer (the country buying) → group by Exporter
    Grouping by 'Exporter' in both cases correctly colours the countries
    that are doing the exporting (Export flow) or doing the importing (Import flow).
    """
    dff = filter_data(region, year, flow)
    hl = find_country(search)

    # Always group by the reporting country ('Exporter' column in both flow directions)
    group_col = 'Exporter'

    totals = dff.groupby(group_col)['Trade_Value_USD'].sum().reset_index()
    totals.columns = ['ISO', 'Value']
    totals['log_val'] = np.log10(totals['Value'].clip(lower=1))
    flow_label = 'Export value' if flow == 'Export' else 'Import value'
    totals['text'] = totals.apply(
        lambda r: f"{get_name(r['ISO'])} ({flow_label}): ${r['Value'] / 1e9:.1f}B",
        axis=1
    )

    fig = go.Figure(go.Choropleth(
        locations=totals['ISO'],
        z=totals['log_val'],
        text=totals['text'],
        hoverinfo='text',
        colorscale='YlOrRd',
        showscale=True,
        colorbar=dict(
            title=dict(text=f'{flow_label} (log10 USD)', font=dict(size=9, color=text2_color)),
            tickfont=dict(size=9, color=text2_color),
            thickness=8,
            len=0.4
        ),
        marker_line_width=0.3,
        marker_line_color='#181c26'
    ))

    if hl and hl in totals['ISO'].values:
        hl_row = totals[totals['ISO'] == hl].iloc[0]
        fig.add_trace(go.Choropleth(
            locations=[hl],
            z=[hl_row['log_val']],
            text=[hl_row['text']],
            hoverinfo='text',
            colorscale=[[0, accent_color], [1, accent_color]],
            showscale=False,
            marker_line_width=2.5,
            marker_line_color=accent_color,
        ))

    fig.update_geos(
        bgcolor='rgba(0,0,0,0)',
        landcolor='#12151c',
        oceancolor='#08090c',
        showocean=True,
        showlakes=False,
        showframe=False,
        coastlinecolor='#181c26',
        countrycolor='#181c26',
        projection_type='natural earth',
        projection_scale = 1.35

    )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        font=dict(color=text3_color, size=9),
        geo=dict(bgcolor='rgba(0,0,0,0)'),
        uirevision='choro-zoom'
    )

    return fig


@app.callback(
    Output('chord-iframe', 'src'),
    [Input('region-filter', 'value')]
)
def update_chord_iframe(region):
    """Update chord diagram region filter."""
    return f'/assets/chord_embed.html?region={region}'


@app.callback(
    [Output('insight-title', 'children'),
     Output('insight-body', 'children')],
    [Input('region-filter', 'value')]
)
def update_insight(region):
    """Update insight panel based on selected region."""
    data = insights.get(region, insights['All'])
    return data['title'], data['body']


if __name__ == '__main__':
    app.run(debug=True)