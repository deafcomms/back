from flask import Flask, request, Response, make_response
import wave
import io
import numpy as np
import whisper
from scipy.signal import resample

app = Flask(__name__)

def bytes_to_wav(file_bytes):
    with wave.open(io.BytesIO(file_bytes), 'rb') as wav_file:
        n_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        frame_rate = wav_file.getframerate()
        n_frames = wav_file.getnframes()
        audio_frames = wav_file.readframes(n_frames)

        dtype = np.int16 if sample_width == 2 else np.uint8
        audio_array = np.frombuffer(audio_frames, dtype=dtype).astype(np.float32)

        # Normalize audio data to [-1, 1] range
        if dtype == np.int16:
            audio_array /= 32767
        else:
            audio_array /= 255

        return audio_array, frame_rate

@app.route('/receive_wav', methods=['POST'])
def receive_wav():
    uploaded_file = request.files.get('file')
    if not uploaded_file:
        return Response('No WAV file uploaded', status=400)

    try:
        # Read the file content as a byte stream
        file_content = uploaded_file.read()

        # Ensure the byte stream is passed to the wave module
        with wave.open(io.BytesIO(file_content), 'rb') as wav_file:
            num_channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()
            frame_rate = wav_file.getframerate()
            num_frames = wav_file.getnframes()
            compression_type = wav_file.getcomptype()
            compression_name = wav_file.getcompname()
            
            # Display the information
            print(f"Number of Channels: {num_channels}")
            print(f"Sample Width (bytes): {sample_width}")
            print(f"Frame Rate (samples per second): {frame_rate}")
            print(f"Number of Frames: {num_frames}")
            print(f"Compression Type: {compression_type}")
            print(f"Compression Name: {compression_name}")

        # Convert the byte stream to a writable numpy array
        audio_data, frame_rate = bytes_to_wav(file_content)
        
        # Load Whisper model and transcribe the audio
        model = whisper.load_model("base")
        print("load model")
        result = model.transcribe(audio_data)
        print("transcribe model")
        transcription_text = result['text']
        print("res == ", transcription_text)

        # print(transcription_text)

        response = make_response(transcription_text)
        response.headers['Content-Disposition'] = 'attachment; filename=transcription.txt'
        response.headers['Content-Type'] = 'text/plain'
        print(response)

        return response
    except Exception as e:
        print(f"Error processing file: {e}")
        return Response('Internal server error', status=500)

if __name__ == '__main__':
    app.run(debug=True)  # Set debug=False for production
