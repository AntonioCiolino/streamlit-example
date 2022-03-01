import streamlit as st
import openai

import Features
import Tables
import Writing

# Title of the page
st.title('Writing tool')
st.header("Lorem Ipsum.")
st.subheader("Lorem Ipsum su dolor emet.")

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

st.session_state.api_key = st.sidebar.text_input('enter your api key here', st.session_state.api_key)
prompt = st.text_input('Prompt to process', '')

st.session_state.features = Features.Features.features
st.session_state.random_tables = Tables.Tables().random_tables

st.session_state.sel = st.sidebar.selectbox('Select a table', st.session_state.random_tables.keys())

# detemine button stuff before displaying or loading text boxes
if st.sidebar.button('Get random thing'):
    st.info("Getting random thing")
    st.session_state.chapter += " " + Tables.Tables().get_random_thing()

st.session_state.feat = st.sidebar.selectbox('Select a feature', st.session_state.features)

# call openAI
if (st.session_state.api_key != "" and prompt != ""):
    st.sidebar.info("Use GPT-3 to Generate content")
    if (st.sidebar.button('Generate tuned content')):
        st.session_state.chapter += Writing.Writing().get_tuned_content(prompt)
    if (st.sidebar.button('Generate generic content')):
        st.session_state.chapter += Writing.Writing().get_generic_content(prompt)

    st.sidebar.info("Use GPT-3 to Complete content")

    #completions vs. tuning.
    if (st.sidebar.button('Run tuned content')):
        st.session_state.chapter += prompt + " " + Writing.Writing().completeModel(prompt)
    if (st.sidebar.button('Run generic content')):
        st.session_state.chapter += prompt + " " + Writing.Writing().completeDavinci(prompt)


chapter = st.text_area('edit this chapter', st.session_state.chapter,  height=500)
if (chapter != st.session_state.chapter):
    st.success("Updating chapter")
    st.session_state.chapter = chapter
