from datetime import datetime

import pygame
from pygame.mixer import Sound

from datasources.network import get_ip_address_string
from ui import colours
from ui.widgets.background import LcarsBackgroundImage
from ui.widgets.lcars_widgets import LcarsText, LcarsButton, LcarsBlockMedium
from ui.widgets.screen import LcarsScreen


class BaseScreen(LcarsScreen):
    def __init__(self, app, background, title):
        super().__init__()
        self.app = app
        self.background = background
        self.title = title
        self.last_clock_update = 0
        self.ip_address = None
        self.beep1 = None
        self.stardate = None

    def setup(self, all_sprites):
        all_sprites.add(LcarsBackgroundImage(self.background), layer=0)
        # panel text
        all_sprites.add(LcarsText(colours.BLACK, (15, 35), self.app.config['version']), layer=1)
        all_sprites.add(LcarsText(colours.ORANGE, (5, 135), self.title, 2), layer=1)

        self.ip_address = LcarsText(colours.BLACK, (444, 520), get_ip_address_string())
        all_sprites.add(self.ip_address, layer=1)

        # date display
        self.stardate = LcarsText(colours.BLUE, (12, 380), "STAR DATE 2711.05 17:54:32", 1.5)

        all_sprites.add(self.stardate, layer=1)

        # buttons
        all_sprites.add(LcarsButton(colours.RED_BROWN, (6, 662), "LOGOUT", self.logout_handler),
                        layer=4)

        self.beep1 = Sound("assets/audio/panel/201.wav")
        Sound("assets/audio/panel/220.wav").play()

    def logout_handler(self, item, event, clock):
        from screens.destruct import ScreenDestruct
        self.loadScreen(ScreenDestruct(self.app))

    def screen_update(self):
        pass

    def update(self, screenSurface, fpsClock):
        if pygame.time.get_ticks() - self.last_clock_update > 1000:
            if self.stardate is not None:
                self.stardate.setText("STAR DATE {}".format(datetime.now().strftime("%d%m.%y %H:%M:%S")))
                self.last_clock_update = pygame.time.get_ticks()

        self.screen_update()

        LcarsScreen.update(self, screenSurface, fpsClock)

    def handleEvents(self, event, fpsClock):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.beep1:
                self.beep1.play()

        if event.type == pygame.MOUSEBUTTONUP:
            return False
