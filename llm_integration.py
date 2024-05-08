from openai import OpenAI
from decouple import config
import platform

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
                "content": f"explain in less than 3 sentences the following,"
                           f"{text}"
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
def query_gpt_do(text):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    temperature=0.1,
    messages=[
    {
    "role": "user",
    "content": f"in python,using subprocess, for {platform.platform()}, write me the following commands, use list comprehension for conditions, for,"
               f" {text}"
    # "content": f"{text}"
    }]
    )
    print(completion.choices[0].message)
    print(completion.choices[0].message.content.split("\n"))
    return completion.choices[0].message.content