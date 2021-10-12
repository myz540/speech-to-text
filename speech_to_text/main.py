import logging
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


class AudioRecorder:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.keyboard_controller = keyboard.Controller()
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release
        )
        self.hotkey = keyboard.HotKey(keys=keyboard.HotKey.parse('<ctrl>+<alt>+h'), on_activate=self.on_activate)

        self.is_recording = False

        with self.microphone as source:
            logger.info("calibrating...")
            self.recognizer.adjust_for_ambient_noise(source)

        self.keyboard_listener.start()

    def on_activate(self):
        print("HotKey activated!")

    def callback(self, recognizer, audio):
        logger.debug("in callback")
        # received audio data, now we'll recognize it using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            data = recognizer.recognize_google(audio)
            chars = list(data)
            for c in chars:
                self.keyboard_controller.press(c)
            logger.info("Google Speech Recognition thinks you said " + data)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(
                "Could not request results from Google Speech Recognition service; {0}".format(
                    e
                )
            )

    def on_press(self, key):
        logger.info(f"pressed {key}")
        if key == keyboard.Key.cmd or key == keyboard.Key.cmd_r:
            if not self.is_recording:
                self.is_recording = True
                logger.info("starting audio listener")
                self.stop_listening = self.recognizer.listen_in_background(
                    self.microphone, self.callback
                )
            else:
                self.is_recording = False
                logger.info("stopping audio listener")
                self.stop_listening(wait_for_stop=False)

    def on_release(self, key):
        if key == keyboard.Key.esc:
            logger.info("stopping keyboard listener")
            return False


if __name__ == "__main__":
    logger.error("HERE")
    x = AudioRecorder()
    time.sleep(100)