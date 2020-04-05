####################################
# Copyright (C) 2018 Michele Curci #
####################################

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
#encrypt
from itertools import cycle, zip_longest as zip

import base64


class CryptoScreen(GridLayout):

    def __init__(self, **kwargs):
        super(CryptoScreen, self).__init__(**kwargs)

        self.cols = 2
        self.rows = 4

        self.add_widget(Label(text='Original', size_hint = [0.2, 0.4], font_size= '30', color=[160/255, 229/255, 0, 1]))
        self.original = TextInput(multiline=True, size_hint = [0.8, 0.4])
        self.add_widget(self.original)

        self.add_widget(Label(text='Encrypted', size_hint = [0.2, 0.4], font_size= '30', color=[160/255, 229/255, 0, 1]))
        self.encrypted = TextInput(multiline=True, size_hint = [0.8, 0.4])
        self.add_widget(self.encrypted)

        self.add_widget(Label(text='KEY', size_hint = [0.2, 0.4], font_size= '30', color=[1, 191/255, 0, 1]))
        self.key = TextInput(multiline=False, size_hint = [0.8, 0.4])
        self.add_widget(self.key)

        self.add_widget(Label(text='', size_hint=[0.2, 0.2]))

        self.butt = Button(text="Encrypt", font_size= '30', color=[1, 0, 54/255, 1], background_color=[0, 102/255, 204/255, 1])
        self.butt.bind(on_press= self.encode, )

        self.butt2 = Button(text="Decrypt",  font_size= '30', color=[1, 0, 54/255, 1], background_color=[0, 102/255, 204/255, 1])
        self.butt2.bind(on_press=self.decode)

        layout = GridLayout(cols=2)
        layout.size_hint = [0.8, 0.3]
        layout.add_widget(self.butt)
        layout.add_widget(self.butt2)

        self.add_widget(layout)




    def encode(self, instance):

        message = self.original.text
        key = self.key.text

        exit = False
        if message == "":
            self.original.text = ">>> THIS FIELD CAN'T BE EMPTY FOR ENCRYPTION <<<"
            exit = True

        if key == "":
            self.key.text = ">>> THIS FIELD CAN'T BE EMPTY FOR ENCRYPTION AND DECRYPTION <<<"
            exit = True

        if exit:
            return

        len_message = len(message)
        calc_key = key

        while (len(calc_key) < len_message):
            calc_key += key

        calc_key = calc_key[:len_message]
        cyphered = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(message, calc_key))


        # Standard Base64 Encoding
        encodedBytes = base64.b64encode(cyphered.encode("ascii"))
        cyphered_plus_base64 = str(encodedBytes, "ascii")

        self.encrypted.text = cyphered_plus_base64

    def decode(self, instance):

        cyphered_base64 = self.encrypted.text

        cyphered = str(base64.b64decode(cyphered_base64.encode("ascii")), "ascii")

        key = self.key.text

        len_message = len(cyphered)
        calc_key = key

        while (len(calc_key) < len_message):
            calc_key += key

        calc_key = calc_key[:len_message]
        message = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(cyphered, calc_key))
        self.original.text = message

class MyApp(App):

    def build(self):
        self.title = "XOR PyCrypt"
        return CryptoScreen()


if __name__ == '__main__':
    MyApp().run()