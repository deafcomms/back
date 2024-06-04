import requests

# Replace with the path to your local WAV file
wav_file_path = './starwars.wav'

# Open the WAV file in binary mode
with open(wav_file_path, 'rb') as wav_file:
    # Read the file data
    wav_data = wav_file.read()

    # Set the request URL
    url = 'http://localhost:5000/receive_wav'

    # No need for multipart headers, send data directly
    response = requests.post(url, files={'file': wav_data}) 

    # Check the response
    if response.status_code == 200:
        print('WAV file uploaded successfully')
    else:
        print(f'Error uploading WAV file: {response.text}')
