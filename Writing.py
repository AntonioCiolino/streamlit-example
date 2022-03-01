import openai
import csv
import random
import streamlit as st
import Features

class Writing:
    model = "curie:ft-vtcnp-2022-02-23-00-34-41"
    features = Features.Features()

    def __init__(self):
        openai.api_key=st.session_state.api_key

    def write(self, dyn_prompt, model, temp=0.73, top_p=1.0, tokens=500, freq_pen=1.73, pres_pen=0.43, stop=["END", "Scene:", "[Scene"]):

        # fine-tuned models requires model parameter, whereas other models require engine parameter
        model_param = (
            {"model": model}
            if ":" in model
               and model.split(":")[1].startswith("ft")
            else {"engine": model}
        )
        st.info("prompt: {} model: {}",  dyn_prompt, model_param)
        try:
            response = openai.Completion.create(
                prompt=dyn_prompt,
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
            return "Completion Error: " + str(oops)

    def get_tuned_content(self, prompt):
        try:
            p = self.features.get_prompt(st.session_state.feat)
            p = "".format(p, prompt)
            st.write(p)
            return self.write(p, self.model)
        except Exception as oops:
            st.error('ERROR in get_query function:{}', str(oops))

    def get_generic_content(self, prompt):
        try:
            p = self.features.get_prompt(st.session_state.feat)
            p = "".format(p, prompt)
            st.write( p)
            return self.write(p, "text-davinci-001")
        except Exception as oops:
            st.error('ERROR in get_query function:', str(oops))


