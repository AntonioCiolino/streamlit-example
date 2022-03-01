import openai
import csv
import random
import streamlit as st
import Features

class Writing:

    features = Features.Features()

    def __init__(self):
        openai.api_key=st.session_state.api_key

    def write(self, dyn_prompt, model, temp=0.73, top_p=1.0, tokens=500, freq_pen=1.73, pres_pen=0.43, stop=["END", "Scene:", "[Scene"]):

        with st.spinner('Querying OpenAI...'):
            # fine-tuned models requires model parameter, whereas other models require engine parameter
            model_param = (
                {"model": model}
                if ":" in model
                   and model.split(":")[1].startswith("ft")
                else {"engine": model}
            )

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

    def get_tuned_content(self, prompt, model):
        try:
            p = self.features.get_prompt(st.session_state.feat)
            p = p.format(prompt)
            st.write(p)
            return self.write(p, model)
        except Exception as oops:
            st.error('ERROR in get_tuned function: ' + str(oops))

    def get_generic_content(self, prompt):
        try:
            p = self.features.get_prompt(st.session_state.feat)
            p = p.format(prompt)
            st.write( p)
            return self.write(p, "text-davinci-001")
        except Exception as oops:
            st.error('ERROR in get_generic function: ' + str(oops))

    def completeDavinci(self, prompt):
        try:
            return self.write(prompt, "text-davinci-001")
        except Exception as oops:
            st.error('ERROR in get_generic function: ' + str(oops))

    def completeModel(self, prompt, model):
        try:
            return self.write(prompt, model)
        except Exception as oops:
            st.error('ERROR in get_generic function: ' + str(oops))


    def getModels(self):
        models = []
        models.append("text-davinci-001")
        models.append("text-curie-001")
        try:
            finetunes = openai.FineTune.list()
            st.write(finetunes.data)
            for row in finetunes.data:
                st.write(row['status'])
                if (row['status'] == "succeeded" and row['result_files']['status'] != "deleted"):
                    models.append(row.fine_tuned_model)

            return models
        except Exception as oops:
            st.error('ERROR in getModels function: ' + str(oops))
