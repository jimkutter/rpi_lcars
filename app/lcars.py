import json
import rpi_backlight as bl

from ui.ui import UserInterface

# global config
from ui.widgets.background import LcarsBackgroundImage
from ui.widgets.gifimage import LcarsGifImage

UI_PLACEMENT_MODE = True
RESOLUTION = (800, 480)
FPS = 60
DEV_MODE = True


class App(object):
    def __init__(self):
        self.config = {}
        with open('config.json') as json_data_file:
            self.config = json.load(json_data_file)

        from screens.authorize import ScreenAuthorize
        self.firstScreen = ScreenAuthorize(self)

        self.assets = {}

    def run(self):
        ui = UserInterface(self.firstScreen, RESOLUTION, UI_PLACEMENT_MODE, FPS, DEV_MODE)

        self.load_assets()

        while True:
            ui.tick()

    def screen_off(self):
        bl.set_power(False)

    def screen_on(self):
        bl.set_power(True)

    def load_assets(self):
        self.assets['assets/lcars_screen_1.png'] = LcarsBackgroundImage('assets/lcars_screen_1.png')
        self.assets['assets/lcars_screen_1b.png'] = LcarsBackgroundImage('assets/lcars_screen_1b.png')
        self.assets['assets/lcars_screen_2.png'] = LcarsBackgroundImage('assets/lcars_screen_2.png')
        self.assets['assets/lcars_screen_blank.png'] = LcarsBackgroundImage('assets/lcars_screen_blank.png')
        self.assets['assets/lcars_screen_destruct.png'] = LcarsBackgroundImage('assets/lcars_screen_destruct.png')
        self.assets['assets/glass-fast.gif'] = LcarsGifImage("assets/glass-fast.gif", (0, 0), 50)


if __name__ == "__main__":
    app = App()
    app.run()
