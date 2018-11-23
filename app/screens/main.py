from screens.base_screen import BaseScreen
from ui import colours
from ui.widgets.lcars_widgets import LcarsButton


class ScreenMain(BaseScreen):

    def __init__(self, app):
        super().__init__(app, "assets/lcars_screen_1.png", "HOME")

    def setup(self, all_sprites):
        super().setup(all_sprites)

        all_sprites.add(LcarsButton(colours.BEIGE, (107, 127), "LIGHTS", self.lights_handler),
                        layer=4)

    def lights_handler(self, item, event, clock):
        from screens.lighting import ScreenLightGroups
        self.loadScreen(ScreenLightGroups(self.app))
