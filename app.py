import streamlit as st
from gtts import gTTS
import pdfplumber



st.title("AudioBook App")
st.info('Convert your E-book to audiobook')

book = st.file_uploader('Please upload your PDF file', type='PDF')

all_text = ''
if book:
    with pdfplumber.open(book) as pdf:
        for text in pdf.pages:
            single_page_text = text.extract_text()
            all_text += '\n' + str(single_page_text)



            gtts = gTTS(all_text)
            gtts.save('audiobook.mp3')



    audio_file = open('audiobook.mp3', 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/wav', start_time=0)



def show_file():
    """
    displays pdf gnerated and downloads it when prompted
    """
    # to display the pdf
    with open(book, 'rb') as f:
        base64_pdf = b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)




