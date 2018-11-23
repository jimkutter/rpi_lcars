import json

from screens.authorize import ScreenAuthorize
from screens.register_hue import ScreenRegister
from ui.ui import UserInterface

# global config
UI_PLACEMENT_MODE = True
RESOLUTION = (800, 480)
FPS = 60
DEV_MODE = True


class App(object):
    def __init__(self):
        self.firstScreen = ScreenAuthorize(self)

        self.config = {}

    def run(self):
        with open('config.json') as json_data_file:
            self.config = json.load(json_data_file)

        ui = UserInterface(self.firstScreen, RESOLUTION, UI_PLACEMENT_MODE, FPS, DEV_MODE)

        while True:
            ui.tick()


if __name__ == "__main__":
    app = App()
    app.run()
