from django.test import TestCase
import socket

try:
    host = socket.gethostbyname('api.openai.com')
    print(f"API OpenAI IP: {host}")
except socket.gaierror:
    print("Erro ao resolver o host da API do OpenAI")


