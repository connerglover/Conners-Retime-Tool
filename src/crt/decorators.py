# Standard library
from functools import wraps
from typing import Callable, Tuple
from decimal import Decimal as d

def error_handler(func: Callable):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            self._show_error(str(e))
            return None
    return wrapper

def invalidate_cache(func: Callable):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.invalidate_caches()
        return result
    return wrapper

def memoize_property(func: Callable):
    cache_key = f'_cache_{func.__name__}'
    @property
    @wraps(func)
    def wrapper(self):
        if not hasattr(self, cache_key) or self._cache_dirty:
            setattr(self, cache_key, func(self))
        return getattr(self, cache_key)
    return wrapper

def validate_load(func: Callable):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        start_frame = kwargs.get('start_frame', args[0] if args else None)
        end_frame = kwargs.get('end_frame', args[1] if len(args) > 1 else None)
        
        if start_frame is not None and end_frame is not None:
            if start_frame == end_frame:
                raise ValueError("The duration of the load is 0.000")
            if start_frame > end_frame:
                raise ValueError("The load time ends before it starts.")
        return func(self, *args, **kwargs)
    return wrapper

def format_time(func: Callable) -> Callable:
    def format_components(time: d) -> Tuple[str, str, str, str]:
        time_str = str(max(time, d(0)))
        
        if '.' in time_str:
            seconds, milliseconds = map(int, time_str.split(".", 1))
        else:
            seconds, milliseconds = int(time_str), 0
        
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        
        return (
            f"{hours:02}",
            f"{minutes:02}", 
            f"{seconds:02}",
            str(milliseconds).rjust(3, "0")
        )

    @wraps(func)
    def wrapper(self, loads: bool = False) -> str:
        time_value = self.time_loads if loads else self.time
        hours, minutes, seconds, ms = format_components(time_value)
        return func(self, hours, minutes, seconds, ms)
    return wrapper
