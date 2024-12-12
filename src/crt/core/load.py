from dataclasses import dataclass

@dataclass
class Load:
    start_frame: int
    end_frame: int

    @property
    def length(self):
        return self.end_frame - self.start_frame