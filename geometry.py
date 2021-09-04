from dataclasses import dataclass
from typing import Any, Union

import util.colors as colors
from util.serialization import Serializable

@dataclass
class Vec2:
    x: int
    y: int

    def norm_sq(self):
        return self.x ** 2 + self.y ** 2
    
    def norm(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vec2(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Vec2(self.x / other, self.y / other)

    def __floordiv__(self, other):
        return Vec2(self.x // other, self.y // other)

    def __mod__(self, other):
        return Vec2(self.x % other, self.y % other)

    def __neg__(self):
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
    color: tuple = colors.pink # BGRA
    filled: bool = False
    relative: bool = False
    visible: bool = True

    def __post_init__(self):
        self.assert_fields()

    def assert_fields(self):
        assert isinstance(self.color, tuple), "Color must be a tuple"
        assert len(self.color) == 3, "Color must be a 3-tuple"
        assert isinstance(self.filled, bool), "Filled must be a boolean"
        assert isinstance(self.relative, bool), "Relative must be a boolean"
        assert isinstance(self.visible, bool), "Visible must be a boolean"
        assert isinstance(self.x, int), "x must be an integer"
        assert isinstance(self.y, int), "y must be an integer"
        assert isinstance(self.width, int), "width must be an integer"
        assert isinstance(self.height, int), "height must be an integer"
        assert self.width >= 0, "width must be >= 0"
        assert self.height >= 0, "height must be >= 0"
        assert self.x >= 0, "x must be >= 0"
        assert self.y >= 0, "y must be >= 0"

    def center(self) -> Vec2:
        return Vec2(self.x + self.width // 2, self.y + self.height // 2)
    
    def center_x(self) -> int:
        return self.x + self.width // 2

    def center_y(self) -> int:
        return self.y + self.height // 2

    def pivot(self) -> Vec2:
        return Vec2(self.x, self.y)
    
    def size(self) -> Vec2:
        return Vec2(self.width, self.height)

    def to_bbox(self) -> tuple:
        return (self.x, self.y, self.width + self.x, self.height + self.y)

    @classmethod
    def from_bbox(self, bbox: tuple):
        return Rect(bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1])

    def __index__(self):
        return self.x, self.y, self.width, self.height, self.color, self.filled

    def __repr__(self):
        return f'Rect(x={self.x}, y={self.y}, width={self.width}, height={self.height}, color={self.color}, filled={self.filled}, relative={self.relative}, visible={self.visible})'

    def __iter__(self):
        yield from (self.x, self.y, self.width, self.height, self.color, self.filled, self.relative, self.visible)

    def __getitem__(self, item):
        return (self.x, self.y, self.width, self.height, self.color, self.filled, self.relative, self.visible)[item]

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

    def __contains__(self, Vec2: Vec2) -> bool:
        return (self.x <= Vec2.x < self.x + self.width and
                self.y <= Vec2.y < self.y + self.height)

    def __eq__(self, o: object) -> bool:
        return self.x == o.x and self.y == o.y and self.width == o.width and self.height == o.height

    def __hash__(self):
        return hash((self.x, self.y, self.width, self.height, self.color))

    def expand(self, amount: Union[int, Vec2]):
        if isinstance(amount, int):
            return Rect(self.x - amount, self.y - amount, self.width + amount * 2, self.height + amount * 2, self.color, self.filled, self.relative, self.visible)
        elif isinstance(amount, Vec2):
            return Rect(self.x - amount.x, self.y - amount.y, self.width + amount.x * 2, self.height + amount.y * 2, self.color, self.filled, self.relative, self.visible)
        else:
            raise TypeError(f'Expected int or Vec2, got {type(amount)}')

    def expandUp(self, amount: int):
        return Rect(self.x, self.y - amount, self.width, self.height + amount, self.color, self.filled, self.relative, self.visible)
    
    def expandDown(self, amount: int):
        return Rect(self.x, self.y, self.width, self.height + amount, self.color, self.filled, self.relative, self.visible)

    def expandLeft(self, amount: int):
        return Rect(self.x - amount, self.y, self.width + amount, self.height, self.color, self.filled, self.relative, self.visible)

    def expandRight(self, amount: int):
        return Rect(self.x, self.y, self.width + amount, self.height, self.color, self.filled, self.relative, self.visible)

    def moveRel(self, movementVec: Vec2):
        return Rect(self.x + movementVec.x, self.y + movementVec.y, self.width, self.height, self.color, self.filled, self.relative, self.visible)

    def moveRelX(self, amount: int):
        return Rect(self.x + amount, self.y, self.width, self.height, self.color, self.filled, self.relative, self.visible)

    def moveRelY(self, amount: int):
        return Rect(self.x, self.y + amount, self.width, self.height, self.color, self.filled, self.relative, self.visible)

    def moveAbs(self, newPivot: Vec2):
        return Rect(newPivot.x, newPivot.y, self.width, self.height, self.color, self.filled, self.relative, self.visible)

    def copy(self):
        return Rect(self.x, self.y, self.width, self.height, self.color, self.filled, self.relative, self.visible)

    def colored(self, color: tuple):
        return Rect(self.x, self.y, self.width, self.height, color, self.filled, self.relative, self.visible)

    def slice_frame(self, frame):
        sx, sy, w, h = self.x, self.y, self.width, self.height
        ex, ey = sx + w, sy + h
        return frame[sy:ey, sx:ex]