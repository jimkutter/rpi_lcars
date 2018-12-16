from datetime import datetime, timedelta

import pygame
from pygame.mixer import Sound

from screens.base_screen import BaseScreen
from ui import colours
from ui.widgets.background import LcarsBackgroundImage
from ui.widgets.gifimage import LcarsGifImage
from ui.widgets.lcars_widgets import LcarsButton
from ui.widgets.lcars_widgets import LcarsText


class CodeButton(LcarsButton):

    def __init__(self, colour, pos, text, handler=None, rectSize=None):
        super().__init__(colour, pos, text, handler, rectSize)
        self.code = None


class ScreenAuthorize(BaseScreen):

    def __init__(self, app):
        super().__init__(app, None, None)
        self.login_timeout = None
        self.reset_timer()

    def setup(self, all_sprites):
        all_sprites.add(LcarsBackgroundImage("assets/lcars_screen_2.png"), layer=0)

        all_sprites.add(LcarsGifImage("assets/gadgets/stlogorotating.gif", (103, 369), 50), layer=0)

        all_sprites.add(LcarsText(colours.ORANGE, (270, -1), "AUTHORIZATION REQUIRED", 2), layer=0)

        all_sprites.add(LcarsText(colours.BLUE, (330, -1), "ONLY AUTHORIZED PERSONNEL MAY ACCESS THIS TERMINAL", 1.5),
                        layer=1)

        all_sprites.add(LcarsText(colours.BLUE, (360, -1), "TOUCH TERMINAL TO PROCEED", 1.5), layer=1)

        greek_alphabet = [
            "alpha",
            "beta",
            "gamma",
            "delta",
            "epsilon",
            "zeta",
            "eta",
            "theta",
            "iota",
            "kappa",
            "lambda",
            "mu",
            "nu",
            "xi",
            "omicron",
            "pi",
            "rho",
            "sigma",
            "tau",
            "upsilon",
            "phi",
            "chi",
            "psi",
            "omega",
        ]

        x_orig = 127
        y_orig = 75
        padding = 20
        width = 122
        height = 44
        row = 0
        col = 0
        for letter in greek_alphabet:
            x = x_orig + (col * (width + padding / 2))
            y = y_orig + (row * (height + padding / 2))
            button = CodeButton(colours.GREY_BLUE, (y, x), letter.upper(), self.button_handler)
            button.code = letter
            col = col + 1
            if col > 3:
                row = row + 1
                col = 0

            all_sprites.add(button, layer=2)

        self.layer1 = all_sprites.get_sprites_from_layer(1)
        self.layer2 = all_sprites.get_sprites_from_layer(2)

        # sounds
        if not self.app.is_screen_off:
            Sound("assets/audio/panel/215.wav").play()

        self.sound_granted = Sound("assets/audio/accessing.wav")
        self.sound_beep1 = Sound("assets/audio/panel/201.wav")
        self.sound_denied = Sound("assets/audio/access_denied.wav")
        self.sound_deny1 = Sound("assets/audio/deny_1.wav")
        self.sound_deny2 = Sound("assets/audio/deny_2.wav")

        ############
        # SET PIN CODE WITH THIS VARIABLE
        ############
        self.pin = self.app.config['pin']
        ############
        self.reset()

    def reset(self):
        # Variables for PIN code verification
        self.correct = 0
        self.pin_i = 0
        self.granted = False
        for sprite in self.layer1: sprite.visible = True
        for sprite in self.layer2: sprite.visible = False

    def screen_update(self):
        super().screen_update()

        if self.login_timeout:
            auth_delta = self.login_timeout - datetime.now()
            if int(auth_delta.total_seconds()) == 0:
                self.reset()

    def handleEvents(self, event, fpsClock):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Play sound
            self.sound_beep1.play()
            self.app.screen_on()

        if event.type == pygame.MOUSEBUTTONUP:
            if not self.layer2[0].visible:
                self.show_login_controls()
            elif self.pin_i == len(self.pin):
                # Ran out of button presses
                if self.correct == len(self.pin):
                    self.sound_granted.play()
                    from screens.main import ScreenMain
                    self.loadScreen(ScreenMain(self.app))
                else:
                    self.sound_deny2.play()
                    self.sound_denied.play()
                    self.reset()

        return False

    def show_login_controls(self):
        for sprite in self.layer1: sprite.visible = False
        for sprite in self.layer2: sprite.visible = True
        Sound("assets/audio/enter_authorization_code.wav").play()
        self.reset_timer()

    def button_handler(self, item, event, clock):
        self.reset_timer()
        if self.pin[self.pin_i] == item.code:
            self.correct += 1
            print(self.correct)

        self.pin_i += 1

    def reset_timer(self):
        self.login_timeout = datetime.now() + timedelta(seconds=self.app.config['login_timeout'])
