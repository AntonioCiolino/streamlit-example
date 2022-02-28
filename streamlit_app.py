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

class Demo:
    random_tables = {}
    selected_table = None
    def __init__(self, **kwargs):
        self.random_tables = self.load_random_tables()


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

    def get_random_thing(self):
        random_tables = self.load_random_tables()
        st.write(self.selected_table)
        self.info = 'Getting random thing...'

        st.write("Getting from " + self.selected_table)
        try:
            result = random.choice(random_tables[self.selected_table])
            st.write(result)
        except Exception as oops:
            st.write('ERROR in get_random_thing function:', oops)



d = Demo()
d.load_random_tables()
st.write(d.random_tables)
selected_table = st.sidebar.selectbox('Select a table', d.random_tables.keys(), on_change=d.get_random_thing)
storydir = 'story'
