import time
from math import atan2

import imu
import ntptime
from events.input import BUTTON_TYPES, Buttons
from system.eventbus import eventbus
from system.patterndisplay.events import PatternDisable
from tildagonos import tildagonos

import app

from .common.background import Background
from .common.conf import conf
from .lib.tools import decimalise_colour, get_interval, led_correct


class Countdown(app.App):
    """Countdown."""

    def __init__(self):
        """Construct."""
        eventbus.emit(PatternDisable())
        ntptime.settime()

        self.button_states = Buttons(self)
        self.conf = conf(__file__)

        self.pallette = self.conf["colours"]["pallette"]
        self.screen_colours = self.conf["colours"]["screen"]

        self.units = self.conf["units"]
        self.unit_index = 3

        self.rotation_offset = 0

        self.resolve_colours()

    def update(self, _):
        """Update."""
        self.scan_buttons()

        acc = imu.acc_read()
        weighting = min(1.0, int(abs(10 - acc[2])) / 9)
        self.rotation_offset = (atan2(acc[1], acc[0])) * weighting

        now = time.time()
        self.interval = self.conf["emf-seconds"] - now
        self.unit = self.units[self.unit_index]

        self.light_leds()

    def draw(self, ctx):
        """Draw."""
        self.overlays = []
        self.overlays.append(
            Background(colour=self.display_colours["background"], opacity=0.85)
        )
        self.draw_overlays(ctx)

        ctx.rotate(-self.rotation_offset)
        self.write_text(ctx)

    def write_text(self, ctx):
        """Write the text."""
        ctx.rgb(*self.display_colours["text"])
        ctx.text_align = ctx.CENTER
        ctx.text_baseline = ctx.MIDDLE

        our_interval = get_interval(self.interval, self.unit)

        verb = "are"
        unit_name = self.unit["name"]

        if our_interval == 1:
            verb = "is"
            unit_name = unit_name[:-1]

        strings = (
            (f"There {verb}", "small", -60),
            (str(our_interval), "large", -22),
            (unit_name, "medium", 14),
            ("until EMF 2026", "small", 50),
        )

        for item in strings:
            ctx.font_size = self.conf["text"]["sizes"][item[1]]
            ctx.move_to(0, item[2])
            ctx.text(item[0])

    def scan_buttons(self):
        """Buttons."""
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()

        if self.button_states.get(BUTTON_TYPES["UP"]):
            self.button_states.clear()
            if self.unit_index < len(self.units) - 1:
                self.unit_index += 1

        if self.button_states.get(BUTTON_TYPES["DOWN"]):
            self.button_states.clear()
            if self.unit_index > 0:
                self.unit_index -= 1

        if self.button_states.get(BUTTON_TYPES["CONFIRM"]):
            self.button_states.clear()

            temp = self.conf["colours"]["screen"]["background"]
            self.conf["colours"]["screen"]["background"] = self.conf["colours"][
                "screen"
            ]["text"]
            self.conf["colours"]["screen"]["text"] = temp

            self.resolve_colours()

    def resolve_colours(self):
        """Sort out the colours."""
        self.led_colours = {}

        for name, key in self.conf["colours"]["leds"].items():
            self.led_colours[name] = led_correct(self.conf["colours"]["pallette"][key])

        self.display_colours = {}
        for name, key in self.conf["colours"]["screen"].items():
            self.display_colours[name] = decimalise_colour(
                self.conf["colours"]["pallette"][key]
            )

    def light_leds(self):
        """Light lights."""
        for index in range(12):
            tildagonos.leds[index + 1] = self.led_colours["background"]

        tildagonos.leds[12 - (self.interval % 12)] = self.led_colours["ticker"]

        tildagonos.leds.write()


__app_export__ = Countdown
