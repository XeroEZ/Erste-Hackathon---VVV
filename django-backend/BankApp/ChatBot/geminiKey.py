from google import genai
from google.genai import types
import os


API_KEY = "AIzaSyB5jcedYvtXN4j9BxYtFwWI6iaEwgxALrQ" 

def ClientApi():
    return  genai.Client(api_key=API_KEY)