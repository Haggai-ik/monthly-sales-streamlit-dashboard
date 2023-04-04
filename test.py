import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objs 
import pickle
from pathlib import Path
import streamlit_authenticator as str
import yaml
from yaml.loader import SafeLoader

file_path= Path(__file__).parent / "hashed.pkl"

with file_path.open("rb") as file:
  hashed_passwords=pickle.load(file)




print(hashed_passwords)