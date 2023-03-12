import os
import openai

openai.api_key = os.getenv('CHAT_GPT_API_KEY')
model_list = openai.Model.list()
print(model_list)
