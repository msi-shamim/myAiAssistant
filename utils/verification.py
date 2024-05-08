import time
import platform
from llm_integration import query_gpt, query_gpt_do_task, query_gpt_do
import webbrowser
import shlex, subprocess
import re

command_verbs = [
    "log in", "sign in", "hook up", "power up", "turn on", "boot up", "start up", "set up", "pull down", "pull down", "click on", "scroll up", "scroll down", "run out of", "back up", "print out", "hack into", "go down", "wipe out", "pop up", "popup", "plug in", "sign up", "key in", "opt in", "opt out", "filter out", "turn off", "shut down", "power down", "go online", "go offline", "make", "do", "write", "take", "close", "open", "create", "add", "delete"
]

def validate_data(data: dict):
    print(platform.platform())
    if "language" in data:
        if data["language"] != "en":
            return "I am having trouble understanding your language"
    if "text" in data:
        print(data["text"].lower().strip(" ,."))
        if data["text"].strip().lower().startswith("open"):
            commands = data["text"].strip().lower().split("and")
            print(commands)
            for command in commands:
                command = command.strip()
                print(command)
                if command.startswith("open browser"):
                    webbrowser.open('https://www.google.com/', new=2)

                if command.startswith("open notes"):
                    subprocess.run(['open', '-a', 'Notes'])

                if command.startswith("open weather"):
                    subprocess.run(['open', '-a', 'Weather'])

                if command.startswith("wait"):
                    subprocess.run(['sleep', '10'])
                if command.startswith("create"):
                    subprocess.run(["osascript", "-e", 'tell application "Notes" to make new note at folder "Notes" with properties {name:"test", body:""}'])

                if command.startswith("close"):
                    subprocess.Popen(["pkill", "-f", "Notes"])

        elif data["text"].strip().lower().startswith("close"):
            commands = data["text"].strip().lower().split("and")
            print(commands)
            for command in commands:
                command = command.strip()
                if command.startswith("close notes"):
                    subprocess.Popen(["pkill", "-f", "Notes"])
                if command.startswith("close weather"):
                    subprocess.Popen(["pkill", "-f", "Weather"])

        else:
            gpt_reply = query_gpt(data["text"])
            return gpt_reply


    # gpt_reply = query_gpt(data["text"])
    gpt_reply = "Done"

    return gpt_reply

# def validate_data(data: dict):
#     print(platform.platform())
#     if "language" in data:
#         if data["language"] != "en":
#             return "I am having trouble understanding your language"
#     if "text" in data:
#         if first_word:=data["text"].strip().split()[0] in command_verbs:
#             reply = query_gpt_do("open weather app and wait 15 sec and close notes app")
#             reply = reply.strip().split("\n")
#             print(reply)
#             for item in reply:
#                 # if item.startswith("    "):
#                 #     continue
#                     # print(item)
#                     # eval(item)
#
#                 if re.search(r"""^if.*:$""", item.strip()) is not None:
#                     continue
#                     # print(item)
#                     # exec(item)
#                 if re.search(r"""\S+=\S+""", item.strip()) is not None:
#                     print(item)
#                     exec(item)
#                 if item.strip().startswith("subprocess."):
#                     print(item)
#                     eval(item)
#             # webbrowser.open('https://www.google.com/', new=2)
#             # cmd = "open /System/Applications/Music.app"
#             # p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#             # stdout, stderr = p.communicate()
#             # subprocess.run(["open", "/System/Applications/Notes.app"])
#             # time.sleep(3)
#             # # Close the Notes app after a delay (e.g., 5 seconds)
#             # subprocess.run(["osascript", "-e", 'tell application "Notes" to quit'])
#             #
#             # applescript = """
#             # tell application "Notes"
#             #     activate
#             #     make new note with properties {name:"New Note", content:"Hello, world!"}
#             #     delay 2 -- Wait for the note to open
#             #     tell application "System Events"
#             #         keystroke "w" using command down -- Shortcut to close the note
#             #     end tell
#             # end tell
#             # """
#             #
#             # # Execute the AppleScript
#             # subprocess.call(['osascript', '-e', applescript])
#             # print("", first_word)
#             return "Done!"
#
#
#     gpt_reply = query_gpt(data["text"])
#     return gpt_reply



