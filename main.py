import streamlit as st
from langchain import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os 

template = """
    Below is an email that may be poorly worded.
    Your goal is to:
    - Properly format the email
    - Convert the input text to a specified tone
    - Convert the input text to a specified dialect

    Here are some examples different Tones:
    - Formal: We went to Barcelona for the weekend. We have a lot of things to tell you.
    - Informal: Went to Barcelona for the weekend. Lots to tell you.  

    Here are some examples of words in different dialects:
    - American: French Fries, cotton candy, apartment, garbage, cookie, green thumb, parking lot, pants, windshield
    - British: chips, candyfloss, flag, rubbish, biscuit, green fingers, car park, trousers, windscreen

    Example Sentences from each dialect:
    - American: I headed straight for the produce section to grab some fresh vegetables, like bell peppers and zucchini. After that, I made my way to the meat department to pick up some chicken breasts.
    - British: Well, I popped down to the local shop just the other day to pick up a few bits and bobs. As I was perusing the aisles, I noticed that they were fresh out of biscuits, which was a bit of a disappointment, as I do love a good cuppa with a biscuit or two.

    Please start the email with a warm introduction. Add the introduction if you need to.

    Below is the email, tone, and dialect:
    TONE: {tone}
    DIALECT: {dialect}
    EMAIL: {email}

    YOUR {dialect} RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=["tone", "dialect", "email"],
    template=template,
)


def load_LLM():
    cached_llm = ChatGoogleGenerativeAI(google_api_key=os.getenv('GOOGLE_API_KEY'), model="gemini-pro",
                                    convert_system_message_to_human=True)
    return cached_llm


st.set_page_config(page_title="Globalize Email", page_icon=":robot:")
st.header("Globalize Text")

col1, col2 = st.columns(2)


st.markdown(
        "Often Professionals would like to improve their emails, "
        "but don't have the skills to do so.\n\n This Tool will help you improve your email skills by converting your emails "
        "into a more professional format.This tool is powered by [Langchain](www.langchain.com) and "
        "made by [Nitin Sharma](https://www.linkedin.com/in/nitin1608/)")


st.markdown("## Enter Your Email To Convert")

col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        'Which tone would you like your email to have?',
        ('Formal', 'Informal'))

with col2:
    option_dialect = st.selectbox(
        'Which English Dialect would you like?',
        ('American', 'British'))


def get_text():
    input_text = st.text_area(label="Email Input", label_visibility='collapsed', placeholder="Your Email...",
                              key="email_input")
    return input_text


email_input = get_text()

if len(email_input.split(" ")) > 700:
    st.write("Please enter a shorter email. The maximum length is 700 words.")
    st.stop()


def update_text_with_example():
    print("in updated")
    st.session_state.email_input = "Sally I am starts work at yours monday from dave"

co1, co2 = st.columns(2)
with co1:
   submit= st.button("Submit", help="Generate Email.")

with co2:
    st.button("*See An Example*", type='secondary', help="Click to see an example of the email you will be converting.",
              on_click=update_text_with_example)




st.markdown("### Your Converted Email:")
if(submit):
    if email_input:
        llm = load_LLM()
        prompt_with_email = prompt.format(tone=option_tone, dialect=option_dialect, email=email_input)
        formatted_email = llm.invoke(prompt_with_email)
        st.write(formatted_email.content)