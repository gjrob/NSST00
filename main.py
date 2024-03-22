import speech_recognition as sr
from transformers import pipeline
import streamlit as st

#Speech Recognition

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio_data = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return "Could not request results; {0}".format(e)


#Translation Using Hugging Face Transformers

def translate_text_to_spanish(text):
    translator = pipeline("translation_en_to_es", model="Helsinki-NLP/opus-mt-en-es")
    translated_text = translator(text, max_length=40)[0]['translation_text']
    return translated_text



#Integrate everything into a Streamlit app. Users can choose to type or speak English, and the app will display the translation in Spanish

st.title('Talk and Translate: Nigg@$ Speak Spanish Too')

# User choice: Type or Speak
user_choice = st.radio("Input method:", ('Type', 'Speak'))

if user_choice == 'Type':
    user_input = st.text_input("Type here:")
    if st.button('Translate'):
        translated_text = translate_text_to_spanish(user_input)
        st.text_area("Translation:", value=translated_text, height=100)
elif user_choice == 'Speak':
    if st.button('Start Speaking'):
        with st.spinner("Listening..."):
            recognized_text = recognize_speech_from_mic()
            st.text_area("Recognized:", value=recognized_text, height=100)
            translated_text = translate_text_to_spanish(recognized_text)
            st.text_area("Translation:", value=translated_text, height=100)


            