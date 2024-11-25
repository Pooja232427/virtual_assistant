from openai import OpenAI
 
# pip install openai 
# if you saved the key under a different environment variable name, you can do something like:
client = OpenAI(
  api_key="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",
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a virtual assistant named Yara skilled in general tasks like Alexa and Google Cloud"},
    {"role": "user", "content": "what is coding"}
  ]
)

print(completion.choices[0].message.content)