import requests
import os 
import shutil
from datetime import datetime


download_folder = 'felix_frimpong'


if os.path.exists('felix_frimpong'):
    try:
        shutil.rmtree(download_folder)
        print(f'Directory {download_folder} has been removed successfully')
    except Exception as e:
        print(f"Error: {e}")

if not os.path.exists(download_folder):
    os.makedirs(download_folder)
    print(f" Directory: {download_folder} created. ")


local_file_path = os.path.join(download_folder, "felix_frimpong")


url = "https://raw.githubusercontent.com/sdg000/pydevops_intro_lab/main/change_me.txt"

response = requests.get(url)

if response.status_code == 200:
    print(f"File successfully downloaded.")
    with open(local_file_path, "wb") as file:
        file.write(response.content)
        print("File saved successfully.")
else:
    print(f"{response.status_code} , download Failed")


user_input = input("Describe what you have learnt thus far in a sentence: \n")
time_now = datetime.now()
current_time = time_now.strftime("%Y-%m-%d %H:%M:%S")

with open(local_file_path, "w") as file:
    file.write(user_input + "\n")
    file.write(f"Last modified on: {current_time}.")
    print("FIle successfully modified.")


with open(local_file_path, "r") as file:
    print("\n You Entered: ", end="")
    print(file.read())
    print("\n")
