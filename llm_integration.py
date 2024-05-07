from openai import OpenAI
from decouple import config

client = OpenAI(
    api_key=config("OPENAI_API_KEY")
)


def query_gpt(text):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=1,
        messages=[
            {
                "role": "user",
                # "content": f"separate the commands for the following sentence, {text}"
                "content": f"{text}"
            }
        ]
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content

# query_gpt("open a file notes and close it")


def query_gpt_do_task(text):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=1,
        messages=[
            {
                "role": "user",
                "content": f"separate the commands for the following sentence, {text}"
                # "content": f"{text}"
            }
        ]
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content