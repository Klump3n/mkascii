#!/usr/bin/env python3
"""
The curses window.

"""
import aalib
import curses

from PIL import Image, ImageOps


class Window(object):
    """
    The curses window.

    """
    def __init__(self, image_path):

        self._image_path = image_path

        self._menu_selection = 0
        self._menu = {
            "brightness": {
                "name": "Brightness",
                "value": 20,
                "min": -255,
                "max":  255,
                "placement": 0
            },
            "contrast": {
                "name": "Contrast",
                "value": 20,
                "min": -255,
                "max":  255,
                "placement": 1
            },
            "gamma": {
                "name": "Gamma",
                "value": 255,
                "min": 0,
                "max": 512,
                "placement": 2
            },
            "dithering": {
                "name": "Dithering",
                "value": 0,
                "min": 0,
                "max": 2,
                "options": [
                    "DITHER_NONE", "DITHER_ERROR_DISTRIBUTION", "DITHER_FLOYD_STEINBERG"
                ],
                "placement": 3
            },
            "invert": {
                "name": "Invert",
                "value": 0,
                "min": 0,
                "max": 1,
                "options": [
                    "False", "True"
                ],
                "placement": 4
            }
        }
        self._menu_entries = []
        for i in range(len(self._menu.keys())):
            for key, value in self._menu.items():
                if value["placement"] == i:
                    self._menu_entries.append(key)

        self._num_menu_entries = len(self._menu.keys())

        self._img_width = 80
        self._img_height = 15

        self._load_image()
        curses.wrapper(self._mainscr)

    def _load_image(self):
        """
        Load and return the image to be rendered.

        """
        try:
            with open(self._image_path, "rb") as img_binary:
                image = Image.open(img_binary).convert('L')
                image = ImageOps.invert(image)
        except (FileNotFoundError, OSError) as e:
            sys.exit("Exception: {}".format(e))

        self._image = image

    def _render_img(self):
        """
        Return the rendered image.

        """
        screen = aalib.AsciiScreen(width=self._img_width, height=self._img_height)
        image = self._image.resize(screen.virtual_size)
        screen.put_image((0, 0), image)

        menu_contrast = self._menu["contrast"]["value"]
        menu_brightness = self._menu["brightness"]["value"]
        menu_gamma = self._menu["gamma"]["value"]
        menu_dithering = self._menu["dithering"]["value"]
        menu_invert = self._menu["invert"]["value"]

        return screen.render(
            contrast=menu_contrast,
            brightness=menu_brightness,
            gamma=menu_gamma/255,
            dithering_mode=menu_dithering,
            inversion=menu_invert
        )

    def _menu_state(self, key):
        """
        Update the state of the menu based on the key input.

        """
        self._num_menu_entries

        if key == curses.KEY_DOWN:
            if self._menu_selection >= (self._num_menu_entries - 1):
                pass
            else:
                self._menu_selection += 1
            return

        if key == curses.KEY_UP:
            if self._menu_selection <= 0:
                pass
            else:
                self._menu_selection -= 1
            return

        menu_entry = self._menu_entries[self._menu_selection]
        value = self._menu[menu_entry]["value"]
        min_val = self._menu[menu_entry]["min"]
        max_val = self._menu[menu_entry]["max"]

        if key == curses.KEY_LEFT:
            new_val = self._menu[menu_entry]["value"] - 1
            if new_val < min_val:
                pass
            else:
                self._menu[menu_entry]["value"] = new_val

        if key == curses.KEY_RIGHT:
            new_val = self._menu[menu_entry]["value"] + 1
            if new_val > max_val:
                pass
            else:
                self._menu[menu_entry]["value"] = new_val

    def _mainscr(self, stdscr):
        """
        Curses main screen.

        """
        # Clear screen
        stdscr.clear()

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        self._height = curses.LINES - 1
        self._width = curses.COLS - 1

        self._command_window = curses.newwin(7, self._width, 0, 0)
        self._output_window = curses.newwin(self._height - 7, self._width, 7, 0)
        self._command_window.keypad(1)
        headline = "Displaying {} [press q to quit]".format(self._image_path)

        while True:

            self._command_window.clear()
            self._output_window.clear()

            self._command_window.addstr(0, 1, headline)
            self._command_window.hline(1, 1, "=", len(headline))

            for menu_key, menu_value in self._menu.items():
                offset = menu_value["placement"]
                name = menu_value["name"]
                value = menu_value["value"]
                try:
                    options = menu_value["options"]
                    value = options[value]
                except KeyError:
                    pass
                if offset == self._menu_selection:
                    self._command_window.addstr(2+offset, 1, "{}: {}".format(name, value), curses.color_pair(1))
                else:
                    self._command_window.addstr(2+offset, 1, "{}: {}".format(name, value))

            img = self._render_img()

            self._output_window.addstr(img)

            self._command_window.move(2+self._menu_selection, 0)

            self._output_window.refresh()
            self._command_window.refresh()

            key = self._command_window.getch()

            # if q we exit, else we update the menu
            if key == ord("q"):
                break
            else:
                self._menu_state(key)
