import logging
import sys
import time

import speech_recognition as sr
from pynput import keyboard

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)-8s - %(name)s:%(filename)s:%(lineno)d - %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)


class SpeechToKeyboard:
    """The `SpeechToKeyboard` class wraps a microphone audio source, a speech recognizer object, a keyboard controller,
    and a keyboard listener. On instantiation, all four previously mentioned resources are initialized.

    * The speech recognizer is initialized.

    * The microphone audio source is initialized and adjusted for ambient noise.

    * The keyboard listener is configured to listen for certain hotkeys. These hotkeys when activated will trigger a
    callback function.

    **  `<shift>+<tab>`: The most basic command, this will toggle audio recording on/off. When turned on, the microphone will
        capture utterances until a certain break in speech is detected. When a break is detected, the
        `audio_recognizer_callback()` callback function is called with the captured audio data. These settings can be
        further configured in the speech recognizer resource.

    **  ``: Stop the keyboard listener. This will effectively end the program since the thread cannot be resumed
        later, requiring a new instance to be instantiated.

    * The keyboard controller is initialized and called as part of the `audio_recognizer_callback()` function. This
    callback converts the speech to text and parses the text into keyboard controller commands. For the moment,
    punctuation and special characters are not supported but adding an escape utterance and proper processing of the
    text before feeding to the keyboard controller would allow additional functionality

    """
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.keyboard_controller = keyboard.Controller()
        self.keyboard_listener = keyboard.GlobalHotKeys(
            {'<shift>+<tab>': self.toggle_recording,
             '<shift>+<cmd>': self.stop_keyboard_listener}
        )
        self.is_recording = False

        with self.microphone as source:
            logger.info("calibrating...")
            self.recognizer.adjust_for_ambient_noise(source)

        # callback function for the audio listener thread
        self.stop_recording_callback = None
        # start the keyboard listener thread
        self.keyboard_listener.start()

    def toggle_recording(self):
        if self.is_recording and self.stop_recording_callback is not None:
            logger.info("stop recording hotkey activated")
            self.stop_recording_callback(wait_for_stop=False)
        else:
            logger.info("start recording hotkey activated")
            self.stop_recording_callback = self.recognizer.listen_in_background(
                self.microphone, self.audio_recognizer_callback
            )
        self.is_recording = not self.is_recording

    def stop_keyboard_listener(self):
        logger.info("stop keyboard listener")
        if self.keyboard_listener is not None:
            self.keyboard_listener.stop()
            sys.exit(0)

    def audio_recognizer_callback(self, recognizer, audio):
        logger.debug("in callback")
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            data = recognizer.recognize_google(audio)
            chars = list(data)
            for c in chars:
                self.keyboard_controller.tap(c)
            logger.info("Google Speech Recognition thinks you said " + data)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(
                "Could not request results from Google Speech Recognition service; {0}".format(
                    e
                )
            )


if __name__ == "__main__":
    x = SpeechToKeyboard()
    time.sleep(1000)