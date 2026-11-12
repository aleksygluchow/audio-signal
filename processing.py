import io
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') # Wyłącza tryb interaktywny, niezbędne dla serwera

def denoise_audio(file_bytes: bytes, threshold_ratio: float = 0.05):
    # Wczytanie pliku audio z bufora pamięci
    rate, data = wavfile.read(io.BytesIO(file_bytes))
    
    # Jeśli stereo, bierzemy jeden kanał dla uproszczenia
    if len(data.shape) > 1:
        data = data[:, 0]
        
    # Szybka transformata Fouriera (FFT)
    n = len(data)
    fft_data = np.fft.fft(data)
    
    # Bramkowanie spektralne (Spectral Gating) - usuwanie tła
    max_amp = np.max(np.abs(fft_data))
    threshold = max_amp * threshold_ratio
    
    fft_data_clean = fft_data.copy()
    fft_data_clean[np.abs(fft_data) < threshold] = 0
    
    # Odwrotna transformata (IFFT) i normalizacja do 16-bit PCM
    clean_data = np.fft.ifft(fft_data_clean).real
    clean_data = np.int16(clean_data / np.max(np.abs(clean_data)) * 32767)
    
    # Zapis odszumionego audio do bufora
    out_audio = io.BytesIO()
    wavfile.write(out_audio, rate, clean_data)
    out_audio.seek(0)
    
    # Generowanie spektrogramów przed i po
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    ax1.specgram(data, Fs=rate, NFFT=1024, cmap='inferno')
    ax1.set_title("Oryginalny sygnał (Zaszumiony)")
    ax1.set_ylabel("Częstotliwość [Hz]")
    
    ax2.specgram(clean_data, Fs=rate, NFFT=1024, cmap='inferno')
    ax2.set_title("Odszumiony sygnał (Po FFT)")
    ax2.set_ylabel("Częstotliwość [Hz]")
    ax2.set_xlabel("Czas [s]")
    
    plt.tight_layout()
    
    # Zapis wykresu do bufora
    out_plot = io.BytesIO()
    plt.savefig(out_plot, format='png')
    out_plot.seek(0)
    plt.close(fig)
    
    return out_audio, out_plot