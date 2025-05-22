import streamlit as st
import plotly.graph_objects as go
import gpxpy
import pandas as pd
import numpy as np
from scipy.signal import savgol_filter
from streamlit_extras.app_logo import add_logo