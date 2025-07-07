import requests

# Hardcoded ElevenLabs API key
ELEVENLABS_API_KEY = "sk_a8e8731c2c0b6b3135b6b9986ef3805cb087d1dbefaed8c5"

def get_available_voices(api_key):
    """
    Fetch and display available voices from ElevenLabs API.
    """
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        voices = response.json().get("voices", [])

        if not voices:
            print("No voices found.")
            return

        print("Available Voices:")
        for index, voice in enumerate(voices, start=1):
            print(f"\nVoice {index}:")
            print(f"  Name: {voice.get('name')}")
            print(f"  Voice ID: {voice.get('voice_id')}")
            print(f"  Category: {voice.get('category')}")
            print(f"  Description: {voice.get('description')}")
            print(f"  Labels: {voice.get('labels')}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching voices: {e}")

if __name__ == "__main__":
    get_available_voices(ELEVENLABS_API_KEY)