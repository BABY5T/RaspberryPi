import numpy as np
import tensorflow as tf


model_path = '/Users/kim/IOTT/resnet.h5'
model = tf.keras.models.load_model(model_path)
#model.summary() 

import librosa
from skimage.transform import resize

classes = ['sad', 'hug', 'diaper', 'hungry',
           'sleepy', 'awake', 'uncomfortable']




def get_input_vector_from_file(file_path: str) -> np.ndarray:
    #import pdb;pdb.set_trace()
    y, sr = librosa.load(file_path, sr=16000)
    mel_spec = librosa.feature.melspectrogram(
        y=y, sr=sr, n_mels=128, n_fft=2048, hop_length=501)
    mel_spec_dB = librosa.power_to_db(mel_spec, ref=np.max)
    RATIO = 862 / 128
    mel_spec_dB_resized = resize(mel_spec_dB, (mel_spec_dB.shape[0], mel_spec_dB.shape[1] * RATIO),
                                 anti_aliasing=True, mode='reflect')
    mel_spec_dB_stacked = np.stack([mel_spec_dB_resized] * 3, axis=-1)
    return mel_spec_dB_stacked[np.newaxis, ]




test_vector = get_input_vector_from_file('/Users/kim/IOTT/received_1700209708.wav')

print(test_vector.shape)

tf.config.set_visible_devices([], 'GPU')

predictions = model.predict(test_vector)[0]

print(classes[np.argmax(predictions)])