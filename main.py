import configparser
import itertools
from time import sleep
from tqdm import trange, tqdm
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.sync import TelegramClient
from telethon import functions, types

config = configparser.ConfigParser()
config.read("config.ini")

api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

phone = config['Telegram']['phone']
username = config['Telegram']['username']
client = TelegramClient(username, api_id, api_hash, device_model='iPhone 15 Pro Max', system_version="4.16.34-vxpetrol")

typeSearch = config['Finder']['type']

with open('config.ini', 'r', encoding='utf-8') as f:
    config = f.read()
    keywords = config.split('keywords = ')[1].replace('\n','').split(';')

requests=[]

for i in range(len(keywords)):
    print(f"[+] Operating {i+1}/{len(keywords)} keyword")
    iterated = list(itertools.permutations(keywords, i+1))

    for i in trange(len(iterated), desc="Preparing requests", unit="request"):
        iterated[i] = ' '.join(iterated[i])

    requests += set(iterated)

requests = set(requests)

print(f"[+] Created {len(requests)} requests")

if len(requests) > 1000:
    confirmation = input("[!] Number of requests more than 1000! Do you understand, that this may lead ban of telegram account? [Y (Yes)/N (No)]")
    if not confirmation.lower() in "yes":
        exit()

results={}

print("[+] Starting telegram client")
client.connect()
if not client.is_user_authorized():
    phone_code_hash = client.send_code_request(phone).phone_code_hash
    try:
        client.sign_in(phone, input('Enter the code: '))
    except SessionPasswordNeededError:
        client.sign_in(password=input('Password: '))

print("[+] Staring search...\n")

for i, request in enumerate(requests):
    print(f"[+] Sending request {i+1}/{len(requests)}")
    print("[+] Request: "+request)
    if i%20 == 0:
        print("[+] Every 20 requests server cool downing, please wait...")
    result = client(functions.contacts.SearchRequest(
        q=request,
        limit=100
    ))

    print(f"[+] Found {len(result.chats)} chats")

    counter=0
    for chat in result.chats:
        if (not chat.id in results.keys()) and (not chat.join_request):
            if (typeSearch == "group"):
                if not chat.megagroup:
                    continue
            elif (typeSearch == "channel"):
                if chat.megagroup:
                    continue

            results[chat.id] = chat
            counter+=1

    print(f"[+] Added {counter} new chats")
    print("------------------------------------------")

print(f"[+] Search ended, found {len(results)} chats")
with open("output.txt", 'w') as f:
    f.write('')

for result in tqdm(results, desc="Saving", unit="result"):
    url = "https://t.me/" + (results[result].username if results[result].username else results[result].usernames[0].username)
    with open("output.txt", 'a') as f:
        f.write(url+"\n")

client.disconnect()
