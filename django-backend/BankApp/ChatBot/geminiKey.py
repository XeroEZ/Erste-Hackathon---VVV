from google import genai
from google.genai import types
import os


API_KEY = "AIzaSyCzcqrr_PQ2bbX2jxT9ZMgvyGAeWr0iFHU" 

def ClientApi():
    return  genai.Client(api_key=API_KEY)