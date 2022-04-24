from dataclasses import dataclass
from typing import Tuple, Union, overload

import utils.colors as colors
from utils.serialization import Serializable

from copy import copy

import numpy as np

ArrayLike = Union[list[float], tuple[float], np.ndarray]
Number = Union[int, float]


class VecN:
    @overload
    def __init__(self, element1: Number, *elements: Number): ...
    @overload
    def __init__(self, values: ArrayLike): ...
    def __init__(self, element1: Union[ArrayLike, Number], *elements: Number):
        element1_is_list_like = isinstance(element1, (list, tuple, np.ndarray, VecN))
        if element1_is_list_like:
            assert len(elements) == 0, 'If you pass a list, you must not pass any other arguments'
            self.values = np.array(element1, dtype=float)
        else:
            self.values = np.array([element1] + list(elements), dtype=float)
            return

        self.values.repeat
        unsupported_types = {type(value) for value in self.values if not isinstance(value, (float, int))}
        if unsupported_types:
            raise TypeError(f'The following types are not supported: {unsupported_types}')
    

    def projected(self, axis: Union['VecN', int]) -> float:
        if isinstance(axis, int):
            index = axis
            axis = VecN([0] * len(self.values))
            axis[index] = self.values[index]

        return np.dot(self.values, axis.values)

    def with_value(self, index: int, value: Number) -> 'VecN':
        new_vec = copy(self)
        new_vec[index] = value
        return new_vec

    def magnitude(self) -> float:
        return self.values.dot(self.values) ** 0.5

    def normalized(self) -> 'VecN':
        return self / self.magnitude()

    def __len__(self) -> int:
        return len(self.values)

    def __iter__(self) -> np.ndarray:
        return iter(self.values)

    def __repr__(self) -> str:
        return f'VecN({self.values})'

    def __str__(self) -> str:
        return f'VecN({self.values})'

    def __eq__(self, other: 'VecN') -> bool:
        if isinstance(other, (VecN, int, float, tuple, list, np.ndarray)):
            return np.all(self.values == other)
        else:
            return False

    def __ne__(self, other: 'VecN') -> bool:
        return not self.__eq__(other)

    def __add__(self, other: Union['VecN', Number, tuple, list, np.ndarray]) -> 'VecN':
        if isinstance(other, (int, float, tuple, list, np.ndarray)):
            other = VecN(other)
        return VecN(self.values + other.values)

    def __sub__(self, other: Union['VecN', Number, tuple, list, np.ndarray]) -> 'VecN':
        if isinstance(other, (int, float, tuple, list, np.ndarray)):
            other = VecN(other)
        return VecN(self.values - other.values)
    
    def __mul__(self, other: Union['VecN', Number, tuple, list, np.ndarray]) -> 'VecN':
        if isinstance(other, (int, float, tuple, list, np.ndarray)):
            other = VecN(other)
        return VecN(self.values * other.values)

    def __truediv__(self, other: Union['VecN', Number, tuple, list, np.ndarray]) -> 'VecN':
        if isinstance(other, (tuple, list, np.ndarray)):
            other = VecN(other)
        return VecN(self.values / other.values)

    def __neg__(self) -> 'VecN':
        return VecN(-self.values)

    def __abs__(self) -> 'VecN':
        return VecN(abs(self.values))

    def __pow__(self, power: Union['VecN', Number, tuple, list, np.ndarray]) -> 'VecN':
        if isinstance(power, (tuple, list, np.ndarray)):
            power = VecN(power)
        return VecN(self.values ** power.values)

    def __rpow__(self, power: Union['VecN', Number, tuple, list, np.ndarray]) -> 'VecN':
        if isinstance(power, (tuple, list, np.ndarray)):
            power = VecN(power)
        return VecN(power.values ** self.values)

    def __getstate__(self) -> dict:
        return {'values': self.values.tolist()}

    def __setstate__(self, state: dict) -> None:
        self.values = np.array(state['values'])

    def __copy__(self) -> 'VecN':
        return VecN(self.values)

    def __deepcopy__(self, memo: dict) -> 'VecN':
        return VecN(copy(self.values))

    def __getitem__(self, index: Union[int, slice]) -> Union['VecN', float]:
        if isinstance(index, int):
            return self.values[index]
        return VecN(self.values[index])

    def keys(self) -> list[int]:
        return list(range(len(self)))

    def __setitem__(self, index: Union[int, slice], value: Union['VecN', float, list, tuple, np.ndarray]) -> None:
        if isinstance(value, (float, int, tuple, list, np.ndarray)):
            if isinstance(value, (tuple, list)):
                value = np.ndarray(value)
            elif isinstance(value, VecN):
                value = value.values
            elif isinstance(value, (float, int)):
                value = np.array([value])
            self.values[index] = value
        else:
            raise TypeError(f'{type(value)} is not supported')
    


class Vec2(VecN):

    @overload
    def __init__(self, x: Number, y: Number):...
    @overload
    def __init__(self, values: tuple[Number, Number]):...
    @overload
    def __init__(self, values: Union[list[Number], tuple[Number], np.ndarray]):...
    @overload
    def __init__(self, vec: VecN):...
    def __init__(self, arg1, *args):
        if isinstance(arg1, VecN):
            assert len(arg1) == 2, 'Vec2 can only be initialized with a VecN with 2 elements'
            assert len(args) == 0, 'If you pass a VecN, you must not pass any other arguments'
            super().__init__(arg1.values)
        elif isinstance(arg1, (tuple, list, np.ndarray)):
            if len(arg1) != 2:
                raise ValueError(f'Vec2 can only be initialized with 2 values, got {len(arg1)}')
            super().__init__(arg1)
        elif isinstance(arg1, (float, int)):
            if len(args) != 1:
                raise ValueError(f'Vec2 can only be initialized with 2 values, got {len(args) + 1}')
            super().__init__(arg1, *args)
        else:
            raise TypeError(f'{type(arg1)} is not supported')
    @property
    def x(self) -> float:
        return self.values[0]
    
    @x.setter
    def x(self, value: float) -> None:
        self.values[0] = value
    
    @property
    def y(self) -> float:
        return self.values[1]
    
    @y.setter
    def y(self, value: float) -> None:
        self.values[1] = value

    @property
    def xy(self) -> 'Vec2':
        return Vec2(self.values)
    
    @xy.setter
    def xy(self, value: 'Vec2') -> None:
        self.x, self.y = value.values
    
    def projected_x(self) -> float:
        return self.projected(0)
    
    def projected_y(self) -> float:
        return self.projected(1)

    def __repr__(self) -> str:
        return f'Vec2({self.values[0]}, {self.values[1]})'

    def __str__(self) -> str:
        return f'Vec2({self.values[0]}, {self.values[1]})'

class Vec3(VecN):
    @overload
    def __init__(self, x: Number, y: Number, z: Number):...
    @overload
    def __init__(self, values: tuple[Number, Number, Number]):...
    @overload
    def __init__(self, values: Union[list[Number], tuple[Number], np.ndarray]):...
    @overload
    def __init__(self, other: 'Vec3'):...
    def __init__(self, arg1, *args):
        if isinstance(arg1, VecN):
            assert len(args) == 0, 'Copy constructor can only be used with no additional arguments'
            assert len(arg1) == 3, 'Vec3 copy constructor can only be initialized with a VecN with 3 elements (or Vec3)'
            super().__init__(arg1.values)
        elif isinstance(arg1, (tuple, list, np.ndarray)):
            if len(arg1) != 3:
                raise ValueError(f'Vec3 can only be initialized with 3 values, got {len(arg1)}')
            super().__init__(arg1)
        elif isinstance(arg1, (float, int)):
            if len(args) != 2:
                raise ValueError(f'Vec3 can only be initialized with 3 values, got {len(args) + 1}')
            super().__init__(arg1, *args)
        else:
            raise TypeError(f'{type(arg1)} is not supported')
    @property
    def x(self) -> float:
        return self.values[0]
    
    @x.setter
    def x(self, value: float) -> None:
        self.values[0] = value
    
    @property
    def y(self) -> float:
        return self.values[1]
    
    @y.setter
    def y(self, value: float) -> None:
        self.values[1] = value
    
    @property
    def z(self) -> float:
        return self.values[2]
    
    @z.setter
    def z(self, value: float) -> None:
        self.values[2] = value
    
    @property
    def xy(self) -> Vec2:
        return Vec2(self.values[0], self.values[1])

    @xy.setter
    def xy(self, value: Vec2) -> None:
        self.x, self.y = value

    @property
    def xz(self) -> Vec2:
        return Vec2(self.values[0], self.values[2])

    @xz.setter
    def xz(self, value: Vec2) -> None:
        self.values[0] = value.x
        self.values[2] = value.y

    @property
    def yz(self) -> Vec2:
        return Vec2(self.values[1], self.values[2])

    @yz.setter
    def yz(self, value: Vec2) -> None:
        self.values[1] = value.x
        self.values[2] = value.y

    @property
    def xyz(self) -> 'Vec3':
        return Vec3(self.values)
    
    @xyz.setter
    def xyz(self, value: 'Vec3') -> None:
        self.x, self.y, self.z = value.values

    def projected_x(self) -> float:
        return self.projected(0)
    
    def projected_y(self) -> float:
        return self.projected(1)
    
    def projected_z(self) -> float:
        return self.projected(2)

    def __repr__(self) -> str:
        return f'Vec3({self.values[0]}, {self.values[1]}, {self.values[2]})'

    def __str__(self) -> str:
        return f'Vec3({self.values[0]}, {self.values[1]}, {self.values[2]})'

    

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

    def to_double_point(self) -> Tuple[Vec2, Vec2]:
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
        return newRect

    def with_y(self, y: int) -> 'Rect':
        newRect = copy(self)
        newRect.y = y
        return newRect

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

    def scaled(self, scale: Union[Tuple[float, float], float]) -> 'Rect':
        if isinstance(scale, tuple):
            scaleX, scaleY = scale
        elif isinstance(scale, float):
            scaleX, scaleY = scale, scale
        else:
            raise TypeError(f'Expected float or tuple, got {type(scale)}')

        newRect = copy(self)
        newRect.x = int(self.x * scaleX)
        newRect.y = int(self.y * scaleY)
        newRect.width = int(self.width * scaleX)
        newRect.height = int(self.height * scaleY)
        #TODO: make RectInt, RectFloat, etc.

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

    def copy(self):
        return copy(self)

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

   