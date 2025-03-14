import numpy as np
import soundfile as sf
import librosa
import librosa.display
import matplotlib.pyplot as plt
import scipy.signal as signal
import noisereduce as nr
from scipy.signal import wiener

filename = "C:/voice/johnvoice3.wav"
y, sr = librosa.load(filename, sr=None)

n_fft = 2048
hop_length = 512
D = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
magnitude, phase = np.abs(D), np.angle(D)

filtered_magnitude = np.apply_along_axis(
    lambda x: signal.medfilt(x, kernel_size=3), axis=1, arr=magnitude
)


def frequency_weighting(
    freqs, low_cutoff=100, high_cutoff=4000, low_scale=0.5, high_scale=0.6
):
    """使用 Sigmoid 函數平滑地加權頻率，避免突兀的降噪"""
    low_weights = 1 / (1 + np.exp(-0.02 * (freqs - low_cutoff)))
    high_weights = 1 / (1 + np.exp(0.002 * (freqs - high_cutoff)))
    return low_weights * low_scale + high_weights * high_scale


freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
weights = frequency_weighting(freqs)

filtered_magnitude = filtered_magnitude * weights[:, np.newaxis]

for i in range(filtered_magnitude.shape[1]):
    filtered_magnitude[:, i] = wiener(filtered_magnitude[:, i], mysize=5)

filtered_D = filtered_magnitude * np.exp(1j * phase)

filtered_y = librosa.istft(filtered_D, hop_length=hop_length)

filtered_y = nr.reduce_noise(y=filtered_y, sr=sr, stationary=False, prop_decrease=0.8)

rms_original = np.sqrt(np.mean(y**2))
rms_filtered = np.sqrt(np.mean(filtered_y**2))
gain = min(1.5, rms_original / (rms_filtered + 1e-8))
filtered_y = filtered_y * gain

output_filename = "C:/voice/johnvoice_filtered_final3.wav"
sf.write(output_filename, filtered_y, sr)
print(f"Filtered speech saved as {output_filename}")

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
librosa.display.specshow(
    librosa.amplitude_to_db(magnitude, ref=np.max),
    sr=sr,
    hop_length=hop_length,
    y_axis="log",
    x_axis="time",
)
plt.title("Original Spectrogram")
plt.colorbar(format="%+2.0f dB")

plt.subplot(1, 2, 2)
librosa.display.specshow(
    librosa.amplitude_to_db(filtered_magnitude, ref=np.max),
    sr=sr,
    hop_length=hop_length,
    y_axis="log",
    x_axis="time",
)
plt.title("Filtered Spectrogram")
plt.colorbar(format="%+2.0f dB")

plt.subplots_adjust(wspace=0.3)
plt.show()
