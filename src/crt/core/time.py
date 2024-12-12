from decimal import Decimal as d

from crt.core.load import Load

class Time:
    GITHUB_LINK = "[Conner's Retime Tool](https://github.com/connerglover/conners-retime-tool)"
    
    def __init__(self, start_frame: int = 0, end_frame: int = 0, framerate: d = 60, precision: int = 3, loads: list[Load] | None = None):
        self.loads = loads if loads is not None else []
        self.start_frame = start_frame
        self.end_frame = end_frame
        
        self.framerate = framerate
        self.precision = precision
        
        self.length = int(self.end_frame - self.start_frame)
        self.length_loads = int(self.length - sum(load.length for load in self.loads))

        self.time = round(d(self.length / self.framerate), self.precision)
        self.time_loads = round(d(self.length_loads / self.framerate), self.precision)
        
        self._update_mod_note()
        
        pass
    
    def _update_mod_note(self):
        base_note = f"Mod Note: Retimed to "
        if self.time != self.time_loads:
            self.mod_note = f"{base_note}{self.src_format(True)} without loads, and {self.src_format()} with loads at {self.framerate} FPS using {self.GITHUB_LINK}"
        else:
            self.mod_note = f"{base_note}{self.src_format()} at {self.framerate} FPS using {self.GITHUB_LINK}"
    
    def recalculate(self) -> None:
        self.length = int(self.end_frame - self.start_frame)
        self.length_loads = int(self.length - sum(load.length for load in self.loads))

        if self.framerate != 0:
            self.time = round(d(self.length / d(self.framerate)), self.precision)
            self.time_loads = round(d(self.length_loads / d(self.framerate)), self.precision)
        else:
            self.time = d(0.000)
            self.time_loads = d(0.000)
        
        self._update_mod_note()
        
        return
    
    def mutate(self, start_frame: int = None, end_frame: int = None, framerate: d = None) -> None:
        if start_frame is not None and end_frame is not None:
            if start_frame > end_frame:
                raise ValueError("The time ends before it starts.")
            else:
                self.start_frame = start_frame
                self.end_frame = end_frame
        elif start_frame is not None:
            if start_frame > self.end_frame and self.end_frame != 0:
                raise ValueError("The time ends before it starts.")
            else:
                self.start_frame = start_frame
        elif end_frame is not None:
            if self.start_frame > end_frame:
                raise ValueError("The time ends before it starts.")
            else:
                self.end_frame = end_frame
                
        if framerate is not None:
            self.framerate = d(framerate)
        
        self.recalculate()
        
        return
    
    def get_load(self, index) -> d:
        load_time = self.loads[index].length / self.framerate
        
        return load_time
    
    def delete_load(self, index) -> None:
        del self.loads[index]
        
        self.recalculate()
        
        return
    
    def mutate_load(self, index: int, start_frame: int = None, end_frame: int = None) -> None:
        if start_frame is not None and end_frame is not None and start_frame > end_frame:
            raise ValueError("The load time ends before it starts.")
            
        if start_frame is not None:
            self.loads[index].start_frame = start_frame
        if end_frame is not None:
            self.loads[index].end_frame = end_frame
            
        self.recalculate()
        
        return
    
    def add_load(self, start_frame: int, end_frame: int) -> None:
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
        
        self.recalculate()
        
        return

    def _format_time_components(self, time: d) -> tuple[str, str, str, str]:
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
        hours, minutes, seconds, ms = self._format_time_components(self.time_loads if loads else self.time)
        return f"{hours}h {minutes}m {seconds}s {ms}ms"
    
    def iso_format(self, loads: bool = False) -> str:
        hours, minutes, seconds, ms = self._format_time_components(self.time_loads if loads else self.time)
        
        if int(hours) > 0:
            return f"{hours}:{minutes}:{seconds}.{ms}"
        elif int(minutes) > 0:
            return f"{minutes}:{seconds}.{ms}"
        return f"{seconds}.{ms}"
