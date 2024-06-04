import whisper

def transcribe_audio(file_path):
    model = whisper.load_model("small")
    result = model.transcribe(file_path)
    return result

# def seconds_to_timestamp(seconds):
#     # Convert seconds to a timedelta object
#     td = datetime.timedelta(seconds=seconds)
#     # Convert timedelta to string
#     total_seconds = int(td.total_seconds())
#     milliseconds = int((td.total_seconds() - total_seconds) * 1000)
#     hours, remainder = divmod(total_seconds, 3600)
#     minutes, seconds = divmod(remainder, 60)
#     return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

# def write_text(transcription_result, text_path):
#     with open(text_path, 'w', encoding='utf-8') as f:
#         for segment in transcription_result['segments']:
#             text = segment['text'].strip()
#             f.write(f"{text}\n")

# def write_srt(transcription_result, srt_path):
#     segments = transcription_result['segments']
#     with open(srt_path, 'w', encoding='utf-8') as f:
#         for i, segment in enumerate(segments):
#             start = seconds_to_timestamp(segment['start'])
#             end = seconds_to_timestamp(segment['end'])
#             text = segment['text'].strip()
#             f.write(f"{i + 1}\n")
#             f.write(f"{start} --> {end}\n")
#             f.write(f"{text}\n\n")