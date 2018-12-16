from phue import Bridge, PhueRegistrationException

from screens.base_screen import BaseScreen
from screens.main import ScreenMain
from ui import colours
from ui.widgets.lcars_widgets import LcarsBlockMedium, LcarsButton, LcarsBlockLarge, LcarsBlockSmall


class IdButton(LcarsButton):

    def __init__(self, colour, pos, text, handler=None, rectSize=None):
        super().__init__(colour, pos, text, handler, rectSize)
        self.id = 0

    def set_state(self, state):
        color = colours.GREY_BLUE
        if state:
            color = colours.BEIGE
        self.applyColour(color)


class BaseLightingScreen(BaseScreen):
    def __init__(self, app):
        super().__init__(app, "assets/lcars_screen_1.png", "LIGHTING")
        self.bridge = None

    def setup(self, all_sprites):
        super().setup(all_sprites)

        all_sprites.add(LcarsBlockMedium(colours.RED_BROWN, (145, 16), "BACK", self.back_handler), layer=1)

        try:
            self.bridge = Bridge(self.app.config['hue_ip'])
            self.bridge.connect()

            self.child_setup(all_sprites)

        except PhueRegistrationException:
            from screens.register_hue import ScreenRegister
            self.loadScreen(ScreenRegister(self.app))
        except Exception:
            from pygame.mixer import Sound
            Sound("assets/audio/unable_to_comply.wav").play()
            self.loadScreen(ScreenMain(self.app))

    def back_handler(self, item, event, clock):
        self.loadScreen(ScreenMain(self.app))

    def child_setup(self, all_sprites):
        pass


class ScreenGroup(BaseLightingScreen):

    def __init__(self, app):
        super().__init__(app)
        self.buttons = {}
        self.lights = None
        self.group_id = None

    def child_setup(self, all_sprites):
        super().child_setup(all_sprites)
        x_orig = 127
        y_orig = 107
        padding = 20
        width = 122
        height = 44
        row = 0
        col = 0
        lights = self.bridge.get_group(int(self.group_id), 'lights')

        for light_id in lights:
            light = self.bridge.get_light(int(light_id))
            x = x_orig + (col * (width + padding / 2))
            y = y_orig + (row * (height + padding / 2))

            button = IdButton(colours.BEIGE, (y, x), light['name'].upper(), self.light_handler)
            button.id = light_id
            button.set_state(light['state']['on'])
            self.buttons[int(light_id)] = button
            col = col + 1
            if col > 4:
                row = row + 1
                col = 0

            all_sprites.add(button)

        all_sprites.add(LcarsBlockLarge(colours.BEIGE, (249, 16), "SHUTDOWN", self.shutdown_handler), layer=1)

        all_sprites.add(LcarsBlockSmall(colours.ORANGE, (211, 16), "POWER UP", self.all_on_handler), layer=1)

    def back_handler(self, item, event, clock):
        self.loadScreen(ScreenLightGroups(self.app))

    def shutdown_handler(self, item, event, clock):
        group_id = int(self.group_id)
        self.bridge.set_group(group_id, 'on', False)
        for light_id in self.buttons:
            button = self.buttons[light_id]
            button.set_state(False)

    def all_on_handler(self, item, event, clock):
        group_id = int(self.group_id)
        self.bridge.set_group(group_id, 'on', True)
        for light_id in self.buttons:
            button = self.buttons[light_id]
            button.set_state(True)

    def light_handler(self, item, event, clock):
        light_id = int(item.id)
        light = self.bridge.get_light(light_id)
        is_on = light['state']['on']
        self.bridge.set_light(light_id, 'on', not is_on)
        item.set_state(not is_on)


class ScreenLightGroups(BaseLightingScreen):

    def __init__(self, app):
        super().__init__(app)
        self.groups = {}
        self.buttons = {}

    def child_setup(self, all_sprites):
        super().child_setup(all_sprites)

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

            button = IdButton(colours.BEIGE, (y, x), group['name'].upper(), self.group_handler)
            button.id = group_id
            button.set_state(group['action']['on'])
            self.buttons[int(group_id)] = button
            col = col + 1
            if col > 4:
                row = row + 1
                col = 0

            all_sprites.add(button)

        all_sprites.add(LcarsBlockLarge(colours.BEIGE, (249, 16), "SHUTDOWN", self.all_lights_handler),
                        layer=1)

    def group_handler(self, item, event, clock):
        group = ScreenGroup(self.app)
        group.group_id = item.id
        self.loadScreen(group)

    def all_lights_handler(self, item, event, clock):
        for group_id in self.groups:
            group_id = int(group_id)
            group = self.bridge.get_group(group_id)
            is_on = group['action']['on']
            if is_on:
                self.bridge.set_group(group_id, 'on', False)
                self.buttons[group_id].set_state(False)
