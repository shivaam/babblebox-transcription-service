import requests
from whisper_run import get_transcription
from pathlib import Path
from env_variables import BABBLEBOX_URL, BABBLEBOX_TRANSCRIPTION_API_KEY

# Path of the current script
script_path = Path(__file__).parent.resolve()

# Path of a file in the same directory as the script
file_path = script_path / 'somefile.txt'


# URLs for the API endpoints
api_url_chat = f"{BABBLEBOX_URL}/api/ChatMessage"
api_url_audio = f"{BABBLEBOX_URL}/api/AudioFile"
headers = {
    "Authorization": f"Token {BABBLEBOX_TRANSCRIPTION_API_KEY}"
}


def update_transcription_using_whisper(audio_message_id):
    file_name = download_audio_file_from_audio_message_id(audio_message_id)
    transcription = get_transcription(file_name)
    update_transcriptions(transcription,  audio_message_id)


def update_transcriptions(transcription, audio_message_id):
    url = f"{api_url_audio}/{audio_message_id}/"
    data = {"transcription_en": transcription}
    response = requests.patch(url, data=data, headers=headers)
    if response.status_code == 200:
        print("Transcription updated successfully.")
    else:
        print(f"Failed to update transcription. Status code: {response.status_code}")


def download_audio_file_from_audio_message_id(audio_message_id):
    audio_file_link = get_audio_file_link(audio_message_id)

    file_name = "/tmp/whisper/" + f"audio+{audio_message_id}.webm"
    download_file(audio_file_link, file_name)
    return file_name


# Function to get the audio message ID
def get_audio_message_id(chat_message_id):
    url = f"{api_url_chat}/{chat_message_id}/"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # Assuming the first item in the list contains the required ID
        print(data)
        return data['audio_message_id']
    else:
        raise Exception(f"Failed to get audio message ID for chat message ID {chat_message_id}. Status code: {response.status_code}")


# Function to get the audio file link
def get_audio_file_link(audio_message_id):
    # Construct the URL with the audio message ID
    url = f"{api_url_audio}/{audio_message_id}/"
    print(url)
    print(headers)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data['audio']
    else:
        raise Exception(f"Failed to get audio file link for audio message ID {audio_message_id}. Status code: {response.status_code}")


def download_file(url, file_name):
    print(f"Downloading file from URL: {url} and saving as: {file_name}")
    # Send an HTTP GET request to the file URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Define the local filename to save the file

        # Open the file in binary write mode and save the content
        with open(file_name, 'wb') as file:
            file.write(response.content)

        print(f"File downloaded successfully: {file_name}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")



#
# # Testing code here:
# get_audio_file_link("720e05e9-953b-49a7-aa57-81bdbea94d14")
