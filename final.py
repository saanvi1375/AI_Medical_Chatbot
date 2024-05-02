import streamlit as st
import requests

API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def medical_query(input_text, max_tokens):
    output = query({
        "inputs": input_text,
        "max_tokens": max_tokens
    })
    
    if isinstance(output, list):
        generated_texts = [item["generated_text"] for item in output]
        return "\n".join(generated_texts)
    elif isinstance(output, dict) and "generated_text" in output:
        return output["generated_text"]
    else:
        return "Error: Unexpected response format"

def main():
    st.title("Personalized AI Doctor 🩺🫀")
    st.markdown(
        """
        <div style='background-color:#f0f0f0;padding:20px;border-radius:10px;'>
        <h5 style='text-align:center;color:#3366ff;'>Your One-Stop Solution for Healthcare</h5>
        </div>
        """,
        unsafe_allow_html=True
    )

    user_input = st.text_area("Enter your medical query here:")
    max_tokens = st.session_state.get("max_tokens", 200)

    if st.button("Get Advice"):
        if user_input.strip() != "":
            st.session_state["user_input"] = user_input
            model_output = medical_query(user_input, max_tokens)
            st.write(model_output)
        else:
            st.warning("Please enter a valid medical query.")

    continue_button = st.button("Continue")
    if continue_button:
        if "user_input" in st.session_state:
            user_input = st.session_state["user_input"]
            max_tokens *= 2  # Increase max_tokens for a more detailed response
            detailed_output = medical_query(user_input, max_tokens)
            st.write(detailed_output)

    # Disclaimer
    st.markdown(
        """
        <div style='position:fixed; bottom:0; width:100%; background-color:#f0f0f0;padding:10px;text-align:center;'>
        <p style='font-size:12px;color:#555;'>This is an AI generated output. It is always better to consider a doctor's opinion!</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
