__authors__ = ("Renaud Balu", "LGDA")
__contact__ = "renaud_balu@hotmail.com"
__copyright__ = "Free and Open-source"
__date__ = "2024-06-12"
__version__ = "1.0.0"

import logging

import google.generativeai as genai

from service.lecteur.PeutSuggererUneChanson import PeutSuggererUneChanson


class GeminiService(PeutSuggererUneChanson):

    def __init__(self, api_key: str):
        logging.info("Initialisation service Gemini(Bard API)")
        self.__API_KEY = api_key
        genai.configure(api_key=self.__API_KEY)
        self.__model = genai.GenerativeModel('gemini-1.5-flash')

    def suggestion(self, titre_chanson: str) -> str:
        response = self.__model.generate_content(
            "I like this song: " + titre_chanson + ". Can you suggest me a similar one, i just want the name of the song and the artist name in the response?")
        return response.text
