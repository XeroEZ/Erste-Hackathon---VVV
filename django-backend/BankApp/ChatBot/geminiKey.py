from google import genai
from google.genai import types
import os


API_KEY = "AIzaSyD2Ycz_cZdolLe9OhASIZGlRt0t__vvUQA" 

def ClientApi():
    return  genai.Client(api_key=API_KEY)