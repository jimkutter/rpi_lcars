from screens.base_screen import BaseScreen
from ui.widgets.lcars_widgets import *


class ScreenRegister(BaseScreen):

    def __init__(self, app):
        super().__init__(app, "assets/lcars_screen_1.png", "REGISTER HUE")

    def setup(self, all_sprites):
        super().setup(all_sprites)

        # info text
        all_sprites.add(LcarsText(colours.WHITE, (192, 174), "Push the connect button on your hue bridge.", 1.5),
                        layer=3)

        all_sprites.add(LcarsButton(colours.ORANGE, (240, 150), "ABORT", self.cancel_handler),
                        layer=4)

        all_sprites.add(LcarsButton(colours.BLUE, (240, 450), "CONFIRM", self.ok_handler),
                        layer=4)

    def cancel_handler(self, item, event, clock):
        from screens.main import ScreenMain
        self.loadScreen(ScreenMain(self.app))

    def ok_handler(self, item, event, clock):
        from screens.lighting import ScreenLightGroups
        self.loadScreen(ScreenLightGroups(self.app))
