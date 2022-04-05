
from typing import Any, Callable, TypeVar

T = TypeVar('T')
def setsig(sig: T) -> Callable[[Any], T]:
    '''Decorator to set the signature of a function to the given value.\n
        Usage:\n
            @setsig(print)\n
            def my_print(*args, **kwargs):\n
                do_stuff_before_print() # For example, start a timer here.\n
                print(*args, **kwargs)\n

            if __name__ == '__main__':\n
                # Works just like print('Hello', 'World'), with IDE, type checking, and other features \n
                my_print('Hello', 'World') 
    '''
    def setsig_dec(func) -> T:
        return func
    return setsig_dec