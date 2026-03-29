import dash
from dash import html, dcc, Input, Output, State, ALL, ctx
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import json
from datetime import datetime
import csv
from pathlib import Path

# DATA LOADING
# Reads the cleaned CSV exported from the Jupyter Notebook
# Columns: Exporter, Importer, Trade_Value_USD, Year, Exporter_Region, Importer_Region, Flow
df = pd.read_csv('data/trade_data_cleaned.csv')

# STUDY MODE CONFIG
# True when user study is running, otherwise false
STUDY_MODE = False

# APP THEME
# All colors defined here so they stay consistent across the whole dashboard
background_color = '#08090c'
card_color       = '#0d0f14'
input_color      = '#12151c'
text1_color      = '#e8eaf0'
text2_color      = '#9499a8'
text3_color      = '#4a4f5e'
accent_color     = '#3b82f6'
success_color    = '#10b981'
warning_color    = '#f59e0b'
danger_color     = '#ef4444'

# REGION COLORS
# Matches notebook region_colors — used across all 3 charts for consistency
regions_colors = {
    'Americas':      '#ef4444',
    'Europe / CIS':  '#3b82f6',
    'Middle East':   '#f59e0b',
    'Asia / Pacific':'#10b981',
    'Africa':        '#a855f7',
}

# COUNTRY NAME SEARCH
# Converts ISO3 codes to full country names for chart labels
country_names = {
    'CAN':'Canada','USA':'United States','MEX':'Mexico','COL':'Colombia',
    'BRA':'Brazil','ARG':'Argentina','TTO':'Trinidad & Tobago','CHL':'Chile',
    'VEN':'Venezuela','ECU':'Ecuador','PER':'Peru','BOL':'Bolivia',
    'RUS':'Russia','NOR':'Norway','GBR':'United Kingdom','NLD':'Netherlands',
    'DEU':'Germany','POL':'Poland','FIN':'Finland','BLR':'Belarus',
    'CZE':'Czechia','HUN':'Hungary','SVK':'Slovakia','AUT':'Austria',
    'FRA':'France','ITA':'Italy','BEL':'Belgium','ESP':'Spain',
    'SWE':'Sweden','DNK':'Denmark','UKR':'Ukraine','GRC':'Greece',
    'PRT':'Portugal','ROU':'Romania','BGR':'Bulgaria','HRV':'Croatia',
    'IRL':'Ireland','CHE':'Switzerland','SRB':'Serbia','SVN':'Slovenia',
    'LTU':'Lithuania','LVA':'Latvia','EST':'Estonia',
    'SAU':'Saudi Arabia','IRQ':'Iraq','IRN':'Iran','QAT':'Qatar',
    'KWT':'Kuwait','OMN':'Oman','ARE':'UAE','BHR':'Bahrain',
    'CHN':'China','JPN':'Japan','KOR':'South Korea','IND':'India',
    'AUS':'Australia','TUR':'Turkey','IDN':'Indonesia','THA':'Thailand',
    'SGP':'Singapore','MYS':'Malaysia','VNM':'Vietnam','PAK':'Pakistan',
    'PHL':'Philippines','BGD':'Bangladesh','TWN':'Taiwan','BRN':'Brunei',
    'NZL':'New Zealand','KAZ':'Kazakhstan','MNG':'Mongolia',
    'NGA':'Nigeria','ZAF':'South Africa','EGY':'Egypt','DZA':'Algeria',
    'AGO':'Angola','LBY':'Libya','MAR':'Morocco','GHA':'Ghana',
    'TZA':'Tanzania','KEN':'Kenya','CMR':'Cameroon','GAB':'Gabon',
    'COG':'Congo','GNQ':'Eq. Guinea','TCD':'Chad','SDN':'Sudan',
    'AZE':'Azerbaijan','MOZ':'Mozambique',
}

# STORY TELLING
# Dynamic text shown in the insight panel based on selected region
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