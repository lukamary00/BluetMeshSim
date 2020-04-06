"""Decribe messages that are passing through network."""
from dataclasses import dataclass


@dataclass
class Frame:
    """Describe frame, that devices sen to each other."""
    source_id: int
    dest_id: int
    frame_id: int = None


    def __str__(self):
        return f"Going from {self.source_id} to {self.dest_id}"
