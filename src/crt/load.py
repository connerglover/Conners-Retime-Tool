# Standard library
from dataclasses import dataclass
from typing import NoReturn

@dataclass
class Load:
    """
    A class that represents a load in a video.
    """
    start_frame: int
    end_frame: int

    @property
    def length(self) -> NoReturn:
        """The length of the load.
        """        
        return int(self.end_frame) - int(self.start_frame)
