import os
import openai

openai.api_key = os.getenv('CHAT_GPT_API_KEY')
model_list = openai.Model.list()
print(model_list)

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "大谷翔平について教えて"},
    ],
)

print(response)
