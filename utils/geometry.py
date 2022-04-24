from ast import Not
from dataclasses import dataclass
from typing import Tuple, Union, overload
from typing_extensions import Self

import utils.colors as colors
from utils.serialization import Serializable

from copy import copy

import numpy as np
from utils.sig import metsig

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

    def with_value(self, index: int, value: Number) -> Self:
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

    def __eq__(self, other: Self) -> bool:
        if isinstance(other, (VecN, int, float, tuple, list, np.ndarray)):

            return len(self) == len(other) and np.allclose(self.values, other.values)
            # return np.all(self.values == other)
        else:
            return False

    def __ne__(self, other: Self) -> bool:
        return not self.__eq__(other)

    def __add__(self, other: Union[Self, Number, tuple, list, np.ndarray]) -> Self:
        if isinstance(other, (float, int)):
            other = [other] * len(self)
        if isinstance(other, (tuple, list, np.ndarray)):
            other = self.__class__(other)
        return self.__class__(self.values + other.values)

    def __sub__(self, other: Union[Self, Number, tuple, list, np.ndarray]) -> Self:
        if isinstance(other, (float, int)):
            other = [other] * len(self)
        if isinstance(other, (tuple, list, np.ndarray)):
            other = self.__class__(other)
        return self.__class__(self.values - other.values)
    
    def __mul__(self, other: Union[Self, Number, tuple, list, np.ndarray]) -> Self:
        if isinstance(other, (float, int)):
            other = [other] * len(self)
        if isinstance(other, (tuple, list, np.ndarray)):
            other = self.__class__(other)
        return self.__class__(self.values * other.values)

    def __truediv__(self, other: Union[Self, Number, Self, tuple, list, np.ndarray]) -> Self:
        if isinstance(other, (VecN)):
            other = other.values
        if isinstance(other, (tuple, list, np.ndarray)):
            other = self.__class__(other)
        return self.__class__(self.values / other)

    def __floordiv__(self, other: Union[Self, Number, tuple, list, np.ndarray]) -> Self:
        if isinstance(other, (VecN)):
            other = other.values
        if isinstance(other, (tuple, list, np.ndarray)):
            other = self.__class__(other)
        return self.__class__(self.values // other)

    def __neg__(self) -> Self:
        return self.__class__(-self.values)

    def __abs__(self) -> Self:
        return self.__class__(abs(self.values))

    def __pow__(self, power: Union[Self, Number, tuple, list, np.ndarray]) -> Self:
        if isinstance(power, (tuple, list, np.ndarray)):
            power = self.__class__(power)
        return self.__class__(self.values ** power.values)

    def __rpow__(self, power: Union[Self, Number, tuple, list, np.ndarray]) -> Self:
        if isinstance(power, (tuple, list, np.ndarray)):
            power = self.__class__(power)
        return self.__class__(power.values ** self.values)

    def __getstate__(self) -> dict:
        return {'values': self.values.tolist()}

    def __setstate__(self, state: dict) -> None:
        self.values = np.array(state['values'])

    def __copy__(self) -> Self:
        return __class__(self.values)

    def __deepcopy__(self, memo: dict) -> Self:
        return __class__(copy(self.values))


    @overload
    def __getitem__(self, index: int) -> Number: ...
    @overload
    def __getitem__(self, index: slice) -> 'VecN': ...
    def __getitem__(self, index: Union[int, slice]) -> Union[float, 'VecN']:
        if isinstance(index, int):
            return self.values[index]
        return __class__(self.values[index])

    def keys(self) -> list[int]:
        return list(range(len(self)))

    def __setitem__(self, index: Union[int, slice], value: Union[Self, float, list, tuple, np.ndarray]) -> None:
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

#   assert Rect2(Vec2(0, 0), Vec2(1, 1)) == Rect2(Vec2(0, 0), Vec2(1, 1))
#     assert Rect2(Vec2(0, 0), Vec2(1, 1)) != Rect2(Vec2(0, 0), Vec2(1, 2))
#     assert Rect2(Vec2(0, 0), Vec2(1, 1)) == Rect2(0, 0, 1, 1)
#     assert Rect2(Vec2(0, 0), Vec2(1, 1)) != Rect2(0, 0, 1, 2)
#     assert Rect2(Vec2(0, 0), Vec2(1, 1)) == Rect2(Vec2(0, 0), size=Vec2(1, 1))
#     assert Rect2(Vec2(0, 0), Vec2(1, 2)) == Rect2(Vec2(0, 0), width=1, height=2)
#     assert Rect2(Vec2(0, 0), Vec2(1, 1)) != Rect2(Vec2(0, 0), width=1, height=2)

#     assert Rect2(Vec2(10, 10), Vec2(20, 20)) == Rect2(10, 10, 20, 20)
#     assert Rect2(Vec2(10, 10), Vec2(20, 20)) != Rect2(10, 10, 20, 21)
#     assert Rect2(Vec2(10, 10), Vec2(20, 20)) == Rect2(Vec2(10, 10), Vec2(20, 20))
#     assert Rect2(Vec2(10, 10), Vec2(20, 20)) != Rect2(Vec2(10, 10), Vec2(20, 21))
#     assert Rect2(Vec2(10, 10), Vec2(20, 20)) == Rect2(10, 10, size=Vec2(10, 10))
#     assert Rect2(Vec2(10, 10), Vec2(20, 20)) != Rect2(10, 10, size=Vec2(10, 11))
#     assert Rect2(Vec2(10, 10), Vec2(20, 20)) == Rect2(Vec2(10, 10), width=10, height=10)
#     assert Rect2(Vec2(10, 10), Vec2(20, 20)) != Rect2(Vec2(10, 10), width=10, height=11)
#     assert Rect2(Vec2(10, 10), Vec2(20, 20)) == Rect2(Rect2(Vec2(10, 10), Vec2(20, 20)))

#     rect = Rect2(Vec2(10, 10), Vec2(20, 20))
#     assert rect.start == Vec2(10, 10)
#     assert rect.end == Vec2(20, 20)
#     assert rect.size == Vec2(10, 10)
#     assert rect.width == 10
#     assert rect.height == 10
#     assert rect.center == Vec2(15, 15)
#     assert rect.left == 10
#     assert rect.right == 20
#     assert rect.top == 20
#     assert rect.bottom == 10
#     assert rect.top_left == Vec2(10, 20)
#     assert rect.top_right == Vec2(20, 20)
#     assert rect.bottom_left == Vec2(10, 10)
#     assert rect.bottom_right == Vec2(20, 10)
#     assert rect.contains(Vec2(15, 15))
#     assert rect.contains(Vec2(10, 10))
#     assert rect.contains(Vec2(20, 20))
#     assert not rect.contains(Vec2(5, 5))
#     assert not rect.contains(Vec2(25, 25))
#     assert not rect.contains(Vec2(15, 25))
#     assert not rect.contains(Vec2(25, 15))
#     assert not rect.contains(Vec2(5, 15))
#     assert not rect.contains(Vec2(15, 5))
#     assert not rect.contains(Vec2(5, 25))

#     assert rect.intersects(Rect2(Vec2(15, 15), Vec2(25, 25)))
#     assert rect.intersects(Rect2(Vec2(15, 15), Vec2(25, 25), width=10, height=10))
#     assert rect.intersects(Rect2(Vec2(15, 15), Vec2(25, 25), size=Vec2(10, 10)))   

#     assert rect + Vec2(10, 10) == Rect2(Vec2(20, 20), Vec2(30, 30))
#     assert rect.expand(10) == Rect2(Vec2(0, 0), Vec2(30, 30))    

@dataclass
class Rect2(Serializable):
    start: Vec2
    end: Vec2
    @overload
    def __init__(self, arg1: Number, arg2: Number, arg3: Number, arg4: Number):
        '''Constructs a Rect2 from 4 values (min_x, min_y, max_x, max_y)'''
        ... 

    @overload
    def __init__(self, arg1: Vec2, arg2: Vec2):
        '''Constructs a Rect2 from 2 Vec2s (start, end)'''
        ...

    @overload
    def __init__(self, arg1: 'Rect2'):
        '''Constructs a Rect2 from another Rect2'''
        ...

    @overload
    def __init__(self, arg1: 'Vec2', *, width: Number, height: Number):
        '''Constructs a Rect2 from a Vec2 and width and height'''
        ...

    @overload
    def __init__(self, arg1: 'Number', arg2: 'Number', *, width: Number, height: Number):
        '''Constructs a Rect2 from x, y, width and height'''
        ...
    
    @overload
    def __init__(self, arg1: 'Vec2', *, size: Vec2):
        '''Constructs a Rect2 from a Vec2 and a Vec2 (size)'''
        ...

    @overload
    def __init__(self, arg1: 'Number', arg2: 'Number', *, size: Vec2):
        '''Constructs a Rect2 from x, y, and a Vec2 (size)'''
        ...    

    def __init__(self, arg1: Union[Vec2, 'Rect2', Number], arg2: Union[Vec2, Number] = None, *args: Number, size: Vec2 = None, width: Number = None, height: Number = None):
        assert arg1 is not None, 'Rect2 must be initialized with at least one argument'
        if isinstance(arg1, Rect2):
            assert arg2 is None, 'Rect2(Rect2) copy can only be initialized with one argument'
            assert len(args) == 0, 'Rect2(Rect2) copy can only be initialized with one argument'
            assert size is None, 'Rect2(Rect2) copy can only be initialized with one argument'
            assert width is None, 'Rect2(Rect2) copy can only be initialized with one argument'
            assert height is None, 'Rect2(Rect2) copy can only be initialized with one argument'
            arg1, arg2 = arg1.start, arg1.end # Convert Rect2(Rect2) to Rect2(Vec2, Vec2)

        end_defined = False
        if isinstance(arg1, Vec2):
            self.start = arg1.xy
            if arg2 is not None:
                if not isinstance(arg2, Vec2):
                    raise TypeError(f'Rect2 can only be initialized with 2 Vec2s, got {type(arg2)}')
                self.end = arg2.xy
                end_defined = True

        elif isinstance(arg1, (float, int)):
            if arg2 is None:
                raise ValueError('Rect2(x, y, ...) must be initialized with at least two arguments')
            if not isinstance(arg2, (float, int)):
                raise ValueError('Rect2(x, y, ...): y must be a number')
                
            self.start = Vec2(arg1, arg2)

            if len(args) != 0:
                # Some positional arguments were given
                if len(args) != 2:
                    raise ValueError('Rect2(min_x, min_y, max_x, max_y): too many or too few positional arguments')
                if not isinstance(args[0], (float, int)):
                    raise ValueError('Rect2(min_x, min_y, max_x, max_y): max_x must be a number')
                if not isinstance(args[1], (float, int)):
                    raise ValueError('Rect2(min_x, min_y, max_x, max_y): max_y must be a number')
                self.end = Vec2(args[0], args[1])
                end_defined = True

        if size is not None:
            assert not end_defined, 'Rect2 can only be initialized either with start and end or with size (`size=Vec2(width, height)` or `width=width, height=height`)'
            if not isinstance(size, Vec2):
                raise ValueError('Rect2(x, y, size=Vec2) must be initialized with a Vec2 (size)')
            self.end = self.start + size
            end_defined = True

        width_or_height_defined = width is not None or height is not None
        if width_or_height_defined:
            assert not end_defined, 'Rect2 can only be initialized either with start and end or with size (`size=Vec2(width, height)` or `width=width, height=height`)'
            if width is None:
                raise ValueError('Rect2(x, y, width=width, ...) must be initialized with a height')
            elif height is None:
                raise ValueError('Rect2(x, y, height=height, ...) must be initialized with a width')

            self.end = self.start + Vec2(width, height)
            end_defined = True

        if not end_defined:
            raise ValueError('Rect2 end not specified: use some of `(min_x, min_y, max_x, max_y)` or `(start, end)` or `(start, width=, height=)` or `(x, y, width=, height=)` or `(x, y, size=Vec2)`')
        
        # Swap start and end if necessary
        if self.start.x > self.end.x or self.start.y > self.end.y:
            self.start, self.end = self.end, self.start
        pass

    
    @property
    def x(self):
        return self.start.x
    
    @property
    def y(self):
        return self.start.y

    @property
    def xy(self):
        return self.start.xy

    @property
    def width(self):
        return self.end.x - self.start.x

    @property
    def height(self):
        return self.end.y - self.start.y

    @property
    def w(self):
        return self.width
    
    @property
    def h(self):
        return self.height

    @property
    def size(self):
        return self.end - self.start
    
    @property
    def wh(self):
        return self.size.xy

    @property
    def xywh(self):
        return VecN(*self.start.xy, *self.size.xy)

    @property
    def bbox(self):
        return VecN(*self.start.xy, *self.end.xy)

    @property
    def tuple_bbox(self):
        return (*self.start.xy, *self.end.xy)

    @property
    def tuple_xywh(self):
        return (*self.start.xy, *self.size.xy)

    @property
    def center(self):
        return self.start + self.size / 2

    @property
    def left(self):
        return self.start.x
    
    @property
    def right(self):
        return self.end.x
    
    @property
    def top(self):
        return self.end.y

    @property
    def bottom(self):
        return self.start.y

    @property
    def min(self):
        return self.start

    @property
    def bottom_left(self):
        return self.start.xy

    @property
    def top_left(self):
        return Vec2(self.start.x, self.end.y)

    @property
    def top_right(self):
        return self.end.xy

    @property
    def bottom_right(self):
        return Vec2(self.end.x, self.start.y)

    def __iter__(self):
        yield from self.bbox

    def __repr__(self):
        return f'Rect2({self.start}, {self.end}, size={self.size})'

    def __str__(self):
        return f'Rect2({self.start}, {self.end}, size={self.size})'

    def __eq__(self, other):
        if not isinstance(other, Rect2):
            return False
        return self.start == other.start and self.end == other.end
    
    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.start, self.end))

    def __add__(self, other):
        if isinstance(other, Vec2):
            return Rect2(self.start + other, self.end + other)
        else:
            raise TypeError(f'Rect2 can only be added with a Vec2, got {type(other)}')
    
    def __sub__(self, other):
        if isinstance(other, Vec2):
            return Rect2(self.start - other, self.end - other)
        else:
            raise TypeError(f'Rect2 can only be subtracted with a Vec2, got {type(other)}')

    def __mul__(self, other):
        if isinstance(other, Vec2):
            return Rect2(self.start * other, self.end * other)
        elif isinstance(other, (int, float)):
            return Rect2(self.start * other, self.end * other)
        else:
            raise TypeError(f'Rect2 can only be multiplied with a Vec2 or a number, got {type(other)}')

    def __truediv__(self, other):
        if isinstance(other, Vec2):
            return Rect2(self.start / other, self.end / other)
        elif isinstance(other, (int, float)):
            return Rect2(self.start / other, self.end / other)
        else:
            raise TypeError(f'Rect2 can only be divided with a Vec2 or a number, got {type(other)}')

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rtruediv__(self, other):
        return self.__truediv__(other)

    def __contains__(self, other):
        if isinstance(other, Vec2):
            return self.start.x <= other.x <= self.end.x and self.start.y <= other.y <= self.end.y
        else:
            raise TypeError(f'Rect2 can only be checked for containment with a Vec2, got {type(other)}')

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.bbox[index]
        elif isinstance(index, slice):
            return Rect2(self.bbox[index])
        else:
            raise TypeError(f'Rect2 can only be sliced with an int or a slice, got {type(index)}')

    def __setitem__(self, index, value):
        assert index in range(4), f'Rect2 can only be indexed with an int in range(4), got {index}'
        targets = [ self.start, self.start, self.end, self.end ]
        targets[index].values[index % 2] = value # start.values[0 -> 0] or start.values[1 -> 1], end.values[2 -> 0] or end.values[3 -> 1]

    def intersects(self, other: 'Rect2') -> bool:
        if not isinstance(other, Rect2):
            raise TypeError(f'Rect2 can only be intersected with another Rect2, got {type(other)}')

        return self.start.x <= other.end.x and self.end.x >= other.start.x and self.start.y <= other.end.y and self.end.y >= other.start.y

    @metsig(__contains__)
    def contains(self, *args, **kwargs) -> bool:
        return self.__contains__(*args, **kwargs)

    def expanded_start(self, size: Vec2) -> 'Rect2':
        return Rect2(self.start - size, self.end)
    
    def expanded_end(self, size: Vec2) -> 'Rect2':
        return Rect2(self.start, self.end + size)

    @overload
    def expanded(self, size: Vec2) -> 'Rect2':
        ...
    @overload
    def expanded(self, size: Number) -> 'Rect2':
        ...
    def expanded(self, size: Union[Vec2, float, int]) -> 'Rect2':
        if isinstance(size, (int, float)):
            size = Vec2(size, size)
        return Rect2(self.start - size/2, self.end + size/2)

    def expanded_left(self, size: float) -> 'Rect2':
        return Rect2(self.start.x - size, self.end.x)
    
    def expanded_right(self, size: float) -> 'Rect2':
        return Rect2(self.start.x, self.end.x + size)

    def expanded_top(self, size: float) -> 'Rect2':
        return Rect2(self.start.y, self.end.y + size)

    def expanded_bottom(self, size: float) -> 'Rect2':
        return Rect2(self.start.y - size, self.end.y)

    def expanded_top_left(self, size: Vec2) -> 'Rect2':
        return Rect2(self.start.xy - size, self.end.xy)

    def expanded_top_right(self, size: Vec2) -> 'Rect2':
        return Rect2(self.start.xy, self.end.xy + size)

    def expanded_bottom_left(self, size: Vec2) -> 'Rect2':
        return Rect2(self.start.xy - size, self.end.xy)

    def expanded_bottom_right(self, size: Vec2) -> 'Rect2':
        return Rect2(self.start.xy, self.end.xy + size)

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

   