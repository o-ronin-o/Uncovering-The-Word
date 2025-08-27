'''
PLEASE Note that the file should be ran from the src dirctory


to run it use the following commands in terminal
cd your local path\phase1-task1.1-audio-filtering\src
then 
python filter_audio.py

'''


import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import sounddevice as sd
import warnings
warnings.filterwarnings('ignore')


def load_audio(file_path):
    sample_rate,audio_data = wavfile.read(file_path)
    #change to mono if stereo
    if (len(audio_data.shape)== 2):
        audio_data = audio_data.mean(axe=1)

    if audio_data.dtype == np.int16:
        audio_data = audio_data.astype(np.float32) / 32768.0
    elif audio_data.dtype == np.int32:
        audio_data = audio_data.astype(np.float32) / 2147483648.0
    
    return sample_rate, audio_data    

def analyze_audio(sample_rate,audio_data,title):
    #plotting in time domain 
    plt.figure(figsize=(15,10))
    plt.subplot(3, 1, 1)
    time = np.linspace(0, len(audio_data) / sample_rate, len(audio_data))
    plt.plot(time, audio_data)
    plt.title(f'{title} - Time Domain')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)


   
    # Frequency domain plot 
    plt.subplot(3, 1, 2)
    frequencies = np.fft.fftfreq(len(audio_data), 1/sample_rate)
    fft_values = np.abs(np.fft.fft(audio_data))
    
    # Only plot positive frequencies
    positive_freq_mask = frequencies >= 0
    positive_freqs = frequencies[positive_freq_mask]
    positive_fft = fft_values[positive_freq_mask]
    
    plt.plot(positive_freqs, positive_fft)
    plt.title(f'{title} - Frequency Domain (Linear Scale)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.xlim(0, 5000)  #Focusing on speech frequencies
    plt.grid(True)
    
    # Frequency domain plot (log scale) to better see peaks
    plt.subplot(3, 1, 3)
    plt.semilogy(positive_freqs, positive_fft)
    plt.title(f'{title} - Frequency Domain (Log Scale)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude (log)')
    plt.xlim(0, 5000)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(rf'..\reports/{title.lower().replace(" ", "_")}_analysis.png')
    plt.show()
    
    # Find prominent peaks (potential noise frequencies)
    peaks, _ = signal.find_peaks(positive_fft, height=np.max(positive_fft)*0.1)
    prominent_peaks = peaks[positive_freqs[peaks] > 100]  # Ignore very low frequencies
    
    print("Prominent frequency peaks found:")
    for peak in prominent_peaks[:10]:  # Show top 10 peaks
        freq = positive_freqs[peak]
        magnitude = positive_fft[peak]
        print(f"  {freq:.1f} Hz - Magnitude: {magnitude:.2f}")
    
    return positive_freqs, positive_fft, prominent_peaks
def design_notch_filter(sample_rate, notch_freq, quality_factor=30):
    #Design a notch filter
    nyquist = sample_rate / 2.0
    normalized_freq = notch_freq / nyquist
    b, a = signal.iirnotch(normalized_freq, quality_factor)
    return b, a

def apply_filter(audio_data, b, a):
    #Apply filter to audio data
    filtered_audio = signal.filtfilt(b, a, audio_data)
    return filtered_audio
def play_audio(sample_rate, audio_data, title):
    """Play audio using sounddevice"""
    print(f"Playing {title}...")
    sd.play(audio_data, sample_rate)
    sd.wait()
def save_audio(file_path, sample_rate, audio_data):
    #Save audio file
    audio_int16 = (audio_data * 32767).astype(np.int16)
    wavfile.write(file_path, sample_rate, audio_int16)
    print(f"✓ Saved: {file_path}")


def main():
    file_path = r"..\data\raw\f04.wav"
    try:
        sample_rate, audio_data = load_audio(file_path)
        print(f"Duration: {len(audio_data)/sample_rate:.2f} seconds")
    except Exception as e:
        print(f"Failed to load audio: {e}")
        return
    frequencies, fft_values, peaks = analyze_audio(sample_rate, audio_data, "Original Sound")
    # Auto-suggest buzz frequency
   
    
    filtered_audio = audio_data 
    for peak in peaks[:10] :
        freq = frequencies[peak]
        b, a = design_notch_filter(sample_rate, freq, 35)
        filtered_audio = apply_filter(filtered_audio, b, a)
         
    filtered_audio = filtered_audio / np.max(np.abs(filtered_audio))
     
    print("5. Analyzing results...")
    analyze_audio(sample_rate, filtered_audio, "Filtered Audio")
    
    print("6. Saving and playing results...")
    #replace the path to your local device path
    save_audio(r'..\data\processed/processed_audio.wav', sample_rate, filtered_audio)
    play_audio(sample_rate, filtered_audio, "Cleaned Audio")
    
    print("\nFiltering complete! Check ../data/processed/processed_audio.wav'")

if __name__ == "__main__":
    main()