import os
import json
import requests
import bcrypt

database_auth_url = "https://shineflixtv.netlify.app/user_database.json" #ignore this im gonna fill it later
response_auth = requests.get(database_auth_url)
data_auth = response_auth.json()
corals_data = os.path.expanduser("~/.config/coral/")
os.makedirs(corals_data, exist_ok=True)
coral_user_auth_local_data = os.path.join(corals_data, "user.json")

settings = os.path.join(os.path.expanduser(corals_data), "settings.json")

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
			return
		else:
			print("Password or username isn't correct")
	else:
		print(f"{username} account does not exist on Coral")

if os.path.exists(coral_user_auth_local_data):
    with open(coral_user_auth_local_data, "r") as f:
        userdata = json.load(f)
else:
    userdata = {}
    login()  # creates user.json
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
		else:
			print("Failure, session token isn't valid")
			login()
	else:
		print("Username not found in online database, re-authenticate.")
		login()
else:
	print("No valid local session was found.")
	login()


def update_channel():
	print("What release channel do you want to use? (This can be changed later): \nSTABLE - This is the stable version of the Coral client (Updated every month)\nBETA - This is the beta version of the Coral client (This is a little bit less stable than the STABLE version, it is updated every week)\nALPHA - This version is NOT stable or beta software, this is THE ALPHA version, this version is basicly every push to the repo on Github.\n")
	answer = input().upper()
	if answer == "STABLE":
		update_channel_data = {
			"release_channel" : "STABLE",
			"url": ""
		}
	elif answer == "BETA":
		update_channel_data = {
			"release_channel" : "BETA",
			"url": ""

	}
	elif answer == "ALPHA":
		update_channel_data = {
			"release_channel": "ALPHA",
			"url": ""

		}
	else:
		print("Invalid option, please choose STABLE or BETA or ALPHA.")
		update_channel()
	with open(settings, "w", encoding="utf-8") as user:
		json.dump(update_channel_data, user, ensure_ascii=False, indent=4)


