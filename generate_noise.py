import numpy as np
from scipy.io import wavfile

# Parametry
sample_rate = 44100 # Standardowe próbkowanie CD
duration = 3.0      # 3 sekundy
frequency = 440.0   # Ton A (440 Hz)

# Czas
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# 1. Czysty sygnał (Sinusoida)
clean_signal = 0.5 * np.sin(2 * np.pi * frequency * t)

# 2. Biały szum
noise = np.random.normal(0, 0.3, clean_signal.shape)

# 3. Zaszumiony sygnał (Sygnał + Szum)
noisy_signal = clean_signal + noise

# Normalizacja do formatu 16-bit PCM (standard plików WAV)
noisy_signal_16bit = np.int16(noisy_signal / np.max(np.abs(noisy_signal)) * 32767)

# Zapis do pliku
wavfile.write("test_noisy_audio.wav", sample_rate, noisy_signal_16bit)
print("Wygenerowano plik: test_noisy_audio.wav")