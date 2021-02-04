from time import sleep
from gtts import gTTS
from os import getcwd
import pygame
from pygame import mixer
from threading import Thread, currentThread
import re


class PlaySound:
    def __init__(self):
        # 44100
        mixer.init(frequency=24000, size=-16, channels=2, buffer=4096)
        self.isMorse = None

        self.codeSounds = {
            ".": getcwd() + "/audio/dot.ogg",
            "-": getcwd() + "/audio/dash.ogg",
            " ": getcwd() + "/audio/short_silence.ogg",
            "/": getcwd() + "/audio/long_silence.ogg",
        }

        self.code = ""

    def restart_mixer(self):
        """ In case we want to set another frequency """
        mixer.quit()
        mixer.init(frequency=24000, size=-16, channels=2, buffer=4096)
        mixer.music.set_volume(0.5)

    def setCode(self, code: "str[]") -> None:
        """ Set the appropiate string as the code to read """

        if re.search("[a-zA-Z]+", code):
            self.code = code
            self.makeTTS()
            self.isMorse = False
            return
        else:
            self.isMorse = True

        self.code = [x for x in code][::-1]

    def makeTTS(self):
        """ Make TTS file """
        tts = gTTS(text=self.code, lang="en")
        tts.save(getcwd() + "/audio/tts.mp3")

    def play(self) -> None:
        """ Play the morse code sounds in the storaged string """

        mixer.stop()

        def _threadedPlay(self):
            """ Plays TTS or morse code """

            if self.isMorse is False:
                try:
                    mixer.music.load(getcwd() + "/audio/tts.mp3")
                    mixer.music.play()
                except Exception as e:
                    print("Couldn't play tts.mp3", e)

                return

            mixer.music.load(self.codeSounds.get(self.code.pop()))

            for i in self.code:
                try:
                    mixer.music.queue(self.codeSounds.get(i))
                    mixer.music.play()

                except:  # pygame.error
                    sleep(1)

                sleep(0.4)

        isPlaying = Thread(target=lambda: _threadedPlay(self))

        if isPlaying.is_alive() is True:
            isPlaying.do_run = False

        isPlaying.start()
