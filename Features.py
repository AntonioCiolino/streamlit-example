import csv
import random
import streamlit as st

class Features:
    prompts = []
    features = []
    def __init__(self, **kwargs):

        with open('features.csv') as data_file:
            data = csv.reader(data_file, delimiter=',')
            for row in data:
                self.features.append(str(row[0]))
                self.prompts.append(str(row[1]))

        st.session_state.features = self.features

    def get_prompt(self, item):
        try:
            return self.prompts[item]
        except Exception as oops:
            st.write('ERROR in get_prompt function:', oops)
