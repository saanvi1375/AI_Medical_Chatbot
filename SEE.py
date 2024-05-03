import streamlit as st
import requests
import re

# API endpoint and authorization token
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
headers = {"Authorization": "Bearer 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"}

# Function to send query to the AI model
def query_model(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Function to process medical queries and generate bullet points
def process_medical_query(input_text, max_tokens):
    # Send query to the model
    output = query_model({
        "inputs": input_text,
        "max_tokens": max_tokens
    })

    bullet_points = []

    # Process model output
    if isinstance(output, list):
        for idx, item in enumerate(output):
            generated_text = item["generated_text"]
            points = get_bullet_points(generated_text, idx == 0)
            bullet_points.extend(points)
    elif isinstance(output, dict) and "generated_text" in output:
        generated_text = output["generated_text"]
        points = get_bullet_points(generated_text, True)
        bullet_points.extend(points)
    else:
        bullet_points.append("Error: Unexpected response format")

    return "\n".join("- " + point for point in bullet_points)

# Function to extract bullet points from generated text
def get_bullet_points(generated_text, skip_first=False):
    points = generated_text.split('\n')[1 if skip_first else 0:6]  # Extract bullet points
    return [end_sentence(point) for point in points]  # Post-process each bullet point

# Function to ensure bullet points end at a sentence boundary
def end_sentence(text):
    match = re.search(r'(?<=[.!?])\s+', text[::-1])  # Match last sentence boundary
    if match:
        end_index = len(text) - match.start()
        return text[:end_index]
    else:
        return text

# Main function to create Streamlit app
def main():
    # App title and description
    st.title("AI Doctor 🩺🫀")
    st.markdown(
        """
        <div style='background-color:#f0f0f0;padding:2px;border-radius:10px;text-align:left;'>
        <h5 style='text-align:center;color:#3366ff;'>Your One-Stop Solution for Healthcare</h5>
        </div>
        <br><br>
        """,
        unsafe_allow_html=True
    )

    # User input textarea
    user_input = st.text_area("Enter your medical query here:")
    max_tokens = st.session_state.get("max_tokens", 200)

    # Button to get initial advice
    if st.button("Get Advice"):
        if user_input.strip() != "":
            st.session_state["user_input"] = user_input
            model_output = process_medical_query(user_input, max_tokens)
            st.write(model_output)
        else:
            st.warning("Please enter a valid medical query.")

    # Button to get more detailed advice
    continue_button = st.button("Continue")
    if continue_button:
        if "user_input" in st.session_state:
            user_input = st.session_state["user_input"]
            max_tokens *= 3  # Increase max_tokens for a more detailed response
            detailed_output = process_medical_query(user_input, max_tokens)
            st.write(detailed_output)

    # Disclaimer
    st.markdown(
        """
        <marquee>
        <div style='position:fixed; bottom:0; width:50%; background-color:#f0f0f0;padding:2px;text-align:center;'>
        <p style='font-size:18px;color:#555;'>This is an AI generated output. It is always better to consider a doctor's opinion!</p>
        </div>
        </marquee>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
