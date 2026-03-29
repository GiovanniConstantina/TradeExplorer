import dash
from dash import html, dcc, Input, Output, State, ALL, ctx
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import json
from datetime import datetime
import csv
from pathlib import Path

df = pd.read_csv('data/trade_data_cleaned.csv')