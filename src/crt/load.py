from dataclasses import dataclass

@dataclass
class Load:
    """
    A class that represents a load in a video.
    """
    start_frame: int
    end_frame: int

    @property
    def length(self):
        return int(self.end_frame) - int(self.start_frame)
