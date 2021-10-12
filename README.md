# speech-to-text

## Motivation

I am a father of two little ones, one is three and half, the other is three months. The motivation behind this project stems from the fact that my wife and I both work remote and are currently juggling watching the three month old and working. He demands to be held all the time so it makes replying to emails, slack messages, and google searching more difficult. Obviously, I do not intend to use this tool to actually write/edit code, but it should allow easier 1-handed interactions with a computer

## Requirements

This is only tested on python 3.9 with the requirements file provided.

You will need `PyAudio` which requires `portaudio`. See [here](http://people.csail.mit.edu/hubert/pyaudio/) for pyaudio installation instructions

## Installation

No fancy `setup.py` or other package installation yet. Just clone the repo and run main.py

```shell
git clone https://github.com/myz540/speech-to-text.git
cd speech-to-text
# make sure you install `portaudio` before this next part
pip install -r requirements.txt
python speech_to_text/main.py
```

Obviously, the current hotkey setup is no good since you will pollute your desired keyboard inputs with the commands to the keyboard listener...