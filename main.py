from datetime import datetime
import requests
import json
import os
import subprocess


base_dir = os.path.dirname(os.path.abspath(__file__))
download_dir = os.path.join(base_dir, 'downloads')

if not os.path.exists(download_dir):
    os.makedirs(download_dir)

url = input("Please paste the URL of the meeting you want to download: ")

try:
    meeting_id = url.split("/meetings/")[1].strip('/')
    print(f"Found meeting ID: {meeting_id}")
except IndexError:
    print("Invalid URL format. Please ensure the URL is in the correct format.")
    exit()

auth_token = input("Please paste the auth token: ")

headers = {
    "Authorization": f"Bearer {auth_token}"
}

api_url = f"https://gw.tldv.io/v1/meetings/{meeting_id}/watch-page?noTranscript=true"
print(f"Making request to: {api_url}")

response = requests.get(api_url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print("Response JSON data:", json.dumps(data, indent=2)) 

    if 'video' in data and 'source' in data['video']:
        video_url = data['video']['source']
        print(f"Video URL: {video_url}")

        mp4_file_path = os.path.join(download_dir, f"{meeting_id}.mp4")

        command = [
            "ffmpeg", "-protocol_whitelist", "file,http,https,tcp,tls,crypto", 
            "-i", video_url, "-c", "copy", mp4_file_path
        ]
        result = subprocess.run(command, capture_output=True, text=True)

        print(result.stdout)
        print(result.stderr)

        if os.path.exists(mp4_file_path):
            print(f"Video converted successfully as {mp4_file_path}")
        else:
            print("Failed to convert the video.")
    else:
        print("'video' key not found in the response JSON.")
else:
    print(f"Failed to get the meeting information. Status code: {response.status_code}")
    print(f"Response content: {response.content}")
