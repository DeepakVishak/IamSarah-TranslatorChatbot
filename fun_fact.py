import os
from bardapi import Bard
from dotenv import load_dotenv

load_dotenv()
token = os.environ['cAi2g49qKNmZzORx43PNyLrQpAFmQKNfSACNk2OOLvkA8NzBdkOW9n70oIi-KA8-R8C3Uw.']
bard = Bard(token=token)
response = bard.get_answer("What is a LLM?")['content']
print(response)