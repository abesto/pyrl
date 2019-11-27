#!/usr/bin/env python

import tcod.color
import tcod.console

from pyrl.components import Collider, Fighter, Player
from pyrl.resources import Menu, Messages, Targeting
from pyrl.vector import Vector

from .. import config
from ..components import Position, Visual
from ..esper_ext import Processor
from ..resources import Fov
from ..resources.map import Map


class RenderProcessor(Processor):
    def process(self):
        root = self.world.get_resource(tcod.console.Console)

        map_panel = tcod.console.Console(config.MAP_WIDTH, config.MAP_HEIGHT)
        self._process_map(map_panel)
        self._process_entities(map_panel)
        self._process_targeting(map_panel)
        map_panel.blit(root)

        panel = tcod.console.Console(config.SCREEN_WIDTH, config.PANEL_HEIGHT)
        self._process_healthbar(panel)
        self._process_messages(panel)
        panel.blit(root, dest_y=config.PANEL_Y)

        self._process_menu(root)

        tcod.console_flush()

    def _process_entities(self, console: tcod.console.Console) -> None:
        fov_map = self.world.get_resource(Fov).fov_map
        matches = self.world.get_components(Position, Visual)

        matches.sort(key=lambda item: item[1][1].render_order.value)
        for ent, (position, visual) in matches:
            if not fov_map.fov[position.y, position.x]:
                continue
            console.print(position.x, position.y, visual.char, fg=visual.color)

    def _process_map(self, console: tcod.console.Console) -> None:
        map = self.world.get_resource(Map)
        fov_map = self.world.get_resource(Fov).fov_map
        for x, column in enumerate(map.tiles):
            for y, tile in enumerate(column):
                if not tile.explored:
                    continue
                wall = tile.block_sight
                visible = fov_map.fov[y, x]

                if wall:
                    char = "#"
                else:
                    char = "."

                console.print(
                    x, y, char, bg=config.theme.background_color(wall, visible)
                )

    def _process_targeting(self, console: tcod.console.Console) -> None:
        targeting = self.world.try_resource(Targeting)
        if targeting is None:
            return

        fov_map = self.world.get_resource(Fov).fov_map
        topleft = targeting.current_target - Vector(targeting.radius, targeting.radius)
        bottomright = targeting.current_target + Vector(
            targeting.radius, targeting.radius
        )
        for x in range(topleft.x, bottomright.x + 1):
            for y in range(topleft.y, bottomright.y + 1):
                try:
                    # Not very smart, but at least it's simple
                    if (
                        targeting.current_target - Vector(x, y)
                    ).length > targeting.radius:
                        continue
                    if not fov_map.fov[y, x]:
                        continue
                except IndexError:
                    pass
                else:
                    console.bg[y, x] = tcod.desaturated_green

    def _process_healthbar(self, console: tcod.console.Console) -> None:
        ent, (_, fighter) = self.world.get_components(Player, Fighter)[0]
        self._render_bar(
            console=console,
            x=1,
            y=1,
            total_width=config.BAR_WIDTH,
            name="HP",
            value=fighter.hp,
            maximum=fighter.max_hp,
            bar_color=tcod.light_red,
            back_color=tcod.darker_red,
        )

    def _process_messages(self, console: tcod.console.Console) -> None:
        messages = self.world.get_resource(Messages)
        for y, message in enumerate(messages.messages):
            console.print(config.MESSAGE_X, y + 1, message.message, message.color)

    def _render_bar(
        self,
        console: tcod.console.Console,
        x: int,
        y: int,
        total_width: int,
        name: str,
        value: int,
        maximum: int,
        bar_color: tcod.color.Color,
        back_color: tcod.color.Color,
    ):
        bar_width = int(float(value) / maximum * total_width)

        console.draw_rect(
            x,
            y,
            total_width,
            height=1,
            ch=ord(" "),
            bg=back_color,
            bg_blend=tcod.BKGND_SCREEN,
        )
        if bar_width > 0:
            console.draw_rect(
                x,
                y,
                bar_width,
                height=1,
                ch=ord(" "),
                bg=bar_color,
                bg_blend=tcod.BKGND_SCREEN,
            )

        console.print(
            int(x + total_width / 2),
            y,
            f"{name}: {value}/{maximum}",
            bg_blend=tcod.BKGND_NONE,
            alignment=tcod.CENTER,
        )

    def _process_menu(self, console: tcod.console.Console):
        menu = self.world.try_resource(Menu)
        if not menu:
            return

        if len(menu.options) > 26:
            raise ValueError("Cannot have a menu with more than 26 options.")

        # calculate total height for the header (after auto-wrap) and one line per option
        header_height = console.get_height_rect(
            0, 0, menu.width, config.SCREEN_HEIGHT, menu.header
        )
        height = len(menu.options) + header_height

        # create an off-screen console that represents the menu's window
        window = tcod.console_new(menu.width, height)

        # print the header, with auto-wrap
        window.print_rect(
            0,
            0,
            menu.width,
            height,
            menu.header,
            bg_blend=tcod.BKGND_NONE,
            alignment=tcod.LEFT,
        )

        # print all the options
        y = header_height
        letter_index = ord("a")
        for option_text in menu.options:
            text = "(" + chr(letter_index) + ") " + option_text
            window.print(0, y, text, bg_blend=tcod.BKGND_NONE)
            y += 1
            letter_index += 1

        # blit the contents of "window" to the root console
        x = int(config.SCREEN_WIDTH / 2 - menu.width / 2)
        y = int(config.SCREEN_HEIGHT / 2 - height / 2)
        window.blit(
            console, dest_x=x, dest_y=y, width=menu.width, height=height, bg_alpha=0.7
        )
