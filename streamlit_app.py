import streamlit as st
from streamlit_quill import st_quill

import Features
import Tables
import Writing

# Title of the page
st.title('OpenAI Geezify')
# st.header("Lorem Ipsum.")
st.write("Use this tool to call OpenAI and enhance existing writing, or add additional flair to whatever content you have.")

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
if 'models' not in st.session_state:
    st.session_state.models = []


with st.expander("Enter your API Key here"):
    st.session_state.api_key = st.text_input('API Key', st.session_state.api_key)

if (st.session_state.api_key == ""):
    st.write("You need to enter your API Key to use this tool.")
else:
    if (st.session_state.models == []):
        st.session_state.models = Writing.Writing().getModels()
    model = st.selectbox("Select a model", st.session_state.models)

    prompt = st.text_input('Prompt to process', '', help="Enter a prompt to process. Used only for the features selection box.")

    st.session_state.features = Features.Features.features
    st.session_state.random_tables = Tables.Tables().random_tables

    st.session_state.sel = st.sidebar.selectbox('Create random table content', st.session_state.random_tables.keys(),
                                                help="Select a random table to pull content from.")

    # detemine button stuff before displaying or loading text boxes
    if st.sidebar.button('Get random thing', help="Add a random thing to the content from a list of items."):
        st.info("Added random thing", )
        st.session_state.chapter += "\n" + Tables.Tables().get_random_thing()

    # for the prompt, if the prompt is blank, disable the controls, but still render.
    d = (prompt == "")
    st.sidebar.info("Use the select box to generate content. This will use the \"Prompt to process\" box.")
    st.session_state.feat = st.sidebar.selectbox('Select a feature', st.session_state.features, disabled = d,
                                                 help="Requests data from GPT-3 in the selected style.")

    if (st.sidebar.button('Generate tuned content', help="Calls OpenAI for fine tuned content based on the prompt.", disabled = d)):
        st.session_state.chapter += Writing.Writing().get_tuned_content(prompt, model)
    if (st.sidebar.button('Generate generic content', help="Calls OpenAI for Davinci content based no the prompt.", disabled = d)):
        st.session_state.chapter += Writing.Writing().get_generic_content(prompt)

    chapter = ""

    st.sidebar.info("Use the content box to enhance chapter content. Note that this takes the whole chapter; we do not handle highlighting and custom selection yet.")
    #completions vs. tuning.
    if (st.sidebar.button('Run tuned content', help="Calls OpenAI for fine tuned content.")):
        st.write("Starting with content: " + st.session_state.chapter)
        chapter += Writing.Writing().completeModel(st.session_state.chapter, model)
        st.write("Finished with content: " + chapter)
    if (st.sidebar.button('Run generic content', help="Calls OpenAI for classic DaVinci content.")):
        st.session_state.chapter += Writing.Writing().completeDavinci(st.session_state.chapter)


    if (st_quill):
        chapter = st_quill(value=st.session_state.chapter)
        if (chapter != st.session_state.chapter):
            st.success("Updated Content")
            st.session_state.chapter = chapter
