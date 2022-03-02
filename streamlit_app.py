import streamlit as st
from streamlit_quill import st_quill

import Features
import Tables
import Writing

# check to see if this is making a difference.
def update_content(args):
    pass


# Title of the page
st.title('WordPlay')
# st.header("Lorem Ipsum.")
st.write("an app that helps users come up with new and interesting words for their writing projects.")

if 'random_tables' not in st.session_state:
    st.session_state.random_tables = {}
if 'features' not in st.session_state:
    st.session_state.features = {}
if 'sel' not in st.session_state:
    st.session_state.sel = ""
if 'feat' not in st.session_state:
    st.session_state.feat = ""
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'result' not in st.session_state:
    st.session_state.result = ""
if 'models' not in st.session_state:
    st.session_state.models = []
if 'chapter' not in st.session_state:
    st.session_state.chapter = ""

with st.expander("Enter your API Key here"):
    st.session_state.api_key = st.text_input('API Key', st.session_state.api_key)

if (st.session_state.api_key == ""):
    st.write("You need to enter your API Key to use this tool.")
else:

    st.session_state.features = Features.Features.features
    st.session_state.random_tables = Tables.Tables().random_tables

    if (st.session_state.models == []):
        st.session_state.models = Writing.Writing().getModels()

    with st.expander("Create random data"):
        st.session_state.sel = st.selectbox('Create random table content', st.session_state.random_tables.keys(),
                                                    help="Select a random table to generate content from.")

        # detemine button stuff before displaying or loading text boxes
        if st.button('Get random thing', help="Add a random thing to the content from a list of items."):
            st.info("Added random thing")
            st.session_state.chapter += "\n" + Tables.Tables().get_random_thing()

    with st.expander("Select a Model"):
        model = st.selectbox("Select a model", st.session_state.models)

        prompt = st.text_input('Prompt to process', '', help="Enter a prompt to process. Used only for the features selection box.")

        # for the prompt, if the prompt is blank, disable the controls, but still render.
        d = (prompt == "")
        st.info("Use the select box to generate content. This will use the \"Prompt to process\" box.")
        st.session_state.feat = st.selectbox('Select a feature', st.session_state.features, disabled = d,
                                                     help="Requests data from GPT-3 in the selected style.")

        if (st.button('Generate tuned content', help="Calls OpenAI for fine tuned content based on the prompt.", disabled = d)):
            st.session_state.chapter += Writing.Writing().get_tuned_content(prompt, model)
        elif (st.button('Generate generic content', help="Calls OpenAI for Davinci content based no the prompt.", disabled = d)):
            st.session_state.chapter += Writing.Writing().get_generic_content(prompt)

    with st.expander("Content"):
        st.info("Use the content box to enhance chapter content. Note that this takes the whole chapter; we do not handle highlighting and custom selection yet.")
        #completions vs. tuning.
        # make a section with the buttons near it
        col1, col2 = st.columns(2)
        with col1:
            if (st.button('Run tuned content', help="Calls OpenAI for fine tuned content.")):
                st.success("Sent to OpenAI: "+ st.session_state.chapter)
                st.session_state.chapter += Writing.Writing().completeModel(st.session_state.chapter, model)
        with col2:
            if (st.button('Run generic content', help="Calls OpenAI for classic DaVinci content.")):
                st.success("Sent to OpenAI: "+ st.session_state.chapter)
                st.session_state.chapter += Writing.Writing().completeDavinci(st.session_state.chapter)

        #not setting the text allow this to work correctly with a submit button.
        st.text_area(label="edit your chapter",
                     help="This is the main body for writing.",
                     height=500,
                     key="chapter",
                     on_change=update_content, args=(st.session_state.chapter, ))

        st.info(st.session_state.chapter)


#submit_button = st.form_submit_button(label='Submit')
