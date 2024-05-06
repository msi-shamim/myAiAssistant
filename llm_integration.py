from openai import OpenAI
from decouple import config

client = OpenAI(
    api_key=config("OPENAI_API_KEY")
)


def query_gpt(text):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"{text}"
            }
        ]
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content


# query = query_gpt("hello")