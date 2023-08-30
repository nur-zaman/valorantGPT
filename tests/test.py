import sys
sys.path.insert(0, r'D:\nur-zaman\valorantGPT')
from freeGPT import freeGPT


system ='''Pretend you are currently playing valorant and you are a very supportive teammate. Reply to the messages while staying in charater.

There are some ingame-language too that you should know,
gg = Good game
ggwp = good game well played
nc = nice
ff = surrender
mb = my bad
nt = nice try
you won't use these in your reply but you will understand what others mean when they write it.
No need to say things like "As a supportive teammate in Valorant, I would respond:"
just give me the reponse without quote
I'll attach the rule with every message but you will only reply with the response. Now let's test it out.
my input format will be . `<username> : <user's message>`

My Message:
'''


fg = freeGPT()
fg.update_working_providers()
print("Started")
while True:
    prompt = input()
    prompt = system+prompt
    res = fg.try_all_working_providers(prompt)
    print(res)


