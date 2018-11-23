from phue import Bridge, PhueRegistrationException

from screens.base_screen import BaseScreen
from screens.main import ScreenMain
from ui import colours
from ui.widgets.lcars_widgets import LcarsBlockMedium, LcarsButton


class GroupButton(LcarsButton):

    def __init__(self, colour, pos, text, handler=None, rectSize=None):
        super().__init__(colour, pos, text, handler, rectSize)
        self.group_id = 0


class ScreenLightGroups(BaseScreen):

    def __init__(self, app):
        super().__init__(app, "assets/lcars_screen_1.png", "LIGHTING")
        self.bridge = None
        self.groups = {}

    def setup(self, all_sprites):
        super().setup(all_sprites)

        if self.app.firstScreen != self:
            all_sprites.add(LcarsBlockMedium(colours.RED_BROWN, (145, 16), "BACK", self.back_handler), layer=1)

        try:
            self.bridge = Bridge(self.app.config['hue_ip'])
            self.bridge.connect()

            x_orig = 127
            y_orig = 107
            padding = 20
            width = 122
            height = 44
            row = 0
            col = 0
            self.groups = self.bridge.get_group()

            for group_id in self.groups:
                group = self.groups[group_id]
                x = x_orig + (col * (width + padding / 2))
                y = y_orig + (row * (height + padding / 2))
                button = GroupButton(colours.GREY_BLUE, (y, x), group['name'].upper(), self.group_handler)
                button.group_id = group_id
                col = col + 1
                if col > 4:
                    row = row + 1
                    col = 0

                all_sprites.add(button)

        except PhueRegistrationException:
            from screens.register_hue import ScreenRegister
            self.loadScreen(ScreenRegister(self.app))

    def back_handler(self, item, event, clock):
        self.loadScreen(ScreenMain(self.app))

    def group_handler(self, item, event, clock):
        group_ip = int(item.group_id)
        group = self.bridge.get_group(group_ip)
        is_on = group['action']['on']
        self.bridge.set_group(group_ip, 'on', not is_on)
