"""
Text to Speech (TTS) Converter
Uses pyttsx3 library for offline text-to-speech conversion.
Install: pip install pyttsx3
"""

import pyttsx3
import argparse
import os
import tkinter as tk
from tkinter import filedialog, messagebox

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self._available_voices = None

    def say(self, text):
        """Convert text to speech and speak it."""
        if not text or not text.strip():
            print("No text provided to speak.")
            return

        try:
            print(f"Speaking: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
            return True
        except Exception as e:
            print(f"Error during speech synthesis: {e}")
            return False

    def cleanup(self):
        """Cleanup the TTS engine."""
        try:
            self.engine.stop()
            self.engine = None
        except:
            pass

    def save_to_file(self, text, output_path):
        """Convert text to speech and save to a file."""
        if not text or not text.strip():
            print("No text provided to save.")
            return False

        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)

            print(f"Saving to: {output_path}")
            self.engine.save_to_file(text, output_path)
            self.engine.runAndWait()
            print("File saved successfully.")
            return True
        except Exception as e:
            print(f"Error saving to file: {e}")
            return False

    def set_rate(self, rate):
        """Set the speaking rate (words per minute). Default is usually 200, range: 50-300."""
        try:
            self.engine.setProperty('rate', rate)
            print(f"Speech rate set to {rate} WPM")
        except Exception as e:
            print(f"Error setting rate: {e}")

    def set_volume(self, volume):
        """Set the volume (0.0 to 1.0). Default is usually 1.0."""
        try:
            if not 0 <= volume <= 1:
                print("Volume must be between 0.0 and 1.0")
                return

            self.engine.setProperty('volume', volume)
            print(f"Volume set to {volume}")
        except Exception as e:
            print(f"Error setting volume: {e}")

    def get_available_voices(self):
        """Get available voices."""
        if self._available_voices is None:
            self._available_voices = self.engine.getProperty('voices')

        voices = []
        for idx, voice in enumerate(self._available_voices):
            voices.append({
                'index': idx,
                'name': voice.name,
                'id': voice.id
            })

        return voices

    def set_voice(self, voice_index):
        """Set the voice by index."""
        try:
            voices = self.get_available_voices()
            if voice_index < 0 or voice_index >= len(voices):
                print(f"Invalid voice index. Available voices: {len(voices)}")
                return False

            self.engine.setProperty('voice', voices[voice_index]['id'])
            print(f"Voice set to: {voices[voice_index]['name']}")
            return True
        except Exception as e:
            print(f"Error setting voice: {e}")
            return False

    def print_voices(self):
        """Print all available voices."""
        voices = self.get_available_voices()
        if not voices:
            print("No voices available.")
            return

        print("\nAvailable voices:")
        for idx, voice in enumerate(voices):
            print(f"  [{idx}] {voice['name']}")


def main():
    parser = argparse.ArgumentParser(
        description='Text to Speech Converter',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Hello, world!"
  %(prog)s -i input.txt -o output.wav
  %(prog)s -v 1 -r 200 "This is faster at 200 WPM"
  %(prog)s --list-voices
  %(prog)s --interactive
        """
    )

    parser.add_argument('text', nargs='?', help='Text to convert to speech')
    parser.add_argument('-i', '--input-file', help='Read text from a file')
    parser.add_argument('-o', '--output-file', help='Save speech to a file')
    parser.add_argument('-v', '--voice', type=int, help='Voice index to use (use --list-voices)')
    parser.add_argument('-r', '--rate', type=int, help='Speaking rate in words per minute (default: 200, range: 50-300)')
    parser.add_argument('--volume', type=float, help='Volume (0.0 to 1.0, default: 1.0)')
    parser.add_argument('--list-voices', action='store_true', help='List available voices and exit')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive mode with a GUI')

    args = parser.parse_args()

    # Initialize TTS engine
    tts = TextToSpeech()

    # List voices if requested
    if args.list_voices:
        tts.print_voices()
        return 0

    # Get text content
    if not args.text:
        if args.input_file:
            try:
                with open(args.input_file, 'r', encoding='utf-8') as f:
                    args.text = f.read()
            except Exception as e:
                print(f"Error reading input file: {e}")
                return 1
        else:
            # Interactive GUI mode
            run_gui(tts, args.voice, args.rate, args.volume)
            return 0

    # Apply voice, rate, volume if specified
    if args.voice is not None:
        tts.set_voice(args.voice)

    if args.rate is not None:
        tts.set_rate(args.rate)

    if args.volume is not None:
        tts.set_volume(args.volume)

    # Output mode
    if args.output_file:
        tts.save_to_file(args.text, args.output_file)
    else:
        tts.say(args.text)

    return 0


def run_gui(tts, voice=None, rate=None, volume=None):
    """Run an interactive GUI using tkinter."""
    root = tk.Tk()
    root.title("Text to Speech Converter")

    def speak():
        text = text_box.get('1.0', tk.END).strip()
        if text:
            tts.say(text)
            if save_checkbox.get():
                filename = filedialog.asksaveasfilename(
                    defaultextension=".wav",
                    filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
                )
                if filename:
                    tts.save_to_file(text, filename)

    text_box = tk.Text(root, wrap=tk.WORD, font=('Arial', 12), width=50, height=15)
    text_box.pack(padx=20, pady=20)

    # Apply settings passed from main()
    if voice is not None:
        tts.set_voice(voice)

    if rate is not None:
        tts.set_rate(rate)

    if volume is not None:
        tts.set_volume(volume)

    speak_btn = tk.Button(root, text="🔊 Speak", command=speak, font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white')
    speak_btn.pack(pady=5)

    save_checkbox = tk.BooleanVar()
    save_checkbox.set(True)
    tk.Checkbutton(root, text="Save to file", variable=save_checkbox).pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    import sys
    sys.exit(main())