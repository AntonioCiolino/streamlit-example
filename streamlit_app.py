import streamlit as st
import csv
import random
import openai

model = "curie:ft-vtcnp-2022-02-23-00-34-41"
api_key = "enter your key here"

if 'random_tables' not in st.session_state:
    st.session_state.random_tables = {}
if 'sel' not in st.session_state:
    st.session_state.sel = ""
if 'chapter' not in st.session_state:
    st.session_state.chapter = "Example text goes here"
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'result' not in st.session_state:
    st.session_state.result = ""

class Tables:
    def __init__(self, **kwargs):
        pass

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
            st.session_state.chapter += random.choice(st.session_state.random_tables[st.session_state.sel])
        except Exception as oops:
            st.write('ERROR in get_random_thing function:', oops)

class OAI:
    def completion(prompt, model, temp=0.73, top_p=1.0, tokens=500, freq_pen=1.73, pres_pen=0.43, stop=["END", "Scene:", "[Scene"]):
        try:
            # fine-tuned models requires model parameter, whereas other models require engine parameter
            model_param = (
                {"model": model}
                if ":" in model
                   and model.split(":")[1].startswith("ft")
                else {"engine": model}
            )

            response = openai.Completion.create(
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop,
                **model_param)
            response = response['choices'][0]['text']
            return response
        except Exception as oops:
            return st.write(str(oops))

    def get_query(self):
        try:
            st.session_state.result = OAI.completion(st.session_state.chapter, model, temp=0.73, top_p=1.0, tokens=500, freq_pen=1.73, pres_pen=0.43, stop=["END", "Scene:", "[Scene"])
            st.session_state.chapter = st.session_state.result
        except Exception as oops:
            st.write('ERROR in get_query function:', oops)



d = Tables()
d.load_tables()
st.session_state.sel = st.sidebar.selectbox('Select a table', st.session_state.random_tables.keys())
thing = st.sidebar.button('Get random thing', on_click=d.get_random_thing)
storydir = 'story'

st.write(st.session_state.chapter)
st.session_state.chapter = st.text_input('edit this content', st.session_state.chapter)
st.session_state.api_key = st.text_input('enter your api key here', st.session_state.api_key)

# call openAI
if (st.session_state.api_key != ""):
    openai.api_key=st.session_state.api_key
    prompt = "create a " + "metaphor" + " from the following sentence.\n" + "i was very hungry" + "\n---\n\n"
    st.sidebar.button("execute query", on_click=lambda: OAI.get_query)
