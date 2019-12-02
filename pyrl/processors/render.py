#!/usr/bin/env python
from functools import lru_cache
from pathlib import Path

import tcod.color
import tcod.console
import tcod.image

from pyrl.components import Fighter, Level, Player
from pyrl.resources import Menu, Messages, Targeting
from pyrl.resources.menu import MenuType
from pyrl.vector import Vector
from pyrl.world_helpers import ProcessorExt, defense, power

from .. import config
from ..components import Position, Visual
from ..resources import Fov
from ..resources.map import Map


class RenderProcessor(ProcessorExt):
    @staticmethod
    @lru_cache()
    def _load_image(path: Path) -> tcod.image.Image:
        rgba = tcod.image.load(str(path))
        # Drop alpha channel as Image.from_array doesn't want it
        rgb = rgba.take((0, 1, 2), 2)
        return tcod.image.Image.from_array(rgb)

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
        self._process_dungeon_level(panel)
        panel.blit(root, dest_y=config.PANEL_Y)

        self._process_menu(root)

        tcod.console_flush()

    def _process_entities(self, console: tcod.console.Console) -> None:
        fov = self.world.try_resource(Fov)
        if fov is None:
            return
        fov_map = fov.fov_map

        matches = self.world.get_components(Position, Visual)

        matches.sort(key=lambda item: item[1][1].render_order.value)
        for ent, (position, visual) in matches:
            if not fov_map.fov[position.y, position.x]:
                continue
            console.print(position.x, position.y, visual.char, fg=visual.color)

    def _process_map(self, console: tcod.console.Console) -> None:
        map = self.world.try_resource(Map)
        if map is None:
            return
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
        matches = self.world.get_components(Player, Fighter)
        if not matches:
            return
        ent, (_, fighter) = matches[0]

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
        messages = self.world.try_resource(Messages)
        if messages is None:
            return
        for y, message in enumerate(messages.messages):
            console.print(config.MESSAGE_X, y + 1, message.message, message.color)

    def _process_dungeon_level(self, console: tcod.console.Console) -> None:
        map = self.world.try_resource(Map)
        if map is None:
            return
        console.print(1, 3, f"Dungeon Level: {map.dungeon_level}")

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

    def _process_menu(self, console: tcod.console.Console) -> None:
        menu = self.world.try_resource(Menu)
        if not menu:
            return

        header_height = console.get_height_rect(
            0, 0, menu.width, config.SCREEN_HEIGHT, menu.header
        )

        # This would ideally be refactored into Menu containing a list of non-choice lines
        # or maybe a dedicated InformationMenu component, or maybe a flag on Menu switching
        # between an information-only and a choice menu
        if menu.menu_type is MenuType.CHARACTER:
            height = 6 + header_height
        else:
            # calculate total height for the header (after auto-wrap) and one line per option
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

        # render background if we're on the main menu
        if menu.menu_type is MenuType.MAIN:
            image = self._load_image(config.MAIN_MENU_BACKGROUND_PATH)
            image.blit_2x(console, dest_x=0, dest_y=0)

        # render menu contents
        contents = tcod.console_new(menu.width, height - header_height)
        if menu.menu_type is MenuType.CHARACTER:
            self._process_character_menu(contents)
        else:
            self._process_choice_menu(contents, menu)
        contents.blit(
            window, dest_x=0, dest_y=header_height, height=height - header_height
        )

        # blit onto the main console
        x = int(config.SCREEN_WIDTH / 2 - menu.width / 2)
        y = int(config.SCREEN_HEIGHT / 2 - height / 2)
        window.blit(
            console, dest_x=x, dest_y=y, width=menu.width, height=height, bg_alpha=0.7
        )

    def _process_choice_menu(self, console: tcod.console.Console, menu: Menu) -> None:
        if len(menu.options) > 26:
            raise ValueError("Cannot have a menu with more than 26 options.")

        # print all the options
        y = 0
        letter_index = ord("a")
        for option_text in menu.options:
            text = "(" + chr(letter_index) + ") " + option_text
            console.print(0, y, text, bg_blend=tcod.BKGND_NONE)
            y += 1
            letter_index += 1

    def _process_character_menu(self, console: tcod.console.Console) -> None:
        # This would ideally be refactored into Menu containing a list of non-choice lines
        # or maybe a dedicated InformationMenu component, or maybe a flag on Menu switching
        # between an information-only and a choice menu
        player = self.player
        if not player:
            return

        level = self.world.component_for_entity(player, Level)
        fighter = self.world.component_for_entity(player, Fighter)
        lines = [
            f"Level: {level.current_level}",
            f"Experience: {level.current_xp}",
            f"Experience to Level: {level.experience_to_next_level}",
            f"Maximum HP: {fighter.max_hp}",
            f"Attack: {power(self.world, player)}",
            f"Defense: {defense(self.world, player)}",
        ]

        for y, line in enumerate(lines):
            console.print(0, y, line, bg_blend=tcod.BKGND_NONE)
