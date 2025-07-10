import streamlit as st
import requests
import json

st.title("Code Review Assistant")

code = st.text_area("Paste Python code:")

if st.button("Review Code"):
    ollama_url = "http://host.docker.internal:11434/api/generate"

    payload = {
        "model": "mistral",
        "prompt": f"""
    You are an expert Python code reviewer.

    Please review the following Python code. Analyze it for:
    - correctness
    - readability
    - potential bugs
    - performance improvements
    - adherence to Python best practices

    Respond in clear, professional language. Your response should include:
    - a brief summary paragraph of your overall impressions
    - a bullet list of any specific improvements or concerns
    - if there are no issues, simply say 'No issues found.'

    Here is the code to review:

    {code}
    """
    }


    resp = requests.post(ollama_url, json=payload, stream=True)

    result = ""

    tokens = []
    for chunk in resp.iter_lines():
        if chunk:
            data_json = json.loads(chunk.decode("utf-8"))
            token = data_json.get("response", "")
            tokens.append(token)

 
    result = "".join(tokens)
    result = " ".join(result.split())

    st.markdown(result)
