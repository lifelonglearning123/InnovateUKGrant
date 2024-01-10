import streamlit as st
import os
import openai
from dotenv import load_dotenv
#How to upload information about how the grant is judged
#Drop down menu for the main questions.

load_dotenv()  # Load environment variables from .env file

openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("InnovateUK Grant Writer")
main_question = st.text_input("What is the main question?")
project_title = st.text_area("What is the project?")

# Initialize the session state for questions and answers. question_answer_paris list is created within the session_state dictionary
if 'question_answer_pairs' not in st.session_state:
    st.session_state.question_answer_pairs = []

# Function to add a new question and answer box
def add_question_and_answer():
    st.session_state.question_answer_pairs.append({'question': '', 'answer': ''})

# Display question and answer boxes
for i in range(len(st.session_state.question_answer_pairs)):
    question_key = f"question_{i}"
    answer_key = f"answer_{i}"
    st.session_state.question_answer_pairs[i]['question'] = st.text_input("Enter sub question:", key=question_key, value=st.session_state.question_answer_pairs[i]['question'])
    st.session_state.question_answer_pairs[i]['answer'] = st.text_area("Write bullet points to answer the question:", key=answer_key, value=st.session_state.question_answer_pairs[i]['answer'])

# Button to add more questions and answers
st.button("Add additional Sub Question and Answer", on_click=add_question_and_answer)

if st.button("Generate Response"):
    messages = [
        {"role": "system", "content": "You are the best innovation grant writer. You must write the best innovation grant for the following questions and answers based on the user inputs"},
        {"role": "user", "content": f"The main question is: {main_question}"},
        {"role": "user", "content": f"The project is: {project_title}"}
    ]

    # Add each question and answer pair to the messages
    for pair in st.session_state.question_answer_pairs:
        if pair['question'] and pair['answer']:
            messages.append({"role": "user", "content": f"Question: {pair['question']}"})
            messages.append({"role": "user", "content": f"Answer: {pair['answer']}"})

    # Send the messages to OpenAI's API
    response = openai.chat.completions.create(
        model="gpt-4 turbo",
        messages=messages
    )

    # Display the response from OpenAI
    st.write(response.choices[0].message.content)
