import json

from ui.ui import UserInterface

# global config
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

    def run(self):
        ui = UserInterface(self.firstScreen, RESOLUTION, UI_PLACEMENT_MODE, FPS, DEV_MODE)

        while True:
            ui.tick()


if __name__ == "__main__":
    app = App()
    app.run()
