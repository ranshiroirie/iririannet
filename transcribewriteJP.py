# !/usr/bin/env python
# coding: utf-8
import argparse
import io
import sys
import codecs
import datetime
import locale

def transcribe_file(speech_file):
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='ja-JP')
    
    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    operationResult = operation.result()

    d = datetime.datetime.today()
    today = d.strftime("%Y%m%d-%H%M%S")
    fout = codecs.open('output{}.txt'.format(today), 'a', 'shift_jis')

    for result in operationResult.results:
      for alternative in result.alternatives:
          fout.write(u'{}\n'.format(alternative.transcript))
    fout.close()

def transcribe_gcs(gcs_uri):
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        sample_rate_hertz=16000,
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        language_code='ja-JP')

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    operationResult = operation.result()

    d = datetime.datetime.today()
    today = d.strftime("%Y%m%d-%H%M%S")
    fout = codecs.open('output{}.txt'.format(today), 'a', 'shift_jis')

    for result in operationResult.results:
      for alternative in result.alternatives:
          fout.write(u'{}\n'.format(alternative.transcript))
    fout.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='File or GCS path for audio file to be recognized')
    args = parser.parse_args()
    if args.path.startswith('gs://'):
        transcribe_gcs(args.path)
    else:
        transcribe_file(args.path)
