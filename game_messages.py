import libtcodpy as libtcod

import textwrap


class Message:
    def __init__(self, text, color=libtcod.white):
        self.text = text
        self.color = color


class MessageLog:
    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height

    def add_message(self, message):
        # split message if needed
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in new_msg_lines:
            # if full buffer, remove first line to make place for new ones
            if len(self.messages) == self.height:
                del self.messages[0]

            # add the new line to message obect, with text and color
            self.messages.append(Message(line, message.color))


