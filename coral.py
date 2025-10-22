import os
import json
import bcrypt
import asyncio
import httpx
import requests
from datetime import datetime


version = "0.0.1"
database_auth_url = "https://shineflixtv.netlify.app/user_database.json" 
response_auth = requests.get(database_auth_url)
data_auth = response_auth.json()
corals_data = os.path.expanduser("~/.config/coral/")
os.makedirs(corals_data, exist_ok=True)
coral_user_auth_local_data = os.path.join(corals_data, "user.json")
corals_logs = os.path.join(corals_data, "coral_logs.json")
settings = os.path.join(os.path.expanduser(corals_data), "settings.json")
now = datetime.now()
current_time = now.strftime("%d-%m-%Y %H:%M:%S")
def write_log(message):
    if os.path.exists(corals_logs):
        with open(corals_logs, "r", encoding="utf-8") as f:
            data = json.load(f)
            logs_list = data.get("logs", [])
    else:
        logs_list = []
    logs_list.append(f"{current_time} - {message}")
    with open(corals_logs, "w", encoding="utf-8") as f:
        json.dump({"logs": logs_list}, f, ensure_ascii=False, indent=4)

async def download(url, filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    async with httpx.AsyncClient(http2=True, verify=True) as client:
        response = await client.get(url)
        response.raise_for_status()
        with open(filepath, "wb") as f:
            f.write(response.content)
        print("Download complete!")
        write_log("Download complete!")
    
def login():
    print("Please login to coral")
    username = input("Username: ")
    password = input("Password: ")

    if username in data_auth["users"]:
        stored_hash = data_auth["users"][username]["password"].encode()
        if bcrypt.checkpw(password.encode(), stored_hash):
            session_token_auth = data_auth["users"][username]["session_token"]
            user_data = {
                "username": username,
                "session_token": session_token_auth
            }
            with open(coral_user_auth_local_data, "w", encoding="utf-8") as user:
                json.dump(user_data, user, ensure_ascii=False, indent=4)

            write_log("Account has successfully been logged in")
            return
        else:
            print("Password or username isn't correct")
            write_log("Account has not successfully been logged in")
    else:
        print(f"{username} account does not exist on Coral")
        write_log("Tried logging in to account which does not exist on Coral!")

if os.path.exists(coral_user_auth_local_data):
    with open(coral_user_auth_local_data, "r") as f:
        userdata = json.load(f)
else:
    write_log("User.json file does not exist.")
    userdata = {}
    login()
    with open(coral_user_auth_local_data, "r", encoding="utf-8") as f:
        userdata = json.load(f)

with open(coral_user_auth_local_data, "r", encoding="utf-8") as f:
    userdata = json.load(f)
    

username_local = userdata.get("username")
session_token_local = userdata.get("session_token")
if username_local and session_token_local:
    if username_local in data_auth["users"]:
        session_token_online = data_auth["users"][username_local]["session_token"]

        if session_token_local == session_token_online:
            print("Success, session token is valid")
            write_log("Session token is valid!")
        else:
            print("Failure, session token isn't valid")
            write_log("Failed to authenticate session token!")
            login()
    else:
        print("Username not found in online database, re-authenticate.")
        write_log("Username not found in online database, re-authenticate")
        login()
else:
    print("No valid local session was found.")
    write_log("No valid local session was found.")
    login()



def update_channel():
    print("What release channel do you want to use? (This can be changed later): \nSTABLE - This is the stable version of the Coral client (Updated every month)\nBETA - This is the beta version of the Coral client (This is a little bit less stable than the STABLE version, it is updated every week)\nALPHA - This version is NOT stable or beta software, this is THE ALPHA version, this version is basicly every push to the repo on Github.\n")
    answer = input().upper()
    if answer == "STABLE":
        update_channel_data = {
            "release_channel" : "STABLE",
            "url": ""
        }
        write_log("Set release channel to STABLE")
    elif answer == "BETA":
        update_channel_data = {
            "release_channel" : "BETA",
            "url": ""
        }
        write_log("Set release channel to BETA")
    elif answer == "ALPHA":
        update_channel_data = {
            "release_channel": "ALPHA",
            "url": "https://raw.githubusercontent.com/143domi1/coral/refs/heads/main/coral.py"
        }
        write_log("Set release channel to ALPHA")
    else:
        print("Invalid option, please choose STABLE or BETA or ALPHA.")
        write_log("User chooses invalid option in release channel menu.")
        update_channel()

    with open(settings, "w", encoding="utf-8") as settings_file:
        json.dump(update_channel_data, settings_file, ensure_ascii=False, indent=4)
    

def update_coral():
    print(f"Current version: {version}")
    with open(settings, "r") as settings:
        setting_db = json.load(settings)
    asyncio.run(download(setting["url"], "coral.py"))
    write_log("Downloaded new version!")
    
if not os.path.exists(settings):
    update_channel()
update_channel()