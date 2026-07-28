import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

# -------------------------------------------------
# Simple General Plotting Helper
# -------------------------------------------------
def plot_fig(title, xlabel="Time (s)", ylabel="Amplitude"):
    """Applies common figure formatting and displays the plot."""
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

# -------------------------------------------------
# 1. Load Speech Audio
# -------------------------------------------------
audio_path = "harvard.wav"  # Ensure speech.wav is in the same folder
y, sr = librosa.load(audio_path, sr=16000, mono=True)

# DC offset removal and normalization
y = y - np.mean(y)
y = y / (np.max(np.abs(y)) + 1e-9)

time = np.arange(len(y)) / sr

# -------------------------------------------------
# 2. Section 1: Time-Domain Waveform
# -------------------------------------------------
plt.figure(figsize=(12, 4))
plt.plot(time, y, linewidth=0.8)
plot_fig("Speech Waveform", "Time (s)", "Normalized Amplitude")

# -------------------------------------------------
# 3. Section 2: Framing & Windowing
# -------------------------------------------------
alpha = 0.97
pre_emphasized = np.append(y[0], y[1:] - alpha * y[:-1])

frame_length = int(0.025 * sr)  # 25 ms
hop_length = int(0.010 * sr)    # 10 ms

frames = librosa.util.frame(
    pre_emphasized,
    frame_length=frame_length,
    hop_length=hop_length
).T

hamming = np.hamming(frame_length)
windowed_frames = frames * hamming

frame_index = min(10, len(frames) - 1)
frame_time_ms = np.arange(frame_length) / sr * 1000

plt.figure(figsize=(12, 4))
plt.plot(frame_time_ms, frames[frame_index], label="Original frame")
plt.plot(frame_time_ms, windowed_frames[frame_index], label="Windowed frame")
plt.plot(frame_time_ms, hamming, "--", label="Hamming window")
plt.legend()
plot_fig("Framing and Hamming Windowing", "Time inside frame (ms)", "Amplitude")

# -------------------------------------------------
# 4. Section 2: STFT Spectrogram
# -------------------------------------------------
D = librosa.stft(
    y,
    n_fft=512,
    hop_length=hop_length,
    win_length=frame_length,
    window="hamming"
)
S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)

plt.figure(figsize=(12, 4))
librosa.display.specshow(S_db, sr=sr, hop_length=hop_length, x_axis="time", y_axis="hz")
plt.ylim(0, 8000)
plt.colorbar(format="%+2.0f dB")
plot_fig("STFT Speech Spectrogram", "Time (s)", "Frequency (Hz)")

# -------------------------------------------------
# 5. Section 2: Energy & Zero-Crossing Rate (STE / ZCR)
# -------------------------------------------------
rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
zcr = librosa.feature.zero_crossing_rate(y, frame_length=frame_length, hop_length=hop_length)[0]
feature_time = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop_length)

plt.figure(figsize=(12, 4))
plt.plot(feature_time, rms / np.max(rms), label="RMS Energy (STE)")
plt.plot(feature_time, zcr / np.max(zcr), label="Zero-Crossing Rate (ZCR)")
plt.legend()
plot_fig("Short-Time Features (STE vs ZCR)", "Time (s)", "Normalized Value")

# -------------------------------------------------
# 6. Section 3: Linear Predictive Coding (LPC Envelope)
# -------------------------------------------------
single_frame = windowed_frames[frame_index]
a_lpc = librosa.lpc(single_frame, order=12)

fft_size = 512
freqs = np.linspace(0, sr / 2, fft_size // 2 + 1)
fft_spectrum = 20 * np.log10(np.abs(np.fft.rfft(single_frame, n=fft_size)) + 1e-9)
lpc_envelope = 20 * np.log10(np.abs(1.0 / (np.fft.rfft(a_lpc, n=fft_size) + 1e-9)))

plt.figure(figsize=(12, 4))
plt.plot(freqs, fft_spectrum, label="FFT Spectrum", color="gray", alpha=0.6)
plt.plot(freqs, lpc_envelope - np.max(lpc_envelope) + np.max(fft_spectrum), label="LPC Envelope (Order 12)", color="red", linewidth=1.5)
plt.legend()
plot_fig("LPC Spectral Envelope vs. FFT Spectrum", "Frequency (Hz)", "Magnitude (dB)")

# -------------------------------------------------
# 7. Section 4: MFCC Extraction
# -------------------------------------------------
mfcc = librosa.feature.mfcc(
    y=y,
    sr=sr,
    n_mfcc=13,
    n_fft=512,
    hop_length=hop_length,
    win_length=frame_length,
    window="hamming"
)

plt.figure(figsize=(12, 4))
librosa.display.specshow(mfcc, x_axis="time", sr=sr, hop_length=hop_length)
plt.colorbar()
plot_fig("13 Mel-Frequency Cepstral Coefficients (MFCCs)", "Time (s)", "MFCC Index")