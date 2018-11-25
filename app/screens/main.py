from screens.base_screen import BaseScreen
from ui import colours
from ui.widgets.lcars_widgets import LcarsButton


class ActionButton(LcarsButton):

    def __init__(self, colour, pos, text, handler=None, rectSize=None):
        super().__init__(colour, pos, text, handler, rectSize)
        self.action = None


class ScreenMain(BaseScreen):

    def __init__(self, app):
        super().__init__(app, "assets/lcars_screen_1.png", "HOME")

    def lights_handler(self, item, event, clock):
        from screens.lighting import ScreenLightGroups
        self.loadScreen(ScreenLightGroups(self.app))

    def self_destruct(self, item, event, clock):
        from screens.destruct import ScreenDestruct
        self.loadScreen(ScreenDestruct(self.app))

    def setup(self, all_sprites):
        super().setup(all_sprites)

        actions = {
            'lights': self.lights_handler,
        }

        x_orig = 127
        y_orig = 107
        padding = 20
        width = 122
        height = 44
        row = 0
        col = 0

        for key in actions:
            action = actions[key]
            x = x_orig + (col * (width + padding / 2))
            y = y_orig + (row * (height + padding / 2))
            button = ActionButton(colours.GREY_BLUE, (y, x), key.upper(), action)
            col = col + 1
            if col > 4:
                row = row + 1
                col = 0

            all_sprites.add(button)
