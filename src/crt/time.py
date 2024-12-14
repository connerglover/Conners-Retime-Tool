from decimal import Decimal as d

from crt.load import Load

class Time:
    """
    A class that represents a time in a video.
    """
    
    def __init__(self, start_frame: int = 0, end_frame: int = 0, framerate: d = 60, precision: int = 3, loads: list[Load] | None = None):
        """
        Initializes the Time class.
        
        Args:
            start_frame (int): The start frame of the time.
            end_frame (int): The end frame of the time.
            framerate (d): The framerate of the video.
            precision (int): The precision of the time.
            loads (list[Load] | None): The loads of the time.
        """
        self.loads = loads if loads is not None else []
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.framerate = framerate
        self.precision = precision
        self._cache = {
            'length_loads': None,
            'avg_load_length': None,
            'total_load_length': None
        }
        self._cache_dirty = True
        self._format_cache = {
            'src': {'with_loads': None, 'without_loads': None},
            'iso': {'with_loads': None, 'without_loads': None}
        }
        self._format_cache_dirty = True
        
    def _update_cache(self):
        if self._cache_dirty:
            total_load_length = sum(load.length for load in self.loads)
            self._cache['total_load_length'] = total_load_length
            self._cache['length_loads'] = self.length - total_load_length
            self._cache['avg_load_length'] = total_load_length // len(self.loads) if self.loads else 0
            self._cache_dirty = False

    def _invalidate_caches(self):
        self._cache_dirty = True
        self._format_cache_dirty = True

    @property
    def length(self) -> int:
        """The total length in frames."""
        return int(self.end_frame - self.start_frame)
    
    @property
    def length_loads(self) -> int:
        """The length in frames excluding loads."""
        self._update_cache()
        return self._cache['length_loads']
    
    @property
    def average_load_length(self) -> int:
        """The average length of the loads."""
        self._update_cache()
        return self._cache['avg_load_length']
    
    @property
    def time(self) -> d:
        """The total time including loads."""
        if self.framerate == 0:
            return d(0.000)
        return round(d(self.length / d(self.framerate)), self.precision)
    
    @property
    def time_loads(self) -> d:
        """The total time excluding loads."""
        if self.framerate == 0:
            return d(0.000)
        return round(d(self.length_loads / d(self.framerate)), self.precision)
    
    def clear_loads(self) -> None:
        """
        Clears the loads.
        """
        self.loads = []
        self._invalidate_caches()
        
        return
    
    def mutate(self, start_frame: int = None, end_frame: int = None, framerate: d = None) -> None:
        """
        Mutates the time.
        
        Args:
            start_frame (int): The start frame of the time.
            end_frame (int): The end frame of the time.
            framerate (d): The framerate of the video.
        """
        self.start_frame = start_frame if start_frame is not None else self.start_frame
        self.end_frame = end_frame if end_frame is not None else self.end_frame
        self.framerate = framerate if framerate is not None else self.framerate
        self._invalidate_caches()
        
        return
    
    def get_load(self, index) -> d:
        """
        Gets the load time.
        
        Args:
            index (int): The index of the load.
        
        Returns:
            d: The load time.
        """
        load_time = self.loads[index].length / self.framerate
        
        return load_time
    
    def delete_load(self, index) -> None:
        """
        Deletes the load.
        
        Args:
            index (int): The index of the load.
        """
        del self.loads[index]
        self._invalidate_caches()
        
        return
    
    def mutate_load(self, index: int, start_frame: int = None, end_frame: int = None) -> None:
        """
        Mutates the load.
        
        Args:
            index (int): The index of the load.
            start_frame (int): The start frame of the load.
            end_frame (int): The end frame of the load.
        """
        if start_frame is not None and end_frame is not None and start_frame > end_frame:
            raise ValueError("The load time ends before it starts.")
            
        if start_frame is not None:
            self.loads[index].start_frame = start_frame
        if end_frame is not None:
            self.loads[index].end_frame = end_frame
        self._invalidate_caches()
        
        return
    
    def add_load(self, start_frame: int, end_frame: int) -> None:
        """
        Adds a load.
        
        Args:
            start_frame (int): The start frame of the load.
            end_frame (int): The end frame of the load.
        """
        if start_frame == 0 and end_frame == 0:
            raise ValueError("You must provide an input for the loads")
        elif start_frame == end_frame:
            raise ValueError("The duration of the load is 0.000")
        elif start_frame > end_frame:
            raise ValueError("The load time ends before it starts.")
        elif self.length_loads - (end_frame - start_frame) < 0:
            raise ValueError("The load time exceeds the time")
        
        load = Load(start_frame, end_frame)
        self.loads.append(load)
        self._invalidate_caches()
        
        return

    def format_time_components(self, time: d) -> tuple[str, str, str, str]:
        """
        Formats the time components.
        
        Args:
            time (d): The time.
        
        Returns:
            tuple[str, str, str, str]: The formatted time components.
        """
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

    def src_format(self, loads: bool = False) -> str:
        """
        Formats the time.
        
        Args:
            loads (bool): Whether to format the time with loads.
        
        Returns:
            str: The formatted time.
        """
        if self._format_cache_dirty or self._format_cache['src']['with_loads' if loads else 'without_loads'] is None:
            hours, minutes, seconds, ms = self.format_time_components(self.time_loads if loads else self.time)
            formatted = f"{hours}h {minutes}m {seconds}s {ms}ms"
            self._format_cache['src']['with_loads' if loads else 'without_loads'] = formatted
        return self._format_cache['src']['with_loads' if loads else 'without_loads']
    
    def iso_format(self, loads: bool = False) -> str:
        """
        Formats the time.
        
        Args:
            loads (bool): Whether to format the time with loads.
        
        Returns:
            str: The formatted time.
        """
        hours, minutes, seconds, ms = self.format_time_components(self.time_loads if loads else self.time)
        
        if int(hours) > 0:
            return f"{hours}:{minutes}:{seconds}.{ms}"
        elif int(minutes) > 0:
            return f"{minutes}:{seconds}.{ms}"
        return f"{seconds}.{ms}"
