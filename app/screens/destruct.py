from datetime import datetime, timedelta

import pygame

from screens.base_screen import BaseScreen
from ui.widgets.gifimage import LcarsGifImage
from ui.widgets.lcars_widgets import LcarsText


class ScreenDestruct(BaseScreen):
    def __init__(self, app):
        super().__init__(app, "assets/lcars_screen_destruct.png", "AUTO DESTRUCT")
        self.timer = None
        self.delta = None
        self.timeout = datetime.now() + timedelta(seconds=self.app.config['destruct_timeout'])
        self.crack = None

    def setup(self, all_sprites):
        super().setup(all_sprites)

        self.timer = LcarsText((77, 19, 22), (180, 280), "00:00:00", 7.0)
        all_sprites.add(self.timer, layer=1)

        self.crack = LcarsGifImage("assets/glass-fast.gif", (0, 0), 50)
        self.crack.pause()
        self.crack.visible = False

        all_sprites.add(self.crack, layer=5)

        self.update_timer()

    def screen_update(self):
        super().screen_update()
        self.update_timer()

        if int(self.delta.total_seconds()) == 0:
            if not self.crack.visible:
                self.crack.play()
                self.crack.visible = True

        if int(self.delta.total_seconds()) == -1:
            from screens.authorize import ScreenAuthorize
            self.loadScreen(ScreenAuthorize(self.app))
            from pygame.event import Event
            pygame.event.post(Event(pygame.USEREVENT))

    def update_timer(self):
        self.delta = self.timeout - datetime.now()
        seconds = self.delta.seconds
        # hours
        hours = seconds // 3600
        # remaining seconds
        seconds = seconds - (hours * 3600)
        # minutes
        minutes = seconds // 60
        # remaining seconds
        seconds = seconds - (minutes * 60)
        # total time
        if not self.crack.visible:
            self.timer.setText('{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds)))
