import streamlit as st
import os
import sounddevice as sd
import numpy as np
import streamlit as st
from pydub import AudioSegment
import time


def list_directories(directory):
    directories = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            directories.append(item)
    return directories

def list_files(directory):
    files = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            files.append(filename)
    return files

def download_file(file_path):
    with open(file_path, "rb") as file:
        file_data = file.read()
    st.download_button("Download", file_data, file_path)

def upload_file(directory):
    uploaded_file = st.file_uploader("Upload File")
    if uploaded_file is not None:
        file_path = os.path.join(directory, uploaded_file.name)
        with open(file_path, "wb") as file:
            file.write(uploaded_file.getbuffer())

def audio_explorer():
    st.title("Audio Library")
    home_directory = os.getcwd()
    current_directory = home_directory + "/Audio_Library"

    selected_directory = st.selectbox("Select Directory", list_directories(current_directory))
    selected_directory_path = os.path.join(current_directory, selected_directory) if selected_directory else current_directory

    files = list_files(selected_directory_path)

    if files:
        selected_file = st.selectbox("Select File", files)
        selected_file_path = os.path.join(selected_directory_path, selected_file)

        audio = AudioSegment.from_file(selected_file_path)
        audio_data = np.array(audio.get_array_of_samples())
        sample_rate = audio.frame_rate

        space, left, center, right = st.columns([1, 2, 2, 2])
        with space:
            st.write()
        with left:
            play_button = st.button("Play Audio")

        with center:
            stop_button = st.button("Stop Audio")
            
        with right:
            download_file(selected_file_path)

        def play_audio(data, rate):
            sd.play(data, rate, blocking=False)

        if play_button:
            play_audio(audio_data, sample_rate)

        elif stop_button:
            sd.stop()

        progress = st.progress(0)
        current_time = st.empty()

        if play_button or stop_button:
            duration = len(audio) / 1000  # Convert duration to seconds
            start_time = st.session_state.get("start_time", None)

            if start_time is None:
                start_time = st.session_state["start_time"] = time.time()

            while time.time() - start_time < duration:
                if stop_button:
                    break

                progress.progress((time.time() - start_time) / duration)
                current_time.text("{:.2f} s / {:.2f} s".format(time.time() - start_time, duration))
                time.sleep(0.1)

            progress.empty()
            current_time.empty()

        # st.write("Transcripts:")
        # transcript_files = list_files(home_directory + "/Transcript_Library")
        # for transcript_file in transcript_files:
        #     st.write(transcript_file)

    upload_file(selected_directory_path)




def transcripts_explorer():
    st.title("Transcripts Library")
    home_directory = os.getcwd()
    current_directory = home_directory + "/Transcript_Library"

    selected_directory = st.selectbox("Select Directory", list_directories(current_directory))
    selected_directory_path = os.path.join(current_directory, selected_directory) if selected_directory else current_directory

    files = list_files(selected_directory_path)

    if files:
        selected_file = st.selectbox("Select File", files)
        selected_file_path = os.path.join(selected_directory_path, selected_file)

        with open(selected_file_path, "r") as file:
            transcript_content = file.read()
            st.text_area("Transcript Content", transcript_content)

        left, center, right = st.columns([1, 1, 3])
        with right:
            download_file(selected_file_path)

    upload_file(selected_directory_path)