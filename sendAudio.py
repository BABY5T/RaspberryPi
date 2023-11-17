import pyaudio
import wave
from socket import *
import os
import time

from dotenv import load_dotenv
import os 

# load .env
load_dotenv()
# 서버임
rasbIp = os.getenv('rasbIp')
audioSocketPort = int(os.getenv('audioSocketPort'))


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 0
RATE = 22050
RECORD_SECONDS = 4
INTERVAL = 4  # 녹음 간격 (초 단위)
RECORD_COUNT = 3  # 원하는 녹음 및 파일 전송 횟수
OUTPUT_DIR = '/home/luna20617/음악'
count = 0

def record_and_save():
    p = pyaudio.PyAudio()

    while True:
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print(f'Start recording {count + 1}')

        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print(f'Record {count + 1} stopped')

        stream.stop_stream()
        stream.close()

        wf = wave.open(os.path.join(OUTPUT_DIR, f"output.wav"), 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        # 파일 전송
        connectionSocket, addr = serverSocket.accept()
        try:
            filename = os.path.join(OUTPUT_DIR, f"output.wav")
            filesize = os.path.getsize(filename)

            with open(filename, 'rb') as file:
                connectionSocket.sendall(str(filesize).encode())
                connectionSocket.recv(1024)
                data = file.read(1024)

                while data:
                    connectionSocket.send(data)
                    data = file.read(1024)
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
serverPort = audioSocketPort
serverSocket.bind((rasbIp, audioSocketPort))
serverSocket.listen(1)
print('Ready to serve...')

# 함수 실행
record_and_save()