import streamlit as st 
import os
from dotenv import load_dotenv
load_dotenv() # it will load all the environment variables

import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

from youtube_transcript_api import YouTubeTranscriptApi



prompt = """You are a youtube video summerizer. You will be taking the transcript text 
and summerizing the entire video and providing the importent summery 
in points within 250 words not more then that The transcript text will be appended here : """






# getting the transcript 

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(
    video_id,
    languages=["en"]
)

        
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]
        return transcript

    except Exception as e:
        raise e
    
    
# getting the summary based on prompt from gemini

def generate_gemini_content(transcript_text,prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+transcript_text)
    return response.text



  
  
st.title("Youtube Transcript to Detailed Video Notes")


youtube_link = st.text_input("Enter yout youtube link: ")
if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg")
if st.button("Get Detial notes"):
    transtext = extract_transcript_details(youtube_link)
    
    if transtext:
        summary = generate_gemini_content(transcript_text=transtext,prompt=prompt)
        st.markdown("## Detail notes")
        st.write(summary)
    
    