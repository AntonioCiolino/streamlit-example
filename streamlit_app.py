from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import csv
import random

# st.logging.basicConfig(filename='kivyUI.log', level=st.logging.INFO, filemode="w")
# st.logging.debug('Debugging started.')

model = "curie:ft-vtcnp-2022-02-23-00-34-41"
if 'random_tables' not in st.session_state:
    st.session_state.random_tables = {}
if 'sel' not in st.session_state:
    st.session_state.sel = ""
if 'chapter' not in st.session_state:
    st.session_state.chapter = "Example text goes here"

class Tables:
    def __init__(self, **kwargs):
        pass

    @st.cache(show_spinner=False)
    def load_tables(self):
        tables = {}
        with open('tables1e.csv') as data_file:
            data = csv.reader(data_file, delimiter='\t')
            for row in data:
                if (row[0] == 'd100'):
                    current_table = row[1]
                    tables[current_table] = []
                else:
                    tables[current_table].append(row[1])
        st.session_state.random_tables = tables

    def get_random_thing(self):
        try:
            st.text_area +=  random.choice(st.session_state.random_tables[st.session_state.sel])
        except Exception as oops:
            st.write('ERROR in get_random_thing function:', oops)



d = Tables()
d.load_tables()

st.session_state.sel = st.sidebar.selectbox('Select a table', st.session_state.random_tables.keys())
thing = st.sidebar.button('Get random thing', on_click=d.get_random_thing)
storydir = 'story'


st.text_area ('editor', st.session_state.chapter)
