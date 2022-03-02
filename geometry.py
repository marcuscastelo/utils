from dataclasses import dataclass
from typing import Tuple

import bot_base.util.colors as colors
from bot_base.util.serialization import Serializable

from copy import copy

import numpy as np

@dataclass
class Vec2:
    x: int
    y: int

    def norm_sq(self):
        return self.x ** 2 + self.y ** 2
    
    def norm(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def proj_x(self):
        return Vec2(self.x, 0)
    
    def proj_y(self):
        return Vec2(0, self.y)

    def with_x(self, x):
        return Vec2(x, self.y)

    def with_y(self, y):
        return Vec2(self.x, y)

    def __add__(self, other: 'Vec2') -> 'Vec2':
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vec2') -> 'Vec2':
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other: int) -> 'Vec2':
        return Vec2(self.x * other, self.y * other)

    def __truediv__(self, other: int) -> 'Vec2':
        return Vec2(self.x / other, self.y / other)

    def __floordiv__(self, other : int) -> 'Vec2':
        return Vec2(self.x // other, self.y // other)

    def __mod__(self, other) -> 'Vec2':
        return Vec2(self.x % other, self.y % other)

    def __neg__(self) -> 'Vec2':
        return Vec2(-self.x, -self.y)

    def __ne__(self, o: object) -> bool:
        return self.x != o.x or self.y != o.y
    
    def __eq__(self, o: object) -> bool:
        return self.x == o.x and self.y == o.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f'Vec2({self.x}, {self.y})'

    def __iter__(self):
        yield from (self.x, self.y)

    def __getitem__(self, item):
        return (self.x, self.y)[item]

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError


    def __len__(self):
        return 2

@dataclass
class Rect(Serializable):
    x: int
    y: int
    width: int
    height: int

    def __post_init__(self):
        self.x = int(self.x)
        self.y = int(self.y)
        self.width = int(self.width)
        self.height = int(self.height)

    def __repr__(self):
        return f'Rect({self.x}, {self.y}, {self.width}, {self.height})'

    def __iter__(self):
        yield from (self.x, self.y, self.width, self.height)

    def __getitem__(self, item):
        assert isinstance(item, int)
        return (self.x, self.y, self.width, self.height)[item]
    
    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.width = value
        elif key == 3:
            self.height = value
        else:
            raise IndexError

    def __add__(self, vec: 'Vec2') -> 'Rect':
        assert isinstance(vec, Vec2)
        newRect = copy(self)
        newRect.x += vec.x
        newRect.y += vec.y
        return newRect

    def __sub__(self, vec: 'Vec2') -> 'Rect':
        assert isinstance(vec, Vec2)
        newRect = copy(self)
        newRect.x -= vec.x
        newRect.y -= vec.y
        return newRect

    def center(self) -> 'Vec2':
        return Vec2(self.x + self.width // 2, self.y + self.height // 2)

    def pivot(self) -> 'Vec2':
        return Vec2(self.x, self.y)

    def size(self) -> 'Vec2':
        return Vec2(self.width, self.height)
    
    def to_bbox(self) -> tuple:
        return (self.x, self.y, self.width + self.x, self.height + self.y)

    def to_double_point(self) -> Tuple[Vec2]:
        return (self.top_left(), self.bottom_right())

    def top_left(self) -> Vec2:
        return Vec2(self.x, self.y)

    def top_right(self) -> Vec2:
        return Vec2(self.x + self.width, self.y)

    def bottom_left(self) -> Vec2:
        return Vec2(self.x, self.y + self.height)

    def bottom_right(self) -> Vec2:
        return Vec2(self.x + self.width, self.y + self.height)

    def with_x(self, x: int) -> 'Rect':
        newRect = copy(self)
        newRect.x = x
        return copy 

    def with_y(self, y: int) -> 'Rect':
        newRect = copy(self)
        newRect.y = y
        return copy

    def with_pivot(self, pivot: 'Vec2') -> 'Rect':
        newRect = copy(self)
        newRect.x = pivot.x - self.width // 2
        newRect.y = pivot.y - self.height // 2
        return newRect

    def with_width(self, width: int) -> 'Rect':
        newRect = copy(self)
        newRect.width = width
        return newRect

    def with_height(self, height: int) -> 'Rect':
        newRect = copy(self)
        newRect.height = height
        return newRect

    def with_size(self, size: 'Vec2') -> 'Rect':
        newRect = copy(self)
        newRect.width = size.x
        newRect.height = size.y
        return newRect

    def expandUp(self, amount: int):
        newRect = copy(self)
        newRect.y -= amount
        newRect.height += amount
        return newRect
    
    def expandDown(self, amount: int):
        newRect = copy(self)
        newRect.height += amount
        return newRect

    def expandLeft(self, amount: int):
        newRect = copy(self)
        newRect.x -= amount
        newRect.width += amount
        return newRect

    def expandRight(self, amount: int):
        newRect = copy(self)
        newRect.width += amount
        return newRect

    def expandCenter(self, amount: int):
        newRect = copy(self)
        newRect.x -= amount
        newRect.y -= amount
        newRect.width += amount * 2
        newRect.height += amount * 2
        return newRect

    def moveRel(self, movementVec: Vec2):
        newRect = copy(self)
        newRect.x += movementVec.x
        newRect.y += movementVec.y
        return newRect

    def moveRelX(self, amount: int):
        newRect = copy(self)
        newRect.x += amount
        return newRect

    def moveRelY(self, amount: int):
        newRect = copy(self)
        newRect.y += amount
        return newRect

    def moveAbs(self, newPivot: Vec2):
        newRect = copy(self)
        newRect.x = newPivot.x 
        newRect.y = newPivot.y
        return newRect

    def __contains__(self, Vec2: Vec2) -> bool:
        return (self.x <= Vec2.x < self.x + self.width and
                self.y <= Vec2.y < self.y + self.height)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Rect):
            return False
        return self.x == o.x and self.y == o.y and self.width == o.width and self.height == o.height

    @classmethod
    def from_bbox(cls, bbox: tuple):
        return cls(bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1])

    def cut_image(self, img: np.ndarray) -> np.ndarray:
        sx, sy, w, h = self.x, self.y, self.width, self.height
        ex, ey = sx + w, sy + h
        return img[sy:ey, sx:ex]

@dataclass
class GRect(Rect):
    color: tuple = colors.pink # BGRA
    filled: bool = False
    visible: bool = True

    def __post_init__(self):
        self.x, self.y, self.width, self.height = map(int, [self.x, self.y, self.width, self.height])
        try:
            self.assert_fields()
        except AssertionError as e:
            print(f'Rectangle: {self.x}, {self.y}, {self.width}, {self.height}, color={self.color}, filled={self.filled}, visible={self.visible}')
            raise e

    def assert_fields(self):
        assert isinstance(self.color, tuple), "Color must be a tuple"
        assert len(self.color) == 3, "Color must be a 3-tuple"
        assert isinstance(self.filled, bool), "Filled must be a boolean"
        assert isinstance(self.visible, bool), "Visible must be a boolean"
        assert isinstance(self.x, int), "x must be an integer"
        assert isinstance(self.y, int), "y must be an integer"
        assert isinstance(self.width, int), "width must be an integer"
        assert isinstance(self.height, int), "height must be an integer"
        assert self.width >= 0, "width must be >= 0, but was " + str(self.width)
        assert self.height >= 0, "height must be >= 0, but was " + str(self.height)
        # assert self.x >= 0, "x must be >= 0"
        # assert self.y >= 0, "y must be >= 0"

    def __index__(self):
        return self.x, self.y, self.width, self.height, self.color, self.filled

    def __repr__(self):
        return f'GRect({self.x}, {self.y}, {self.width}, {self.height}, color={self.color}, filled={self.filled}, visible={self.visible})'

    def __iter__(self):
        yield from (self.x, self.y, self.width, self.height, self.color, self.filled, self.visible)

    def __getitem__(self, item):
        return (self.x, self.y, self.width, self.height, self.color, self.filled, self.visible)[item]

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.width = value
        elif key == 3:
            self.height = value
        elif key == 4:
            self.color = value
        elif key == 5:
            self.filled = value
        else:
            raise IndexError

    def colored(self, color: tuple):
        return GRect(self.x, self.y, self.width, self.height, color, self.filled, self.visible)

   