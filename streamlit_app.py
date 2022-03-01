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
prompt = st.text_input('Prompt to process', prompt)

writing = Writing.Writing()
d = Tables.Tables()
f = Features.Features()
st.session_state.sel = st.sidebar.selectbox('Select a table', st.session_state.random_tables.keys())
st.session_state.feat = st.sidebar.selectbox('Select a feature', st.session_state.features)
thing = st.sidebar.button('Get random thing', on_click=d.get_random_thing)
storydir = 'story'

st.session_state.chapter = st.text_area('edit this chapter', st.session_state.chapter)

# call openAI
if (st.session_state.api_key != "" and prompt != ""):
    c_prompt = "create a " + st.session_state.feat + " from the following sentence.\n" + prompt + "\n---\n\n"
    st.sidebar.button("execute query", on_click=writing.get_query(c_prompt))
    prompt = ''
