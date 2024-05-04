from faster_whisper import WhisperModel


def get_transcription(file):
    print("File name used for whisper transcription: ", file)
    model_size = "small"

    model = WhisperModel(model_size, device="cpu", compute_type="int8", download_root = '/tmp/whisper')
    segments, info = model.transcribe(file, beam_size=5, language="en", task='translate')

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    text = ""
    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        text += segment.text

    return text
