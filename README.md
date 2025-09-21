VRecord.py - Simple recorder with silence detection and CLI

Overview

This small script records audio using sounddevice and saves two output WAV files (to match the original behavior):
- recording0.wav (default filename) — written with scipy.io.wavfile.write
- recording1.wav — written with wavio.write

It preserves the original interactive behavior while adding CLI flags and optional silence detection.

Dependencies

- Python 3.8+
- sounddevice
- scipy
- wavio
- numpy

Install dependencies:

```powershell
pip install sounddevice scipy wavio numpy
```

Usage

Interactive (original behavior):

```powershell
python VRecord.py
# then type duration or press Enter for default 5
```

CLI examples:

Record 3 seconds to out.wav:

```powershell
python VRecord.py --duration 3 --outfile out.wav
```

List devices:

```powershell
python VRecord.py --list-devices
```

Record until 1 second of silence is detected (RMS threshold 0.01):

```powershell
python VRecord.py --silence-detect --silence-threshold 0.01 --silence-duration 1.0
```

Record and play back:

```powershell
python VRecord.py --duration 4 --play
```

Notes

- The silence detector uses RMS over short blocks (default 0.1s) to determine silence. Adjust `--silence-threshold` and `--silence-duration` for your environment.
- If you prefer a single output format, use the `--outfile` parameter; the script still writes a second `recording1.wav` to preserve previous behavior.
- On Windows you may need to select a device using `--device <id>`; use `--list-devices` to see available devices.
