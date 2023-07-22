import streamlit as st
from gtts import gTTS
import pdfplumber
import docx
import ebooklib
from ebooklib import epub

st.title("Streamlit AudioBook App")
st.info('Convert your E-book to audiobook')

book = st.file_uploader('Please upload your file', type=['pdf', 'txt', 'docx', 'epub'])

def extract_text_from_docx(file):
    doc = docx.Document(file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def extract_text_from_epub(file):
    book = epub.read_epub(file)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())
    return '\n'.join(chapters)

if book:
    if book.type == 'application/pdf':
        all_text = ""
        with pdfplumber.open(book) as pdf:
            for text in pdf.pages:
                single_page_text = text.extract_text()
                all_text = all_text + '\n' + str(single_page_text)
    elif book.type == 'text/plain':
        all_text = book.read().decode("utf-8")
    elif book.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        all_text = extract_text_from_docx(book)
    elif book.type == 'application/epub+zip':
        all_text = extract_text_from_epub(book)

    tts = gTTS(all_text)
    tts.save('audiobook.mp3')

    audio_file = open('audiobook.mp3','rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/wav', start_time=0)

