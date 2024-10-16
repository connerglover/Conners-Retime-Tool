from decimal import Decimal as d
import json
import re

class Load:
    def __init__(self, start_frame: int, end_frame: int):
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.length = end_frame - start_frame
        pass

class Time:
    def __init__(self, start_frame: int = 0, end_frame: int = 0, framerate: d = 60, precision: int = 3, loads: list[Load] = []):
        self.start_frame = start_frame
        self.end_frame = end_frame
        
        self.framerate = framerate
        self.precision = precision
        
        self.loads = loads
        
        self.length = int(self.end_frame - self.start_frame)
        self.length_loads = int(self.length - sum(load.length for load in self.loads))

        self.time = round(d(self.length / self.framerate), self.precision)
        self.time_loads = round(d(self.length_loads / self.framerate), self.precision)
        
        self.mod_note = (f"Mod Note: Retimed to {self.src_format(True)} without loads, and {self.src_format()} with loads" if self.time != self.time_loads  else f"Mod Note: Retimed to {self.src_format()}") + f" at {self.framerate} FPS using [Conner's Retime Tool](https://github.com/connerglover/conners-retime-tool)"
        
        pass
    
    def recalculate(self) -> None:
        self.length = int(self.end_frame - self.start_frame)
        self.length_loads = int(self.length - sum(load.length for load in self.loads))

        if self.framerate != 0:
            self.time = round(d(self.length / d(self.framerate)), self.precision)
            self.time_loads = round(d(self.length_loads / d(self.framerate)), self.precision)
        else:
            self.time = d(0.000)
            self.time_loads = d(0.000)
        
        self.mod_note = (f"Mod Note: Retimed to {self.src_format(True)} without loads, and {self.src_format()} with loads" if self.time != self.time_loads  else f"Mod Note: Retimed to {self.src_format(self.time)}") + f" at {self.framerate} FPS using [Conner's Retime Tool](https://github.com/connerglover/conners-retime-tool)"
        
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
        if start_frame != None and end_frame != None:
            if start_frame > end_frame:
                raise Exception
        if start_frame != None:
            self.loads[index].start_frame = start_frame
        if end_frame != None:
            self.loads[index].end_frame = end_frame
            
        self.loads[index].length = self.loads[index].end_frame - self.loads[index].start_frame
        
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

    def src_format(self, loads: bool = False) -> str:
        time = self.time_loads if loads else self.time
        if time < d(0):
            time_str = str(d(0.000))
        else:
            time_str = str(time)
        
        if '.' in time_str:
            seconds, milliseconds = map(int, time_str.split(".", 1))
        else:
            seconds = int(time_str)
            milliseconds = "000"
        
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        
        hours_str = f"{hours:02}"
        minutes_str = f"{minutes:02}"
        seconds_str = f"{seconds:02}"
        milliseconds_str = str(milliseconds).rjust(3, "0")
        
        return f"{hours_str}h {minutes_str}m {seconds_str}s {milliseconds_str}ms"
    
    def iso_format(self, loads: bool = False) -> str:
        time_str = str(self.time_loads if loads else self.time)
        
        if '.' in time_str:
            seconds, milliseconds = map(int, time_str.split(".", 1))
        else:
            seconds = int(time_str)
            milliseconds = "000"

        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        
        hours_str = f"{hours:02}"
        minutes_str = f"{minutes:02}"
        seconds_str = f"{seconds:02}"
        milliseconds_str = str(milliseconds).rjust(3, "0")
        
        if hours > 0:
            return f"{hours_str}:{minutes_str}:{seconds_str}.{milliseconds_str}"
        elif minutes > 0:
            return f"{minutes_str}:{seconds_str}.{milliseconds_str}"
        else:
            return f"{seconds_str}.{milliseconds_str}"

def debug_info_to_frame(time: Time, debug_info: str) -> int:
    debug_info = "{" + debug_info.split("{", 1)[-1]
    
    try:
        parsed_debug_info = json.loads(debug_info)
    except json.decoder.JSONDecodeError:
        raise ValueError("The debug info provided is invalid.\nPlease re-enter debug info.")
    
    try:
        cmt = parsed_debug_info["cmt"]
    except KeyError:
        raise ValueError("The debug info provided is invalid.\nPlease re-enter debug info.")
    
    output = d(cmt) * d(time.framerate)
    output = int(round(output, 0))
    
    return output

def clean_framerate(framerate: str) -> d:
    cleaned_framerate = re.sub(r'[^0-9.]', '', framerate)
    
    if not re.search(r'[0-9]', cleaned_framerate):
        return "0"
    
    if cleaned_framerate.count('.') > 1:
        first_period_index = cleaned_framerate.find('.')
        cleaned_framerate = cleaned_framerate[:first_period_index + 1] + cleaned_framerate[first_period_index + 1:].replace('.', '')
    
    if cleaned_framerate.endswith('.'):
        cleaned_framerate += '0'
    
    cleaned_framerate = d(cleaned_framerate)
    
    return cleaned_framerate

def clean_frame(framerate: str) -> int:
    if any(char.isdigit() for char in framerate):
        cleaned_frame = int(re.sub(r"[^0-9]", "", framerate))
    else:
        cleaned_frame = 0
    
    return cleaned_frame