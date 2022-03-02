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
st.write("""
an app that helps users come up with new and interesting words for their writing projects.")
 DO NOT DEPEND ON THIS TOOL TO KEEP YOUR STORY. It can reset at any time.
 """)

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

    with st.expander("Select a Generator: choose which model that OpenAI will use to generate your content."):
        model = st.selectbox("Select a model", st.session_state.models)

    with st.expander("Optional prompt: generate a style baed on a specific sentence, phrase or idea."):
        prompt = st.text_input('Prompt to process', '', help="If you have a specific short prompt, place it here to process. It will append the results to the story.")

        # for the prompt, if the prompt is blank, disable the controls, but still render.
        d = (prompt == "")
        st.session_state.feat = st.selectbox('Select a style', st.session_state.features, disabled = d,
                                                     help="Requests data from GPT-3 in the selected style.")

        if (st.button('Generate tuned content', help="Calls OpenAI for fine tuned content based on the prompt.", disabled = d)):
            st.session_state.chapter += Writing.Writing().get_tuned_content(prompt, model)
        elif (st.button('Generate generic content', help="Calls OpenAI for Davinci content based no the prompt.", disabled = d)):
            st.session_state.chapter += Writing.Writing().get_generic_content(prompt)


    with st.expander("Inject random data"):
        st.info("Appends a random thing from the collection of options into the story area. THis can be used to spark ideas for yourself or the generator.")
        st.session_state.sel = st.selectbox('Select grouping of content', st.session_state.random_tables.keys(),
                                            help="Select a random table to generate content from.")

        # detemine button stuff before displaying or loading text boxes
        if st.button('Inject a thing', help="Add a random thing to the content from a list of items."):
            st.session_state.chapter += "\n" + Tables.Tables().get_random_thing()

    with st.expander("Content Generation Controls"):
        st.info("Use the content box to enhance chapter content. Note that this takes the whole chapter; we do not handle highlighting and custom selection yet.")
        #completions vs. tuning.
        # make a section with the buttons near it
        col1, col2 = st.columns(2)
        with col1:
            if (st.button('Run selected model content', help="Calls OpenAI for model (fine tuned) content.")):
                st.success("Sent to OpenAI: "+ st.session_state.chapter)
                st.session_state.chapter += Writing.Writing().completeModel(st.session_state.chapter, model)
        with col2:
            if (st.button('Run Davinci content', help="Calls OpenAI for classic DaVinci content.")):
                st.success("Sent to OpenAI: "+ st.session_state.chapter)
                st.session_state.chapter += Writing.Writing().completeDavinci(st.session_state.chapter)

    #not setting the text allow this to work correctly with a submit button.
    st.text_area(label="Your chapter",
                 help="The story that you are creating is here. You can add content to it by clicking the buttons above.",
                 height=500,
                 key="chapter",
                 on_change=update_content, args=(st.session_state.chapter, ))

#submit_button = st.form_submit_button(label='Submit')
