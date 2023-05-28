import deepai


def useTheb(prompt):
    response = ""
    for token in deepai.Completion.create(prompt):
        response += token
    return response


def readInitPrompt(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    return content


content = readInitPrompt(r"prompt.txt")
while True:
    prompt = input("Question:")
    if prompt == "!stop":
        break
    sentMsg = f"valplayer#9999 : {prompt}"
    content_prompt = content + sentMsg
    response = useTheb(content_prompt)
    # response = useTheb(prompt)

    print(f"Answer: {response}")
