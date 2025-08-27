# Task 1.1 Report: Audio Filtering Approach

## 📋 Overview
This report documents the approach taken to recover a hidden word from a noisy audio signal contaminated with buzz noise.

## 🔍 Analysis Method
1. **Signal Analysis**: Used Fourier Transform to analyze the audio in frequency domain
2. **Noise Identification**: Identified a prominent buzz noise at 1000Hz
3. **Filter Selection**: Chose a notch filter to specifically target the buzz frequency

## 🛠️ Technical Implementation
- **Library**: SciPy for signal processing, NumPy for numerical operations
- **Filter Type**: IIR Notch filter (infinite impulse response)
- **Filter Design**: 
  - Center frequency: 1000Hz (noise frequency)
  - Quality factor: 30 (controls filter bandwidth)
- **Application**: Used `filtfilt()` for zero-phase filtering

## 📊 Results
The notch filter successfully:
- Removed the 1000Hz buzz noise
- Preserved the speech signal containing the hidden word
- Made the previously masked word clearly audible

## 🎯 Key Insight
The buzz noise was a single-frequency interference, making a notch filter the ideal choice as it surgically removes only the problematic frequency while leaving other frequencies intact.

## 🔧 How to Use
1. Place noisy audio in `data/raw/noisy_audio.wav`
2. Run `python filter_audio.py`
3. Listen to `data/processed/cleaned_audio.wav` for the revealed word