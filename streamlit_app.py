import streamlit as st
import openai

import Features
import Tables
import Writing


if 'random_tables' not in st.session_state:
    st.session_state.random_tables = {}
if 'features' not in st.session_state:
    st.session_state.features = {}
if 'sel' not in st.session_state:
    st.session_state.sel = ""
if 'feat' not in st.session_state:
    st.session_state.feat = ""
if 'chapter' not in st.session_state:
    st.session_state.chapter = "Example text goes here"
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'result' not in st.session_state:
    st.session_state.result = ""


st.session_state.api_key = st.text_input('enter your api key here', st.session_state.api_key)
prompt = st.text_input('Prompt to process', '')

st.session_state.features = Features.Features.features
st.session_state.random_tables = Tables.Tables().random_tables

st.session_state.sel = st.sidebar.selectbox('Select a table', st.session_state.random_tables.keys())

st.session_state.feat = st.sidebar.selectbox('Select a feature', st.session_state.features)

chapter = st.text_area('edit this chapter', st.session_state.chapter,  height=None)
if (chapter != st.session_state.chapter):
    st.session_state.chapter = chapter

if st.sidebar.button('Get random thing'):
    Tables.Tables().get_random_thing()

# call openAI
if (st.session_state.api_key != "" and prompt != ""):
    # st.sidebar.button("Get specific content", on_click=writing.get_query(prompt))
    if (st.sidebar.button('Get tuned content')):
        Writing.Writing().get_tuned_content(prompt)
    if (st.sidebar.button('Get generic content')):
        Writing.Writing().get_generic_content(prompt)

