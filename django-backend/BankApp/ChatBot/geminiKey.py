from google import genai
from google.genai import types
import os


API_KEY = "AIzaSyDq6vZSWy_fstI7jojzid2sB4RImX6MHnM" 

def ClientApi():
    return  genai.Client(api_key=API_KEY)