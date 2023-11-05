import g4f

g4f.debug.logging = True
g4f.check_version = True


def useChatCompletion(prompt, role="user") -> str:
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": f"{role}", "content": f"{prompt}"}],
        stream=False,
    )
    return response
