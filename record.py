import pyaudio
import wave
from socket import *
import os
import time

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 22050
RECORD_SECONDS = 4
INTERVAL = 3  # 녹음 간격 (초 단위)
RECORD_COUNT = 1  # 원하는 녹음 및 파일 전송 횟수
OUTPUT_DIR = '/home/lunar20617/음악'

def record_and_save(serverSocket):
    p = pyaudio.PyAudio()
    count = 0

    while count < RECORD_COUNT:
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print(f'Start recording {count + 1}/{RECORD_COUNT}')

        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print(f'Record {count + 1}/{RECORD_COUNT} stopped')

        stream.stop_stream()
        stream.close()

        wf = wave.open(os.path.join(OUTPUT_DIR, f"output_{count + 1}.wav"), 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        # 파일 전송
        connectionSocket, addr = serverSocket.accept()
        try:
            with open(os.path.join(OUTPUT_DIR, f"output_{count + 1}.wav"), 'rb') as f:
                for l in f:
                    connectionSocket.sendall(l)
        except FileNotFoundError:
            print(f"File not found:")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            connectionSocket.close()

        # 대기 시간
        time.sleep(INTERVAL)
        count += 1

    print("Recording and file transfer completed.")
    serverSocket.close()

# 서버 소켓 설정
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 12345
serverSocket.bind(("", serverPort))
serverSocket.listen(1)
print('Ready to serve...')

# 함수 실행
record_and_save(serverSocket)
