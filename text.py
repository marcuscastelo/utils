from dataclasses import dataclass
from typing import Any
import pygame

from bot_base.util.geometry import Vec2Int

pygame.font.init()

def get_font(fontName = "Arial", size = 20, bold = False, italic = False):
    assert isinstance(fontName, str)
    assert isinstance(size, int)
    assert isinstance(bold, bool)
    assert isinstance(italic, bool)
    font = pygame.font.SysFont(fontName, size)
    font.set_bold(bold)
    font.set_italic(italic)
    return font

@dataclass
class Text:
    text: str
    pos: Vec2Int
    font: Any
    color: tuple
    centered: bool = False
    visible: bool = True

    def __post_init__(self):
        assert isinstance(self.text, str), "Text.text must be a string"

    def colored(self, color: tuple):
        return Text(self.text, self.pos, self.font, color, self.centered)