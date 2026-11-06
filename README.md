# Text to Speech Converter

A simple offline text-to-speech application using the `pyttsx3` library. Works with Windows, macOS, and Linux.

## Features

- Convert text to speech
- Save speech as WAV files
- Interactive GUI mode
- Command-line interface with voice, rate, and volume options
- Support for multiple voices

## Installation

Install the required dependencies:

```bash
pip install pyttsx3
```

## Usage

### Command Line Interface

```bash
# Speak text directly
python tts.py "Hello, world!"

# Read from file and save to output
python tts.py -i input.txt -o output.wav

# List available voices
python tts.py --list-voices

# Interactive GUI mode
python tts.py --interactive

# Customize voice, rate, and volume
python tts.py -v 1 -r 200 -o speech.wav "Welcome to text-to-speech!"

# Arguments:
# -t, --text          Text to convert to speech
# -i, --input-file    Read text from a file
# -o, --output-file   Save speech to a file
# -v, --voice         Voice index (use --list-voices)
# -r, --rate          Speaking rate in words per minute (50-300, default 200)
# --volume           Volume (0.0 to 1.0, default 1.0)
# --list-voices      List available voices
# --interactive      Interactive GUI mode
```

### Interactive GUI

Run the GUI mode:

```bash
python tts.py --interactive
```

In the GUI:
- Enter text in the text box
- Click "🔊 Speak" to listen
- Check "Save to file" to save as WAV

## Available Voices

On Windows, you might see voices like:
- Microsoft David Desktop - English (United States)
- Microsoft Zira Desktop - English (United States)

Run `python tts.py --list-voices` to see what's available on your system.

## Project Structure

```
omniroute/
├── tts.py          # Main script
└── README.md       # This file
```

## License

This project is open source and available for use.