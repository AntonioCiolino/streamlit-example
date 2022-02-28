import openai
import csv
import random
import streamlit as st

class Writing:
    def __init__(self):
        openai.api_key=st.session_state.api_key

    def completion(prompt, model, temp=0.73, top_p=1.0, tokens=500, freq_pen=1.73, pres_pen=0.43, stop=["END", "Scene:", "[Scene"]):
        try:
            # fine-tuned models requires model parameter, whereas other models require engine parameter
            model_param = (
                {"model": model}
                if ":" in model
                   and model.split(":")[1].startswith("ft")
                else {"engine": model}
            )

            st.write("*** sent " + prompt)
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

    def get_query(self, prompt):

        model = "curie:ft-vtcnp-2022-02-23-00-34-41"

        try:
            result = openai.Completion.create(prompt, model, temp=0.73, top_p=1.0, tokens=100, freq_pen=1.73, pres_pen=0.43, stop=["END", "Scene:", "[Scene"])
            st.session_state.chapter += result
            st.write(st.session_state.chapter)  # this is the text that is displayed on the page
        except Exception as oops:
            st.write('ERROR in get_query function:', oops)
