import csv
import random
import streamlit as st

class Features:
    def __init__(self, **kwargs):
        features = []
        with open('features.csv') as data_file:
            data = csv.reader(data_file, delimiter='\t')
            for row in data:
                features.append(row[0])

        st.session_state.features = features
