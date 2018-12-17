import string
import urllib

import nest
import requests
from pygame.mixer import Sound

from screens.base_screen import BaseScreen
from screens.main import ScreenMain
from ui import colours
from ui.widgets.lcars_widgets import LcarsBlockMedium, LcarsText, LcarsButton


class ThermostatButton(LcarsButton):
    def __init__(self, thermostat, pos, handler):
        self.thermostat = thermostat

        color = colours.RED_BROWN if thermostat.temperature > 65 else colours.GREY_BLUE

        super().__init__(color,
                         pos,
                         "%s (%s)" % (thermostat.name, thermostat.temperature),
                         handler)


class ThermostatScreen(BaseScreen):
    def __init__(self, app, thermostat):
        super().__init__(app, "assets/lcars_screen_1.png", thermostat.name_long)
        self.thermostat = thermostat
        self.target_temp = self.thermostat.target
        self.temp_sprite = None

    def setup(self, all_sprites):
        super().setup(all_sprites)

        all_sprites.add(LcarsBlockMedium(colours.RED_BROWN, (145, 16), "BACK", self.back_handler), layer=1)

        all_sprites.add(LcarsButton(colours.RED_BROWN, (107, 127 + 212), "Warmer", self.warm_handler))
        all_sprites.add(LcarsButton(colours.BLUE, (107, 127), "Cooler", self.cool_handler))

        self.temp_sprite = LcarsText(colours.ORANGE, (107, 127 + 132), self.get_temperature_string(), 2.0)

        all_sprites.add(self.temp_sprite)

    def update_temp_sprite(self):
        self.temp_sprite.setText(self.get_temperature_string())

    def warm_handler(self, item, event, clock):
        self.target_temp += 1
        if self.target_temp > self.thermostat.max_temperature:
            self.target_temp = self.thermostat.max_temperature

        self.update_temp_sprite()

    def cool_handler(self, item, event, clock):
        self.target_temp -= 1
        if self.target_temp < self.thermostat.min_temperature:
            self.target_temp = self.thermostat.min_temperature

        self.update_temp_sprite()

    def back_handler(self, item, event, clock):
        self.thermostat.target = self.target_temp
        self.loadScreen(ClimateScreen(self.app))

    def get_temperature_string(self):
        return "%s" % self.target_temp


class ClimateScreen(BaseScreen):
    def __init__(self, app):
        super().__init__(app, "assets/lcars_screen_1.png", "LIFE SUPPORT")
        self.pin = []
        self.pin_entry_sprites = []
        self.pin_sprite = None
        self.auth_url = None
        self.napi = nest.Nest(client_id=self.app.config['nest']['client_id'],
                              client_secret=self.app.config['nest']['client_secret'],
                              access_token_cache_file='nest.json')
        self.sound_denied = Sound("assets/audio/access_denied.wav")

    def setup(self, all_sprites):
        super().setup(all_sprites)

        all_sprites.add(LcarsBlockMedium(colours.RED_BROWN, (145, 16), "BACK", self.back_handler), layer=1)

        if self.napi.authorization_required:
            self.add_pin_entry_sprites(all_sprites)
            self.show_pin_entry()
        else:
            self.add_thermostats(all_sprites)

    def add_pin_entry_sprites(self, all_sprites):
        buttons = list(string.ascii_lowercase) + list(string.digits) + ["DEL"]
        x_orig = 127
        y_orig = 197
        padding = 20
        width = 44
        height = 46
        row = 0
        col = 0
        max_col = 11
        for letter in buttons:
            x = x_orig + (col * (width + padding / 2))
            y = y_orig + (row * (height + padding / 2))
            from screens.authorize import CodeButton
            button = CodeButton(colours.GREY_BLUE, (y, x), str(letter).upper(), self.button_handler,
                                (width, height))
            button.code = letter
            col = col + 1
            if col > max_col:
                row = row + 1
                col = 0

            all_sprites.add(button, layer=2)

            all_sprites.add(
                LcarsText(colours.ORANGE, (107, 127), "Open %s on your computer." % self.get_auth_url(), 2.0),
                layer=2)

            self.pin_sprite = LcarsText(colours.ORANGE, (147, 127), "PIN: %s" % self.pin_text(), 2.0)

            all_sprites.add(self.pin_sprite, layer=2)
        self.pin_entry_sprites = all_sprites.get_sprites_from_layer(2)
        self.hide_pin_entry()

    def get_auth_url(self):
        if self.auth_url is None:
            self.auth_url = self.napi.authorize_url
            short_links_url = "https://firebasedynamiclinks.googleapis.com/v1/shortLinks?key=%s" % self.app.config[
                "firebase_key"]
            data = {
                "longDynamicLink": "https://lcars.page.link/?link=%s" % urllib.parse.quote(self.auth_url),
                "suffix": {
                    "option": "SHORT"
                }
            }
            response = requests.post(short_links_url, json=data)

            if response.status_code == 200:
                print(response.text)
                self.auth_url = response.json()['shortLink']

        return self.auth_url

    def thermostat_button_handler(self, item, event, clock):
        self.loadScreen(ThermostatScreen(self.app, item.thermostat))
        pass

    def button_handler(self, item, event, clock):
        if item.code == "DEL" and len(self.pin) > 0:
            self.pin.pop()
        else:
            self.pin.append(item.code)

        self.update_pin_sprite()
        if len(self.pin) == 8:
            self.submit_pin()

    def update_pin_sprite(self):
        self.pin_sprite.setText("PIN: %s" % self.pin_text())

    def pin_text(self):
        return ''.join(self.pin)

    def back_handler(self, item, event, clock):
        self.loadScreen(ScreenMain(self.app))

    def show_pin_entry(self):
        for sprite in self.pin_entry_sprites:
            sprite.visible = True

    def hide_pin_entry(self):
        for sprite in self.pin_entry_sprites:
            sprite.visible = False

    def submit_pin(self):
        try:
            self.napi.request_token(self.pin_text())
            # Try to login, and if we can, refresh the screen to let that kick in.
            self.loadScreen(ClimateScreen(self.app))
        except Exception:
            self.sound_denied.play()
            self.pin = []
            self.update_pin_sprite()

    def add_thermostats(self, all_sprites):
        x_orig = 127
        y_orig = 107
        padding = 20
        width = 122
        height = 44
        row = 0
        col = 0
        for thermostat in self.napi.thermostats:
            x = x_orig + (col * (width + padding / 2))
            y = y_orig + (row * (height + padding / 2))
            button = ThermostatButton(thermostat, (y, x), self.thermostat_button_handler)
            col = col + 1
            if col > 4:
                row = row + 1
                col = 0

            all_sprites.add(button, layer=3)
