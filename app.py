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