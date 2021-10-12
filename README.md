# speech-to-text

## Motivation

I am a father of two little ones, one is three and half, the other is three months. The motivation behind this project stems from the fact that my wife and I both work remote and are currently juggling watching the three month old and working. He demands to be held all the time so it makes replying to emails, slack messages, and google searching more difficult. Obviously, I do not intend to use this tool to actually write/edit code, but it should allow easier 1-handed interactions with a computer

## Requirements

This is only tested on python 3.9 with the requirements file provided.

You will need `PyAudio` which requires `portaudio`. See [here](http://people.csail.mit.edu/hubert/pyaudio/) for pyaudio installation instructions

You will likely be prompted for system permissions to control and listen to the keyboard, as well as usage of the microphone

This probably only works on Macs at the moment as I have not tested this on another OS. It seems there are some interoperability issues with the different keyboard keys and their mappings

## Installation

No fancy `setup.py` or other package installation yet. Just clone the repo and run main.py

```shell
git clone https://github.com/myz540/speech-to-text.git
cd speech-to-text
# make sure you install `portaudio` before this next part
pip install -r requirements.txt
python speech_to_text/main.py
```

## Usage

Once the program is running, you can move your mouse cursor to where you want text to be input, then hit `<shift>+<tab>`. This hotkey will start the microphone recording. Now you are free to start talking, when a break in the utterances is detected, the text will be input where the cursor is. At this point, you can either continue with more utterances, or stop the recording with `<shift>+<tab>` again. NOTE: After stopping the audio listener thread, it can take 2-3 seconds for the thread to fully die. Since it is context managed, if you try to start recording again immediately, it will fail. There is probably a workaround that involves spawning new audio and speech recognition resources each time but I haven't explored it. To stop the listener and end the program, hit `<shift>+<cmd>+x` to stop the keyboard listener and exit the program. 

**WARNING** If whatever program is in the foreground has a command for `<shift>+<cmd>+x`, it will be executed!