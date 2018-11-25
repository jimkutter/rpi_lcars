from datetime import datetime, timedelta

import pygame

from screens.base_screen import BaseScreen
from ui.widgets.background import LcarsBackgroundImage
from ui.widgets.lcars_widgets import LcarsText


class ScreenBlank(BaseScreen):
    def __init__(self, app):
        super().__init__(app, None, None)

    def setup(self, all_sprites):
        all_sprites.add(LcarsBackgroundImage("assets/lcars_screen_blank.png"), layer=0)

    def handleEvents(self, event, fpsClock):
        if event.type == pygame.MOUSEBUTTONDOWN:
            from screens.authorize import ScreenAuthorize
            self.loadScreen(ScreenAuthorize(self.app))

        return super().handleEvents(event, fpsClock)
