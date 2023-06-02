import streamlit as st
import os
import time
import numpy as np
import sounddevice as sd
import speech_recognition as sr
from pydub import AudioSegment
from pytube import YouTube
from moviepy.editor import VideoFileClip


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

def transcribe_file():
    st.title("Transcribe File")
    home_directory = os.getcwd()
    current_directory = home_directory + "/Audio_Library"

    uploaded_file = st.file_uploader("Upload Audio File", type=["wav", "mp3", "ogg"])

    if uploaded_file is not None:
        audio_path = os.path.join(current_directory, uploaded_file.name)
        with open(audio_path, "wb") as file:
            file.write(uploaded_file.getbuffer())

        audio_format = os.path.splitext(audio_path)[1][1:].lower()

        if audio_format == "ogg":
            converted_audio_path = convert_to_wav(audio_path)
            if converted_audio_path is None:
                st.write("Audio conversion failed.")
                return
            audio_path = converted_audio_path

        transcribe_button = st.button("Transcribe")

        if transcribe_button:
            st.write("Transcribing audio...")
            transcribed_text = perform_transcription(audio_path)

            if transcribed_text:
                text_path = home_directory + "/Transcribed_Library"
                text_path = os.path.splitext(audio_path)[0] + ".txt"
                with open(text_path, "w") as file:
                    file.write(transcribed_text)
                st.write("Transcription completed!")
                st.download_button("Download Transcription", text_path)
            else:
                st.write("Transcription failed.")


def convert_to_wav(audio_path):
    try:
        audio = AudioSegment.from_file(audio_path)
        converted_audio_path = os.path.splitext(audio_path)[0] + ".wav"
        audio.export(converted_audio_path, format="wav")        
        return converted_audio_path
    except Exception as e:
        st.write(f"Error converting audio: {e}")
        return None

def perform_transcription(audio_path):
    r = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:
        audio = r.record(source)

    try:
        transcribed_text = r.recognize_google(audio, language="en-US")
        progress_bar = st.progress(0)        
        for percent_complete in range(0, 101, 20):
            progress_bar.progress(percent_complete)
            time.sleep(0.1)
        progress_bar.empty()
        st.write("Transcription complete!")
        return transcribed_text
    except sr.UnknownValueError:
        st.write("Unable to transcribe audio. Please try again.")
    except sr.RequestError:
        st.write("Could not connect to the speech recognition service. Please try again later.")




def convert_to_wav(audio_file_path):
    audio = AudioSegment.from_file(audio_file_path)
    wav_file_path = os.path.splitext(audio_file_path)[0] + '.wav'
    audio.export(wav_file_path, format='wav')
    return wav_file_path

def transcribe_file():
    st.title("Transcribe File")
    home_directory = os.getcwd()
    current_directory = home_directory + "/Audio_Library"

    audio_file_path = upload_file(current_directory)

    transcribe_button = st.button("Transcribe")

    if transcribe_button:
        st.write("Transcribing audio...")
        
        # Convert the audio file to WAV format
        wav_file_path = convert_to_wav(audio_file_path)

        # Perform transcription on the converted WAV file
        transcribed_text = perform_transcription(wav_file_path)

        st.write("Transcription:")
        st.write(transcribed_text)

    upload_file(current_directory)


# def transcribe_file():
#     st.title("Transcribe File")
#     home_directory = os.getcwd()
#     current_directory = home_directory + "/Audio_Library"

#     uploaded_file = st.file_uploader("Upload Audio File", type=["wav", "mp3"])

#     if uploaded_file is not None:
#         audio_path = os.path.join(current_directory, uploaded_file.name)
#         with open(audio_path, "wb") as file:
#             file.write(uploaded_file.getbuffer())

#         transcribe_button = st.button("Transcribe")

#         if transcribe_button:
#             st.write("Transcribing audio...")

#             # Perform audio transcription
#             transcribed_text = perform_transcription(audio_path)

#             if transcribed_text:
#                 text_path = os.path.splitext(audio_path)[0] + ".txt"
#                 with open(text_path, "w") as file:
#                     file.write(transcribed_text)
#                 st.write("Transcription completed!")
#                 st.download_button("Download Transcription", text_path)
#             else:
#                 st.write("Transcription failed.")

# def perform_transcription(audio_path):
#     r = sr.Recognizer()

#     with sr.AudioFile(audio_path) as source:
#         audio = r.record(source)

#     try:
#         transcribed_text = r.recognize_google(audio, language="en-US")
#         return transcribed_text
#     except sr.UnknownValueError:
#         st.write("Unable to transcribe audio. Please try again.")
#     except sr.RequestError:
#         st.write("Could not connect to the speech recognition service. Please try again later.")






# def transcribe_file():
#     st.title("Transcribe File")
#     home_directory = os.getcwd()
#     current_directory = home_directory + "/Audio_Library"

#     upload_file(current_directory)

#     transcribe = st.button("Transcribe")
    
#     if transcribe:
#         st.write()
#         import speech_recognition as sr

#         def get_audio():
#             rObject = sr.Recognizer()
#             audio = ''
#             with sr.Microphone() as source:
#                 print("Listening...")
#                 audio = rObject.listen(source, phrase_time_limit = 5)
#             try:
#                 text = rObject.recognize_google(audio, language ='en-US')
#                 print("You : ", text)
#                 return text
#             except:
#                 return 0

        

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
            st.text_area("Transcript Content", transcript_content, height=300)

        left, center, right = st.columns([1, 1, 3])
        with right:
            download_file(selected_file_path)

    # upload_file(selected_directory_path)

    
def download_youtube():
    # Proofreading Tool
    # pip install pytube
    st.title("Download From Youtube")
    url = st.text_input("Youtube Url")
    download = st.button("Download")
    
    home_directory = os.getcwd()
    current_directory = home_directory + "/Download_Library"

    if download:
        # yt = YouTube(url)
        # audio_stream = yt.streams.filter(only_audio=True).first()
        # audio_file_path = audio_stream.download()
        # st.write("Audio downloaded:", current_directory)
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_file_path = audio_stream.download()
        print("Audio downloaded:", audio_file_path)

        # Convert the downloaded video to audio
        audio_file_name = os.path.splitext(audio_file_path)[0] + '.mp3'
        video_clip = VideoFileClip(audio_file_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(audio_file_name)
        audio_clip.close()
        video_clip.close()

        # Remove the original video file
        os.remove(audio_file_path)
        st.write("Audio downloaded:", current_directory)

def downloader(url):
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_file_path = audio_stream.download()
    print("Audio downloaded:", audio_file_path)

    # Convert the downloaded video to audio
    audio_file_name = os.path.splitext(audio_file_path)[0] + '.mp3'
    video_clip = VideoFileClip(audio_file_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_file_name)
    audio_clip.close()
    video_clip.close()

    # Remove the original video file
    os.remove(audio_file_path)

    print("Audio converted:", audio_file_name)

