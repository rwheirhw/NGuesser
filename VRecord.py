import argparse
import wavio as wv
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import time


DEFAULT_SR = 44100
DEFAULT_LEN = 5


def list_devices():
    print('Available audio devices:')
    print(sd.query_devices())


def record(duration, samplerate, channels, device):
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, device=device)
    sd.wait()
    return recording


def record_with_silence_detect(samplerate, channels, device, silence_threshold=0.01, silence_duration=1.0, block_duration=0.1):
    """
    Stream from input device and stop when RMS stays below silence_threshold
    for silence_duration seconds. Returns a numpy array with recorded samples.
    """
    block_frames = max(1, int(block_duration * samplerate))
    frames = []
    silent_blocks = 0
    required_silent = max(1, int(silence_duration / block_duration))

    print(f'Starting silence-detection recording (threshold={silence_threshold}, silence_duration={silence_duration}s)')

    with sd.InputStream(samplerate=samplerate, channels=channels, device=device, blocksize=block_frames) as stream:
        try:
            while True:
                data, overflow = stream.read(block_frames)
                if overflow:
                    print('Warning: overflow occurred while recording')
                frames.append(data.copy())

                # compute RMS
                # data shape: (frames, channels)
                rms = np.sqrt(np.mean(np.square(data.astype(np.float32))))
                # print('.', end='', flush=True)
                if rms < silence_threshold:
                    silent_blocks += 1
                else:
                    silent_blocks = 0

                if silent_blocks >= required_silent:
                    # we've seen enough consecutive silent blocks
                    break
        except KeyboardInterrupt:
            print('\nRecording interrupted by user')

    if frames:
        rec = np.concatenate(frames, axis=0)
    else:
        rec = np.empty((0, channels), dtype=np.float32)
    return rec


def main():
    parser = argparse.ArgumentParser(description='Simple recorder')
    parser.add_argument('--duration', '-d', type=int, help='Recording duration in seconds')
    parser.add_argument('--outfile', '-o', type=str, default='recording0.wav', help='Output filename')
    parser.add_argument('--samplerate', '-r', type=int, default=DEFAULT_SR, help='Sample rate (Hz)')
    parser.add_argument('--channels', '-c', type=int, default=2, choices=[1, 2], help='Number of channels')
    parser.add_argument('--device', type=int, help='Input device id (use --list-devices)')
    parser.add_argument('--list-devices', action='store_true', help='List available audio devices and exit')
    parser.add_argument('--play', action='store_true', help='Play back recording after saving')
    parser.add_argument('--silence-detect', action='store_true', help='Enable auto-stop when silence detected')
    parser.add_argument('--silence-threshold', type=float, default=0.01, help='RMS threshold below which sound is considered silence')
    parser.add_argument('--silence-duration', type=float, default=1.0, help='Seconds of continuous silence to stop recording')
    parser.add_argument('--block-duration', type=float, default=0.1, help='Block size in seconds for silence checks')

    args = parser.parse_args()

    if args.list_devices:
        list_devices()
        return

    if args.duration is None and not args.silence_detect:
        try:
            user_in = input(f'How many seconds do you wanna record for? (press Enter for default {DEFAULT_LEN})\n').strip()
            if user_in == '':
                rec_len = DEFAULT_LEN
            else:
                rec_len = int(user_in)
        except Exception:
            rec_len = DEFAULT_LEN

        rec = record(rec_len, args.samplerate, args.channels, args.device)
    elif args.silence_detect:
        rec = record_with_silence_detect(args.samplerate, args.channels, args.device,
                                         silence_threshold=args.silence_threshold,
                                         silence_duration=args.silence_duration,
                                         block_duration=args.block_duration)
    else:
        rec = record(args.duration, args.samplerate, args.channels, args.device)

    # save files
    try:
        write(args.outfile, args.samplerate, rec)
    except Exception as e:
        print(f'Error saving {args.outfile}: {e}')

    alt_out = 'recording1.wav'
    try:
        wv.write(alt_out, rec, args.samplerate, sampwidth=2)
    except Exception as e:
        print(f'Error saving {alt_out}: {e}')

    if args.play:
        try:
            sd.play(rec, args.samplerate)
            sd.wait()
        except Exception as e:
            print(f'Error during playback: {e}')


if __name__ == '__main__':
    main()