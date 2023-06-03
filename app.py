import streamlit as st
from streamlit_option_menu import option_menu
from jinja2 import Environment, FileSystemLoader
import numpy as np
import pandas as pd
import os
import dir as files 


with st.sidebar:
    selected = option_menu(
        menu_title="Audio transcription",
        menu_icon="cassette-fill",
        options=["Transcribe File", "Audio Archive", "Transcripts Files", "Download Youtube"],
        icons=["music-note-list", "archive-fill", "credit-card-2-front-fill", "play-btn-fill"],
        default_index=0
    )

if selected == "Transcribe File":
    # st.write("Transcribe content goes here")
    files.transcribe_file()

elif selected == "Audio Archive":
    files.audio_explorer()

elif selected == "Transcripts Files":
    files.transcripts_explorer()
    
elif selected == "Download Youtube":
    files.download_youtube()