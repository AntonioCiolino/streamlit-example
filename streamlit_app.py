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
table_selected = ""

def __init__(self, **kwargs):
    random_tables = self.load_random_tables()
    st.write(random_tables)

    self.table_selected = st.selectbox('Select a table', random_tables.keys(), on_change=self.get_random_thing())
    self.storydir = 'story'


def load_random_tables(self):
    tables = {}
    with open('tables1e.csv') as data_file:
        data = csv.reader(data_file, delimiter='\t')
        for row in data:
            if (row[0] == 'd100'):
                current_table = row[1]
                tables[current_table] = []
            else:
                tables[current_table].append(row[1])
    return tables

def get_random_thing(self, button):
    self.info = 'Getting random thing...'
    all_tables = self.load_random_tables()
    try:
        result = random.choice(all_tables[button.text])
        st.write(result)
    except Exception as oops:
        print('ERROR in get_random_thing function:', oops)
        st.logging.fatal('ERROR in get_random_thing function: %s', oops)
